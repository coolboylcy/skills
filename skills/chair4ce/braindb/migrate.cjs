#!/usr/bin/env node
/**
 * BrainDB Memory Migration
 * 
 * Imports existing OpenClaw workspace files into BrainDB.
 * Scans for MEMORY.md, daily notes, SOUL.md, USER.md, IDENTITY.md,
 * TOOLS.md, AGENTS.md, and any custom markdown files.
 *
 * Uses swarm (Gemini Flash) for fact extraction when available,
 * falls back to chunked encoding when swarm is unavailable.
 *
 * Usage:
 *   node migrate.js [workspace_path]          # Migrate workspace
 *   node migrate.js --scan [workspace_path]   # Preview what would be migrated
 *   node migrate.js --file path/to/file.md    # Migrate a single file
 *
 * Options:
 *   --braindb URL    BrainDB gateway URL (default: http://localhost:3333)
 *   --swarm PORT     Swarm daemon port (default: 9999)
 *   --swarm          Use swarm (Gemini Flash) for smarter extraction (sends data to Google API)
 *   --no-swarm       Force local chunked encoding (default)
 *   --dry-run        Extract facts but don't encode
 *   --scan           Just list files that would be migrated
 *   --batch N        Files per swarm batch (default: 8)
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

// ─── Config ──────────────────────────────────────────────
const args = process.argv.slice(2);
const flags = new Set(args.filter(a => a.startsWith('--')));
// Filter out flag values (args that follow --flag)
const positional = [];
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    // Skip flags that take a value
    if (['--braindb', '--swarm', '--batch', '--file'].includes(args[i])) i++;
    continue;
  }
  positional.push(args[i]);
}

function getArg(name, fallback) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}

const WORKSPACE = positional[0] || process.cwd();
const BRAINDB_URL = getArg('braindb', 'http://localhost:3333');
const SWARM_PORT = parseInt(getArg('swarm', '9999'));
const BATCH_SIZE = parseInt(getArg('batch', '8'));
const DRY_RUN = flags.has('--dry-run');
const SCAN_ONLY = flags.has('--scan');
const USE_SWARM = flags.has('--swarm');
const NO_SWARM = !USE_SWARM; // Default: local-only. Pass --swarm to enable Gemini API extraction.
const SINGLE_FILE = getArg('file', null);

// ─── File Discovery ──────────────────────────────────────

// Files to look for, with their shard mapping and priority
const KNOWN_FILES = [
  { pattern: 'MEMORY.md', shard: 'episodic', priority: 1, desc: 'Long-term memory' },
  { pattern: 'USER.md', shard: 'semantic', priority: 1, desc: 'User profile' },
  { pattern: 'IDENTITY.md', shard: 'semantic', priority: 1, desc: 'Agent identity' },
  { pattern: 'SOUL.md', shard: 'procedural', priority: 1, desc: 'Personality & behavior' },
  { pattern: 'AGENTS.md', shard: 'procedural', priority: 2, desc: 'Agent instructions' },
  { pattern: 'TOOLS.md', shard: 'procedural', priority: 2, desc: 'Tool configuration' },
  { pattern: 'HEARTBEAT.md', shard: 'procedural', priority: 3, desc: 'Heartbeat config' },
];

const DAILY_NOTE_PATTERN = /^memory\/\d{4}-\d{2}-\d{2}\.md$/;
const MEMORY_DIRS = ['memory', 'memory/topics', 'research', 'docs', 'notes'];

function discoverFiles(workspacePath) {
  const files = [];
  const seen = new Set();

  // 1. Known workspace files
  for (const known of KNOWN_FILES) {
    const fullPath = path.join(workspacePath, known.pattern);
    if (fs.existsSync(fullPath)) {
      files.push({
        path: fullPath,
        relative: known.pattern,
        shard: known.shard,
        priority: known.priority,
        desc: known.desc,
        type: 'workspace',
      });
      seen.add(fullPath);
    }
  }

  // 2. Daily notes
  const memoryDir = path.join(workspacePath, 'memory');
  if (fs.existsSync(memoryDir)) {
    for (const entry of fs.readdirSync(memoryDir, { withFileTypes: true })) {
      if (entry.isFile() && /^\d{4}-\d{2}-\d{2}\.md$/.test(entry.name)) {
        const fullPath = path.join(memoryDir, entry.name);
        if (!seen.has(fullPath)) {
          files.push({
            path: fullPath,
            relative: `memory/${entry.name}`,
            shard: 'episodic',
            priority: 2,
            desc: `Daily note (${entry.name.replace('.md', '')})`,
            type: 'daily',
          });
          seen.add(fullPath);
        }
      }
    }
  }

  // 3. Other markdown files in known directories
  for (const dir of MEMORY_DIRS) {
    const dirPath = path.join(workspacePath, dir);
    if (!fs.existsSync(dirPath)) continue;
    walkDir(dirPath, (fullPath, relPath) => {
      if (!seen.has(fullPath) && fullPath.endsWith('.md')) {
        files.push({
          path: fullPath,
          relative: path.join(dir, relPath),
          shard: guessShard(relPath, dir),
          priority: 3,
          desc: `${dir}/${relPath}`,
          type: 'extra',
        });
        seen.add(fullPath);
      }
    });
  }

  // Sort: priority first, then alphabetical
  files.sort((a, b) => a.priority - b.priority || a.relative.localeCompare(b.relative));
  return files;
}

function walkDir(dir, callback, base) {
  base = base || dir;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walkDir(full, callback, base);
    else callback(full, path.relative(base, full));
  }
}

function guessShard(relPath, dir) {
  const lower = relPath.toLowerCase();
  if (dir === 'research') return 'semantic';
  if (lower.includes('topic')) return 'semantic';
  if (lower.includes('lesson') || lower.includes('how') || lower.includes('procedure')) return 'procedural';
  return 'episodic';
}

// ─── HTTP Helpers ────────────────────────────────────────

function httpPost(url, body, timeoutMs = 120000) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const parsed = new URL(url);
    const req = http.request({
      hostname: parsed.hostname,
      port: parsed.port,
      path: parsed.pathname,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) },
      timeout: timeoutMs,
    }, (res) => {
      let buf = '';
      res.on('data', chunk => buf += chunk);
      res.on('end', () => {
        const lines = buf.trim().split('\n');
        try { resolve(JSON.parse(lines[lines.length - 1])); } catch { resolve(null); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.write(data);
    req.end();
  });
}

function httpGet(url, timeoutMs = 5000) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const req = http.request({
      hostname: parsed.hostname,
      port: parsed.port,
      path: parsed.pathname,
      method: 'GET',
      timeout: timeoutMs,
    }, (res) => {
      let buf = '';
      res.on('data', chunk => buf += chunk);
      res.on('end', () => { try { resolve(JSON.parse(buf)); } catch { resolve(null); } });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

// ─── Fact Extraction ─────────────────────────────────────

function truncate(text, maxChars = 4000) {
  if (text.length <= maxChars) return text;
  return text.substring(0, maxChars) + '\n...[truncated]';
}

function buildExtractionPrompt(fileContent, fileName, shard) {
  const shardGuidance = {
    episodic: 'Focus on events, decisions, conversations, milestones, and things that happened.',
    semantic: 'Focus on facts, identities, preferences, relationships, knowledge, and concepts.',
    procedural: 'Focus on rules, workflows, processes, lessons learned, and how-to knowledge.',
  };

  return `Extract the most important, durable facts from this file. Each fact should be a standalone memory that would be useful context in future conversations.

Guidelines:
- ${shardGuidance[shard] || shardGuidance.semantic}
- Be specific: include names, numbers, dates when present
- Each fact should make sense without the source document
- Skip temporary info, TODOs, and meta-commentary
- 3-8 facts per document (more for longer files)

Format as JSON array:
[{"trigger": "Short searchable title", "content": "The complete fact with specific details", "shard": "${shard}"}]

Source: ${fileName}
---
${truncate(fileContent)}`;
}

// Fallback: chunk file into paragraphs and encode directly
function chunkEncode(content, fileName, shard) {
  const facts = [];
  // Split by headers or double newlines
  const sections = content.split(/\n##?\s+|\n\n/).filter(s => s.trim().length > 50);
  
  for (const section of sections.slice(0, 10)) {
    const firstLine = section.trim().split('\n')[0].replace(/^[#*\-]+\s*/, '').slice(0, 80);
    facts.push({
      trigger: firstLine || fileName,
      content: section.trim().slice(0, 500),
      shard,
    });
  }
  return facts;
}

