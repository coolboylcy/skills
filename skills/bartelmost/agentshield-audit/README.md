# AgentShield - Security Assessment for AI Agents

🔒 Automated pattern analysis and security assessment for AI agents.

**Status:** v1.2.4 - Production Ready
**Live:** https://agentshield-api-bartel-fe94823ceeea.herokuapp.com
**Website:** https://agentshield.live

## ⚠️ Important: What This Tool Does

AgentShield performs **static pattern analysis** on:
- ✅ System prompts (looking for vulnerability patterns)
- ✅ Agent code (detecting security risks)
- ✅ Token efficiency (optimizing costs)

**It does NOT perform:**
- ❌ Live penetration testing (simulated with real subagents in skill)
- ❌ Dynamic execution of attack code
- ❌ Runtime security monitoring

Think of it as: "A security linter for AI agents" - not a full penetration test.

## Products

### 💰 Token Optimizer (Active)
- Analyzes prompt efficiency
- Suggests optimizations
- Cost: Free during beta (use code BETA5)

### 🔍 Code Security Scan (Active)
- Pattern-based vulnerability detection
- Supports Python, JavaScript
- Cost: $0.10 per scan

### 🛡️ Agent Audit (Active)
- Generates security certificates
- Ed25519 cryptographic identity
- Cost: $2.50 per audit

### 🧪 Live Security Test (Skill Only)
- Real subagent testing with jailbreak attempts
- Requires local OpenClaw installation
- See SKILL.md for details

## Installation

```bash
# ClawHub (for local testing)
clawhub install agentshield-audit

# Python API
pip install requests
curl -X POST https://agentshield-api-bartel-fe94823ceeea.herokuapp.com/api/code-scan \
  -H "Content-Type: application/json" \
  -d '{"code": "your code here", "promo_code": "BETA5"}'
```

## Documentation

- [Full API Documentation](docs/API.md)
- [Usage Examples](examples/)
- [Changelog](CHANGELOG.md)

## License
MIT
