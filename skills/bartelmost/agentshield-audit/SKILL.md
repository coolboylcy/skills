# AgentShield Audit Skill

Security assessment tool for AI agents. Performs static pattern analysis to identify vulnerabilities in system prompts and agent code.

## Installation

```bash
clawhub install agentshield-audit
```

## Usage

### Basic Audit (Pattern Scan)

```bash
# Scan a local agent configuration
agentshield-audit scan --prompt "Your system prompt here"

# Scan code for vulnerabilities
agentshield-audit scan --code-file ./agent.py

# Full audit with certificate
agentshield-audit audit --prompt-file ./prompt.txt --code-file ./agent.py
```

### Live Testing (Real Subagents)

To test with real subagents and actual attack attempts:

```bash
python scripts/demo_real_integration.py
```

This spawns real OpenClaw subagents and costs ~$0.01-0.10 per test.

## ⚠️ Important Limitations

This skill performs **static pattern analysis**, not live penetration testing:

### What It Does
- ✅ Scans your agent's code and prompts for known vulnerability patterns
- ✅ Identifies potential security risks through signature matching
- ✅ Runs locally on your machine (no data sent to external services)
- ✅ Generates PDF reports for documentation

### What It Does NOT Do
- ❌ Execute real jailbreak attacks against running agents
- ❌ Test actual runtime behavior
- ❌ Guarantee security (patterns can miss novel attacks)

### Comparison

| Feature | Pattern Scan | Live Test |
|---------|-------------|-----------|
| Method | Static analysis | Real agent interaction |
| Cost | Free | ~$0.01-0.10 |
| Speed | Instant | 10-60 seconds |
| Coverage | Known patterns | Actual attack vectors |
| Best For | CI/CD, quick checks | Security validation |

## API Integration

```python
import requests

# Code scan
response = requests.post(
    'https://agentshield-api-bartel-fe94823ceeea.herokuapp.com/api/code-scan',
    json={'code': 'your code here', 'promo_code': 'BETA5'}
)
print(response.json())
```

## Certificate Verification

AgentShield issues Ed25519-based certificates for verified agents:

```bash
# Verify a certificate
agentshield-audit verify --certificate ./agent_certificate.json
```

## Privacy

- Private keys stored locally in `~/.openclaw/workspace/.agentshield/`
- API calls use public endpoints only
- No agent code or prompts leave your machine during local scans

## Support

- Documentation: https://agentshield.live/docs
- Source: https://github.com/bartelmost/agentshield
- Issues: https://github.com/bartelmost/agentshield/issues