// ─── Encoding ────────────────────────────────────────────

async function encodeFact(fact, source) {
  const result = await httpPost(`${BRAINDB_URL}/memory/encode`, {
    event: fact.trigger,
    content: fact.content,
    shard: fact.shard || 'semantic',
    context: { source, migrated: new Date().toISOString() },
    motivationDelta: { serve: 0.3 },
    dedupThreshold: 0.90,
  });
  return result;
}

// ─── Main ────────────────────────────────────────────────

async function main() {
  console.log('🧠 BrainDB Memory Migration');
  console.log('═'.repeat(50));

  // Single file mode
  if (SINGLE_FILE) {
    if (!fs.existsSync(SINGLE_FILE)) {
      console.error(`❌ File not found: ${SINGLE_FILE}`);
      process.exit(1);
    }
    const files = [{
      path: path.resolve(SINGLE_FILE),
      relative: path.basename(SINGLE_FILE),
      shard: 'semantic',
      priority: 1,
      desc: path.basename(SINGLE_FILE),
      type: 'single',
    }];
    return await migrateFiles(files);
  }

  // Discover files
  const wsPath = path.resolve(WORKSPACE);
  console.log(`📂 Workspace: ${wsPath}`);
  
  const files = discoverFiles(wsPath);
  if (files.length === 0) {
    console.log('\n⚠️  No files found to migrate.');
    console.log('Make sure you\'re running this from your OpenClaw workspace directory,');
    console.log('or pass the path: node migrate.js /path/to/workspace');
    process.exit(0);
  }

  // Scan mode: just list files
  if (SCAN_ONLY) {
    console.log(`\n📋 Found ${files.length} files to migrate:\n`);
    for (const f of files) {
      const size = fs.statSync(f.path).size;
      const kb = (size / 1024).toFixed(1);
      console.log(`  ${f.shard.padEnd(11)} ${kb.padStart(6)}KB  ${f.relative}  (${f.desc})`);
    }
    console.log(`\nRun without --scan to migrate these files.`);
    return;
  }

  await migrateFiles(files);
}

