# Dropbox KB Auto

**Automatically index your Dropbox into a searchable knowledge base with OCR and Office file support.**

## When to Use This Skill

Use this skill when you want to:
- Automatically index Dropbox documents into OpenClaw's knowledge base
- Search across PDFs, images, Office files using semantic search
- Extract text from scanned documents and images via OCR
- Keep your knowledge base in sync with Dropbox (delta-based, efficient)
- Make historical documents, receipts, research papers searchable

## What This Skill Does

1. Connects to your Dropbox via OAuth (read-only recommended)
2. Monitors specified folders for new/changed files
3. Extracts text from:
   - PDFs (with OCR fallback for scanned docs)
   - Images (JPG, PNG via Tesseract OCR)
   - Office files (Word, Excel, PowerPoint)
   - Text files (TXT, MD, CSV, JSON)
4. Saves extracted content as markdown in `memory/knowledge/dropbox/`
5. OpenClaw automatically generates embeddings for semantic search
6. Uses Dropbox delta API for efficient incremental syncs (only processes changes)

## Prerequisites

### System Dependencies
```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu poppler-utils

# macOS
brew install tesseract tesseract-lang poppler
```

### Python Dependencies
```bash
pip3 install pypdf openpyxl python-pptx python-docx
```

Or run the included setup script:
```bash
bash setup.sh
```

### Dropbox App Setup

1. Create Dropbox app at https://www.dropbox.com/developers/apps
2. Choose **Scoped access** → **Full Dropbox** (or App folder)
3. Add permissions:
   - `files.metadata.read`
   - `files.content.read`
4. Generate refresh token (see Dropbox OAuth 2 docs)
5. Add credentials to `~/.openclaw/.env`:
   ```bash
   DROPBOX_FULL_APP_KEY=your_app_key
   DROPBOX_FULL_APP_SECRET=your_app_secret
   DROPBOX_FULL_REFRESH_TOKEN=your_refresh_token
   ```

## Installation

### Via ClawHub
```bash
clawhub install dropbox-kb-auto
```

### Manual
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/ferreirafabio/dropbox-kb-auto.git
```

## Configuration

Edit `config.json` to customize:
```json
{
  "folders": [
    "/Documents",
    "/Work",
    "/Research"
  ],
  "skip_paths": [
    "/Archive",
    "/Backups"
  ],
  "file_types": ["pdf", "docx", "xlsx", "pptx", "jpg", "png", "txt"],
  "max_file_size_mb": 20
}
```

## Usage

### One-Time Manual Sync
```bash
cd ~/.openclaw/workspace/skills/dropbox-kb-auto
python3 dropbox-sync.py
```

First run: 5-10 minutes (builds delta cursors)  
Subsequent runs: <10 seconds (delta-only)

### Automated Sync (Cron)
```bash
openclaw cron create \
  --name "Dropbox KB Sync" \
  --cron "0 */6 * * *" \
  --tz "Europe/Berlin" \
  --timeout-seconds 14400 \
  --session isolated \
  --message "cd ~/.openclaw/workspace/skills/dropbox-kb-auto && python3 dropbox-sync.py"
```

### Search Indexed Files

Once indexed, ask Karl:
- "Show me my tax documents from 2025"
- "Find my blood test results"
- "Search presentations about machine learning"

OpenClaw's built-in memory system handles embeddings and semantic search automatically.

## How It Works

### Delta-Based Sync
Instead of re-scanning all 650K+ files every time:
1. **First run:** Lists all files, saves a cursor (timestamp)
2. **Next run:** Fetches only files added/modified/deleted since cursor
3. **Result:** 10x-100x faster than full scans

### Text Extraction Pipeline
```
File → Extension check
  ├─ PDF → pypdf → OCR fallback (if pypdf returns <100 chars)
  ├─ DOCX/DOC → python-docx
  ├─ XLSX/XLS → openpyxl (first 5 sheets, 100 rows each)
  ├─ PPTX/PPT → python-pptx (first 30 slides)
  ├─ JPG/PNG → Tesseract OCR (eng+deu)
  └─ TXT/MD/CSV/JSON → UTF-8 decode
    ↓
Save as .md in memory/knowledge/dropbox/
    ↓
OpenClaw auto-generates embeddings (text-embedding-3-small)
```

## Supported File Types

| Type | Extensions | Method |
|------|-----------|--------|
| PDF | `.pdf` | pypdf + OCR fallback |
| Word | `.docx`, `.doc` | python-docx |
| Excel | `.xlsx`, `.xls` | openpyxl |
| PowerPoint | `.pptx`, `.ppt` | python-pptx |
| Images | `.jpg`, `.jpeg`, `.png` | Tesseract OCR |
| Text | `.txt`, `.md`, `.csv`, `.json` | UTF-8 |

## Performance

Tested on 650,000 files (1,840 indexable):
- **First sync:** ~15 min
- **Incremental syncs:** <30 sec
- **Disk usage:** ~45 MB

## Troubleshooting

### Missing Dependencies
```bash
# If pypdf is missing
pip3 install pypdf openpyxl python-pptx python-docx

# If tesseract is missing
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu
```

### Timeout on First Run
Large Dropboxes (500K+ files) may need longer timeout:
```bash
openclaw cron edit <job-id> --timeout-seconds 28800  # 8 hours
```

### Rate Limiting
The script includes retry logic with exponential backoff. If you still hit limits:
- Reduce folder scope in `config.json`
- Add sleep intervals between files

## Files Created

Indexed files are saved in:
```
~/.openclaw/workspace/memory/knowledge/dropbox/
├── 2_dokumente_taxes_2025.pdf.md
├── work_presentation_slides.pptx.md
├── research_paper_analysis.xlsx.md
└── blood_test_results.jpg.md
```

Progress tracked in:
```
~/.openclaw/workspace/memory/
├── dropbox-index-progress.json  # Files already indexed
├── dropbox-cursor.json          # Delta cursors per folder
└── dropbox-indexer.log          # Execution log
```

## Security

- **Read-only recommended** - Use Dropbox app with only read permissions
- **Local processing** - All text extraction happens on your machine
- **No external transmission** - Files never leave Dropbox/your machine
- **Credential safety** - Tokens stored in `~/.openclaw/.env` (gitignored)

## Comparison to Alternatives

| Skill | Auto-Index | OCR | Office Files | Delta Sync | Use Case |
|-------|-----------|-----|--------------|-----------|----------|
| **dropbox-kb-auto** | ✅ | ✅ | ✅ | ✅ | Knowledge base |
| dropbox-api | ❌ | ❌ | ❌ | ❌ | File operations |
| dropbox-integration | ❌ | ❌ | ❌ | ❌ | Manual browsing |

## Examples

### Medical Records
```
Input: Blood test PDFs, doctor's notes (images)
Result: "Show me my cholesterol levels from 2025"
```

### Research Papers
```
Input: Papers folder with 500 PDFs
Result: "Find papers about reinforcement learning published after 2023"
```

### Tax Documents
```
Input: Receipts (images), expense spreadsheets
Result: "List all tax-deductible expenses from Q1 2025"
```

## Contributing

Issues and PRs: https://github.com/ferreirafabio/dropbox-kb-auto

## License

MIT - See LICENSE file

## Author

Fabio Ferreira ([@ferreirafabio](https://github.com/ferreirafabio))
