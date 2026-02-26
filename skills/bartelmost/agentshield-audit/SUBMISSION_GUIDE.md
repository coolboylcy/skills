# ClawHub Submission Guide - AgentShield v1.2.4

## Submission Steps

### 1. Prepare Bundle

```bash
# Create bundle with all required files
tar -czf agentshield-audit-v1.2.4-clawhub.tar.gz \
  clawhub.json \
  SKILL.md \
  README_CLAWHUB.md \
  INSTALLATION.md \
  src/agentshield_security/
```

### 2. Submit via Web

1. Go to: https://clawhub.ai/submit
2. Upload: `agentshield-audit-v1.2.4-clawhub.tar.gz`
3. Category: "Security"
4. Tags: `security`, `assessment`, `pattern-analysis`, `ai-safety`
5. Click Submit

### 3. Wait for Review

- Review time: 1-3 days
- May receive feedback for adjustments
- Once approved, skill appears in registry

### 4. Test Installation

```bash
clawhub install agentshield-audit
```

---

## Required Files in Bundle

✅ `clawhub.json` - Manifest with metadata
✅ `SKILL.md` - Usage documentation
✅ `README_CLAWHUB.md` - Short description
✅ `INSTALLATION.md` - Setup instructions
✅ `src/agentshield_security/` - Python modules

---

**Contact**: GitHub Issues @ bartelmost/agentshield