async function migrateFiles(files) {
  // Check BrainDB connectivity
  try {
    const health = await httpGet(`${BRAINDB_URL}/health`);
    if (!health?.status) throw new Error('no response');
    console.log(`✅ BrainDB: ${health.status} (${health.totalMemories || 0} existing memories)`);
  } catch (e) {
    console.error(`❌ Can't reach BrainDB at ${BRAINDB_URL}`);
    console.error(`   Make sure BrainDB is running: docker compose up -d`);
    process.exit(1);
  }

  // Check swarm availability
  let useSwarm = USE_SWARM;
  if (useSwarm) {
    try {
      const status = await httpGet(`http://localhost:${SWARM_PORT}/status`);
      if (status && (status.status === 'ok' || status.workers || status.uptime)) {
        const workerCount = status.workers?.totalNodes || status.workers || '?';
        console.log(`✅ Swarm: ${workerCount} workers (⚠️  file contents will be sent to Google Gemini API)`);
      } else throw new Error('not ok');
    } catch {
      console.log('⚠️  Swarm unavailable — falling back to local chunked encoding');
      useSwarm = false;
    }
  } else {
    console.log('📦 Using local chunked encoding (fully local, no external API calls)');
    console.log('   Pass --swarm for smarter extraction via Gemini Flash (sends data to Google API)');
  }

  console.log(`📋 Files to migrate: ${files.length}`);
  if (DRY_RUN) console.log('   (DRY RUN — no encoding)');
  console.log('');

  let totalFacts = 0;
  let totalEncoded = 0;
  let totalDedup = 0;
  let errors = 0;

  if (useSwarm) {
    // Batch extraction via swarm
    for (let i = 0; i < files.length; i += BATCH_SIZE) {
      const batch = files.slice(i, i + BATCH_SIZE);
      const batchNum = Math.floor(i / BATCH_SIZE) + 1;
      const totalBatches = Math.ceil(files.length / BATCH_SIZE);
      console.log(`🐝 Batch ${batchNum}/${totalBatches}`);

      const prompts = batch.map(f => {
        const content = fs.readFileSync(f.path, 'utf8');
        return buildExtractionPrompt(content, f.relative, f.shard);
      });

      let result;
      try {
        result = await httpPost(`http://localhost:${SWARM_PORT}/parallel`, { prompts });
      } catch (e) {
        console.log(`   ❌ Swarm error: ${e.message}`);
        // Fall back to chunked for this batch
        for (const f of batch) {
          const content = fs.readFileSync(f.path, 'utf8');
          const facts = chunkEncode(content, f.relative, f.shard);
          const res = await encodeAll(facts, f.relative, DRY_RUN);
          totalFacts += facts.length;
          totalEncoded += res.encoded;
          totalDedup += res.dedup;
          errors += res.errors;
        }
        continue;
      }

      if (!result?.results) {
        console.log('   ❌ No results from swarm');
        errors += batch.length;
        continue;
      }

      for (let j = 0; j < result.results.length; j++) {
        const raw = result.results[j];
        const file = batch[j];

        if (!raw) {
          console.log(`   ⚠️  ${file.relative}: empty response`);
          errors++;
          continue;
        }

        let facts;
        try {
          const jsonMatch = raw.match(/\[[\s\S]*?\]/);
          if (!jsonMatch) throw new Error('No JSON array');
          facts = JSON.parse(jsonMatch[0]);
        } catch (e) {
          console.log(`   ⚠️  ${file.relative}: parse error, falling back to chunks`);
          const content = fs.readFileSync(file.path, 'utf8');
          facts = chunkEncode(content, file.relative, file.shard);
        }

        const res = await encodeAll(facts, file.relative, DRY_RUN);
        totalFacts += facts.length;
        totalEncoded += res.encoded;
        totalDedup += res.dedup;
        errors += res.errors;
      }

      // Brief pause between batches
      if (!DRY_RUN && i + BATCH_SIZE < files.length) {
        await new Promise(r => setTimeout(r, 500));
      }
    }
  } else {
    // No swarm: chunked encoding
    for (const file of files) {
      const content = fs.readFileSync(file.path, 'utf8');
      const facts = chunkEncode(content, file.relative, file.shard);
      const res = await encodeAll(facts, file.relative, DRY_RUN);
      totalFacts += facts.length;
      totalEncoded += res.encoded;
      totalDedup += res.dedup;
      errors += res.errors;
    }
  }

  // Summary
  console.log('');
  console.log('═'.repeat(50));
  console.log('📊 Migration Complete');
  console.log(`   Files processed: ${files.length}`);
  console.log(`   Facts extracted: ${totalFacts}`);
  console.log(`   Facts encoded:   ${totalEncoded}`);
  console.log(`   Duplicates:      ${totalDedup} (skipped)`);
  console.log(`   Errors:          ${errors}`);
  console.log('═'.repeat(50));

  if (totalEncoded > 0) {
    console.log('\n✅ Your memories are loaded! Test with:');
    console.log(`   curl -s -X POST ${BRAINDB_URL}/memory/recall \\`);
    console.log(`     -H "Content-Type: application/json" \\`);
    console.log(`     -d '{"query":"who am I","limit":3}' | jq '.results[].content'`);
  }
}

async function encodeAll(facts, source, dryRun) {
  let encoded = 0, dedup = 0, errors = 0;
  
  console.log(`   📄 ${source}: ${facts.length} facts`);

  if (dryRun) {
    for (const f of facts) {
      console.log(`      → ${f.trigger}`);
    }
    return { encoded: 0, dedup: 0, errors: 0 };
  }

  for (const fact of facts) {
    try {
      const result = await encodeFact(fact, source);
      if (result?.ok) {
        if (result.deduplicated) {
          dedup++;
        } else {
          encoded++;
        }
      } else {
        errors++;
        if (result?.error) console.log(`      ❌ ${fact.trigger}: ${result.error}`);
      }
    } catch (e) {
      errors++;
    }
  }
  return { encoded, dedup, errors };
}

main().catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});
