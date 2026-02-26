# Installation Guide

## Method 1: ClawHub (Recommended)

```bash
clawhub install agentshield-audit
```

## Method 2: Manual Install

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/bartelmost/agentshield.git agentshield-audit
cd agentshield-audit
pip install -r requirements.txt
```

## Verification

```bash
python -c "from agentshield_security import run_quick_test; print('✓ Installation successful')"
```

## First Run

```bash
python scripts/initiate_audit.py --auto --yes
```
