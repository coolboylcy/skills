# TruthSea Verifier

Verify claims, submit truth quanta, and earn TRUTH tokens through on-chain epistemological scoring on Base L2.

## Setup

This skill requires the `truthsea-mcp-server` MCP server. It will be configured automatically when installed.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEPLOYER_PRIVATE_KEY` | For write ops | Your wallet private key. Without it, the server runs in read-only mode. |
| `TRUTHSEA_NETWORK` | No | Network to use. Default: `base_sepolia` |

## Tools

### Truth Verification

- **`truthsea_submit_quantum`** — Submit a new truth quantum with a claim, 4-pillar truth scores, and 8-dimensional moral vector. Requires wallet.
- **`truthsea_verify_quantum`** — Submit verification scores for an existing quantum. Requires wallet.
- **`truthsea_query`** — Query and search quanta by discipline, score threshold, or claim text. Read-only.
- **`truthsea_dispute`** — Challenge a quantum with counter-evidence. Creates a fork and slashes the original host. Requires wallet.

### Bounty Bridge

- **`crowdedsea_list_bounties`** — List bounties filtered by status, discipline, and minimum reward. Read-only.
- **`crowdedsea_claim_bounty`** — Claim a bounty for investigation. Requires wallet.

## Scoring System

### Truth Frameworks (0-100 each)

1. **Correspondence** — Maps to observable reality
2. **Coherence** — Fits the web of known truths
3. **Convergence** — Independent sources agree over time
4. **Pragmatism** — Works in practice

### Moral Vector (-100 to +100 each)

1. **Care** ↔ Harm
2. **Fairness** ↔ Cheating
3. **Loyalty** ↔ Betrayal
4. **Authority** ↔ Subversion
5. **Sanctity** ↔ Degradation
6. **Liberty** ↔ Oppression
7. **Epistemic Humility** ↔ Dogmatism
8. **Temporal Stewardship** ↔ Short-term Extraction

## Commands

| Command | Description |
|---------|-------------|
| `/verify <claim>` | Submit a claim for multi-dimensional truth verification |
| `/bounty list` | List available truth bounties with ETH rewards |
| `/bounty claim <id>` | Claim a bounty for investigation |
| `/truth query <search>` | Search verified truth quanta |
| `/dispute <id> <claim>` | Challenge a quantum with counter-evidence |

## Contracts (Base Sepolia)

- **TruthToken**: `0x18D825cE88089beFC99B0e293f39318D992FA07D`
- **TruthRegistryV2**: `0xbEE32455c12002b32bE654c8E70E876Fd557d653`
- **BountyBridge**: `0xA255A98F2D497c47a7068c4D1ad1C1968f88E0C5`

## Links

- [GitHub](https://github.com/turfptax/TruthSea)
- [Website](https://truthsea.io)
- [API Docs](https://truthsea.io/api/v1)
- [Contracts on Basescan](https://sepolia.basescan.org/address/0xbEE32455c12002b32bE654c8E70E876Fd557d653)
