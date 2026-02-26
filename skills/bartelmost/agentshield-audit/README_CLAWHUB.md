# AgentShield Audit v1.2.4

## 🔍 Pattern-Based Security Assessment for AI Agents

AgentShield performs **static pattern analysis** on AI agent configurations to identify potential security risks and optimization opportunities.

### What It Does ✅
- **Token Optimizer**: Reduce LLM costs by 35-60% (Free with BETA5)
- **Code Security Scan**: Pattern-based vulnerability detection ($0.10)
- **Agent Audit**: Generate security certificates ($2.50)
- **Live Testing**: Real subagent tests via local OpenClaw ($0.01-0.10)

### What It Does NOT Do ❌
- Live penetration testing via API (moved to skill-only)
- Runtime security monitoring
- Guaranteed protection against novel attacks

---

## Installation

```bash
clawhub install agentshield-audit
```

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/agentshield-audit
python scripts/initiate_audit.py --auto
```

## Requirements

- Python 3.8+
- OpenClaw CLI
- cryptography library (auto-installed)

## Privacy

- Private keys stored locally (`~/.openclaw/workspace/.agentshield/`)
- No external API keys required
- Pattern analysis happens locally

---

**License**: MIT
**Author**: @bartelmost
