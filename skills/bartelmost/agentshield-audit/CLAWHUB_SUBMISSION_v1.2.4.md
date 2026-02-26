# ClawHub Registry Submission Guide v1.2.4

## Submission Form Data

### Basic Information
| Field | Value |
|-------|-------|
| **Name** | `agentshield-audit` |
| **Version** | `1.2.4` |
| **Author** | `bartelmost` |
| **License** | `MIT` |
| **Category** | `Security` |

### Description

**Short Description (max 120 chars):**
```
Security assessment tool for AI agents. Performs static pattern analysis to identify vulnerabilities in prompts and code.
```

**Long Description:**
```
AgentShield analyzes AI agent configurations for security risks through pattern matching. It checks for common vulnerabilities in system prompts, agent code, and provides optimization recommendations. Includes certificate generation for agent identity verification.

Important: This tool performs static pattern analysis - think of it as a security linter, not a full penetration test. For live testing with real subagents, use the --local flag.
```

### Keywords
```
security, audit, agents, protection, ai-safety, pattern-analysis, vulnerability-detection, certificates
```

### Repository
```
https://github.com/bartelmost/agentshield
```

### Homepage
```
https://agentshield.live
```

### Min OpenClaw Version
```
2026.2.0
```

---

## Installation Configuration

### Install Mode
```json
{
  "mode": "bundle"
}
```

### Scripts
```json
{
  "scripts": {
    "initiate_audit": "python scripts/initiate_audit.py --auto",
    "run_live_test": "python scripts/demo_real_integration.py --local"
  }
}
```

### Triggers (Natural Language)
```json
[
  "audit agent security",
  "security assessment",
  "check agent vulnerabilities",
  "get security certificate",
  "verify agent"
]
```

### Environment Variables
```json
{
  "envVars": {
    "AGENTSHIELD_API_KEY": {
      "description": "API key for AgentShield (optional for basic usage)",
      "required": false
    }
  }
}
```

### Privacy Statement
```
Private keys stored locally in ~/.openclaw/workspace/.agentshield/. API calls use public endpoints only. Pattern scans run entirely locally.
```

### Support Links
```json
{
  "support": {
    "docs": "https://agentshield.live/docs",
    "source": "https://github.com/bartelmost/agentshield",
    "issues": "https://github.com/bartelmost/agentshield/issues"
  }
}
```

---

## Full JSON Manifest

**File:** `clawhub.json`

```json
{
  "name": "agentshield-audit",
  "version": "1.2.4",
  "description": "Security assessment tool for AI agents. Performs static pattern analysis to identify vulnerabilities in prompts and code.",
  "longDescription": "AgentShield analyzes AI agent configurations for security risks through pattern matching. It checks for common vulnerabilities in system prompts, agent code, and provides optimization recommendations. Includes certificate generation for agent identity verification.",
  "author": "bartelmost",
  "license": "MIT",
  "keywords": ["security", "audit", "agents", "protection", "ai-safety", "pattern-analysis"],
  "categories": ["Security"],
  "minOpenClawVersion": "2026.2.0",
  "install": {
    "mode": "bundle"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/bartelmost/agentshield"
  },
  "homepage": "https://agentshield.live",
  "bugs": "https://github.com/bartelmost/agentshield/issues",
  "scripts": {
    "initiate_audit": "python scripts/initiate_audit.py --auto",
    "run_live_test": "python scripts/demo_real_integration.py --local"
  },
  "triggers": [
    "audit agent security",
    "security assessment",
    "check agent vulnerabilities",
    "get security certificate",
    "verify agent"
  ],
  "envVars": {
    "AGENTSHIELD_API_KEY": {
      "description": "API key for AgentShield (optional for basic usage)",
      "required": false
    }
  },
  "privacy": "Private keys stored locally in ~/.openclaw/workspace/.agentshield/. API calls use public endpoints only.",
  "support": {
    "docs": "https://agentshield.live/docs",
    "source": "https://github.com/bartelmost/agentshield",
    "issues": "https://github.com/bartelmost/agentshield/issues"
  }
}
```

---

## Submission Steps

### Step 1: Prepare the Bundle
```bash
# Create submission directory
mkdir -p agentshield-audit-1.2.4
cp clawhub.json agentshield-audit-1.2.4/
cp -r scripts/ agentshield-audit-1.2.4/
cp -r skill/ agentshield-audit-1.2.4/
cp README.md agentshield-audit-1.2.4/
cp SKILL.md agentshield-audit-1.2.4/

# Create archive
tar -czf agentshield-audit-1.2.4.tar.gz agentshield-audit-1.2.4/
```

### Step 2: Submit via ClawHub

1. Open OpenClaw ClawHub interface
2. Navigate to "Submit New Skill"
3. Upload `agentshield-audit-1.2.4.tar.gz`
4. Or paste the JSON manifest directly
5. Fill in required fields using data above
6. Submit for review

### Step 3: Verification

After submission:
- Skill should appear in registry within 24-48h
- Test installation: `clawhub install agentshield-audit`
- Verify version: `clawhub list | grep agentshield`

---

## Important Notes for Reviewers

### What This Skill Actually Does
⚠️ **Static Pattern Analysis Only**

This skill scans code and prompts for known vulnerability patterns. It does NOT:
- Execute live penetration tests (that's in a separate script requiring local OpenClaw)
- Run actual attack code
- Monitor runtime security

Users must run `demo_real_integration.py` separately for live testing with real subagents.

### Cost Transparency
- Pattern scan: Free (runs locally)
- Live test: ~$0.01-0.10 per test (spawns real subagents)
- This is clearly documented in SKILL.md

---

## Contact Information

- **GitHub:** https://github.com/bartelmost/agentshield
- **Website:** https://agentshield.live
- **Issues:** https://github.com/bartelmost/agentshield/issues
- **Email:** (add if available)
