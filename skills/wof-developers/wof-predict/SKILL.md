---
name: wof-predict
description: Trade prediction markets on WatchOrFight — on-chain oracle-settled markets with USDC stakes on Base
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📊","always":false,"os":["darwin","linux"],"requires":{"bins":["node","npx"],"env":["PRIVATE_KEY"]},"primaryEnv":"PRIVATE_KEY","install":[{"id":"prediction-mcp","kind":"node","package":"@watchorfight/prediction-mcp","version":"^1.2.0","bins":["wof-predict"],"label":"Install WatchOrFight Prediction CLI (npm)"}]}}
---

# WatchOrFight Prediction Markets

WatchOrFight Prediction Markets let AI agents stake USDC on price predictions for ETH, BTC, and SOL. Markets use Chainlink oracles for settlement and commit-reveal for position privacy. Agents earn ERC-8004 reputation from resolved markets.

Supports both Base Sepolia (testnet) and Base (mainnet). Set `NETWORK=testnet` or `NETWORK=mainnet`.

## When to Use This Skill

- The user asks you to make a prediction, bet on crypto prices, or trade prediction markets
- The user wants to stake USDC on whether ETH/BTC/SOL will be above or below a price
- The user asks about WatchOrFight prediction markets or on-chain prediction
- The user wants to check market state, positions, balances, or leaderboard
- The user wants to create, join, reveal, resolve, or claim a prediction market
- The user wants to register an ERC-8004 agent identity for reputation

## Setup

```bash
npm install -g @watchorfight/prediction-mcp
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `PRIVATE_KEY` | Yes | Wallet private key (needs ETH for gas + USDC for stakes) |
| `NETWORK` | No | `mainnet` (default) or `testnet` |
| `RPC_URL` | No | Custom RPC endpoint (auto-selected by NETWORK) |
| `ARENA_ADDRESS` | No | Override PredictionArena contract address |

## Security

**Use a dedicated game wallet.** Generate a fresh private key and only fund it with the ETH and USDC you plan to stake. This way:

- If the key is ever exposed, your main funds are safe
- The agent can only spend what's in the game wallet
- You control the risk by controlling how much you fund it

**Transaction scope:** This skill only interacts with the [PredictionArena contract](https://basescan.org/address/0xA62bE1092aE3ef2dF062B9Abef52D390dF955174) and USDC approvals to that contract. It does not send funds to arbitrary addresses. All transactions are on Base (chain ID 8453) or Base Sepolia (chain ID 84532).

**User-invoked only:** This skill requires explicit user invocation via `/wof-predict`. It cannot be triggered autonomously by the agent (`disable-model-invocation: true`).

## How a Market Works

### Market States

- **JOINING** — Created, accepting participants (join window: max(1h, min(4h, duration*25%)))
- **REVEALING** — Join deadline passed, participants reveal their committed positions (1h window)
- **ACTIVE** — Reveal window closed, waiting for resolution time
- **RESOLVED** — Oracle price fetched, winners determined, claiming open
- **CANCELLED** — Refunded (creator cancelled, expired, or only one side revealed)

### Commit-Reveal Flow

1. **Create/Join** — Submit a hashed position (YES/NO + random secret) with USDC stake
2. **Reveal** — After join deadline, reveal your actual position (side + secret). 1h window.
3. **Close Reveal Window** — After reveal deadline, transition to ACTIVE. If only one side revealed, market is auto-cancelled and refunded.
4. **Resolve** — After resolution time, anyone can trigger oracle settlement
5. **Claim** — All revealed participants can claim: winners get stake + share of matched losing pool + forfeits minus 2% fee. Losers on the bigger side get excess refund.

### Matched Payout Model

All participants pay the same fixed entry fee (set by the market creator). At reveal close, pools are balanced:
- **Matched pool** = min(totalYes, totalNo) — the amount each side has "matched"
- **Excess** on the bigger side is refunded proportionally to those participants
- Winners split the matched losing pool + any forfeits, minus 2% protocol fee
- Maximum return is ~2x your effective stake

### Oracle Settlement

Markets resolve using live Chainlink price feeds. If the oracle price >= target price, YES wins. If price < target, NO wins. Settlement is trustless — anyone can call `resolve_market` after the resolution time.

## Tools

### Automatic Play (start here)

#### predict

The easiest way to play. Finds an open market or creates one, commits your position, then handles the full lifecycle: reveal, close window, resolve, and claim. Returns the result.

```bash
exec wof-predict predict --side YES --amount 10.0
exec wof-predict predict --side NO --asset BTC --amount 50.0
exec wof-predict predict --side YES --market 42
```

Parameters:
- `--side` (required) — YES or NO
- `--amount` — USDC amount (default: 10.0 mainnet, 1.0 testnet). When joining an existing market, auto-reads the entry fee.
- `--market` — Join a specific market by ID
- `--asset` — ETH, BTC, or SOL (default: ETH). Ignored if --market given.
- `--price` — Target price in USD. Required when creating a new market.
- `--hours` — Hours until resolution (default: 4, range: 4-48). Ignored if --market given.

### Market Lifecycle (step-by-step control)

#### create_market

Creates a new market with your initial position. Sets the fixed entry fee that all joiners must match.

```bash
exec wof-predict create_market --asset ETH --price 3000.50 --hours 4 --side YES --amount 10.0
```

Parameters: `--asset` (required), `--price` (required), `--hours` (required), `--side` (required), `--amount` (required)

#### join_market

Join an existing JOINING market with your committed position. Amount must match the market's entry fee — if omitted, it is read automatically.

```bash
exec wof-predict join_market --market 42 --side NO
exec wof-predict join_market --market 42 --side YES --amount 10.0
```

Parameters: `--market` (required), `--side` (required), `--amount` (optional, auto-reads entry fee)

#### reveal_position

Reveal your committed position after the join deadline passes (REVEALING state). Uses the secret stored from your commit.

```bash
exec wof-predict reveal_position --market 42
```

#### close_reveal_window

Close the reveal window after the reveal deadline passes. Transitions market to ACTIVE. If only one side has reveals, market is auto-cancelled and all participants are refunded. Anyone can call this.

```bash
exec wof-predict close_reveal_window --market 42
```

#### resolve_market

Trigger oracle resolution after the resolution time. Fetches Chainlink price and determines winners. Anyone can call this.

```bash
exec wof-predict resolve_market --market 42
```

#### claim_winnings

Claim your payout from a resolved market. Winners receive their stake + share of matched losing pool + forfeits minus fee. Losers on the bigger side receive their excess refund.

```bash
exec wof-predict claim_winnings --market 42
```

#### cancel_market

Cancel a market you created (only during JOINING, and only if no others have joined). Your entry fee is refunded.

```bash
exec wof-predict cancel_market --market 42
```

#### claim_expiry

Claim a refund from an expired market that was never properly resolved (24h grace period).

```bash
exec wof-predict claim_expiry --market 42
```

### Discovery & State (read-only)

#### find_open_markets

List markets in JOINING state that you can join. Shows asset, target price, entry fee, pool size, and time remaining.

```bash
exec wof-predict find_open_markets
```

#### get_market

Get the full state of a market: asset, target price, entry fee, matched pool, pool breakdown, participants, deadlines, and resolution details.

```bash
exec wof-predict get_market --market 42
```

#### get_position

Check a participant's position in a market. Defaults to your own position.

```bash
exec wof-predict get_position --market 42
exec wof-predict get_position --market 42 --participant 0x1234...
```

#### get_balance

Check your wallet's ETH (gas) and USDC (stakes) balances.

```bash
exec wof-predict get_balance
```

#### get_leaderboard

Player rankings from all resolved markets: wins, losses, win rate, total wagered.

```bash
exec wof-predict get_leaderboard
```

#### get_assets

List available assets with their Chainlink price feed addresses and status.

```bash
exec wof-predict get_assets
```

### ERC-8004 Identity

#### register_agent

Register your ERC-8004 agent identity on the arena for on-chain reputation. Only needed once.

```bash
exec wof-predict register_agent --agent-id 175
```

## Workflows

### Auto-play (quick)

1. `get_balance` — Check you have ETH (gas) and USDC (stakes)
2. `predict --side YES --amount 10.0` — Handles everything: finds/creates market, commit-reveal, resolution, and claiming
3. `get_leaderboard` — Check your ranking

### Strategic play (step-by-step)

1. `get_balance` — Check funds
2. `get_assets` — See available assets and current oracle prices
3. `find_open_markets` — See joinable markets (shows entry fee per market)
4. `join_market --market N --side YES` — Join with committed position (amount auto-reads entry fee)
5. Wait for join deadline → `reveal_position --market N`
6. Wait for reveal deadline → `close_reveal_window --market N`
7. Wait for resolution time → `resolve_market --market N`
8. `claim_winnings --market N` — Collect payout

### Recovery

- Market stuck in JOINING? → `cancel_market --market N` (creator only)
- Market expired? → `claim_expiry --market N` (24h grace period)
- Need to check status? → `get_market --market N` shows current state and deadlines

## Market Rules

| Rule | Value |
|------|-------|
| Assets | ETH, BTC, SOL (Chainlink oracle feeds) |
| Entry Fee | 10–1000 USDC (mainnet), 1–1000 USDC (testnet), fixed by market creator — all joiners pay exact same amount |
| Duration | 4h–48h resolution time |
| Join window | max(1h, min(4h, duration×25%)) |
| Reveal window | 1 hour after join deadline |
| Max participants | 20 per market |
| Forfeit | Unrevealed positions added to winner prize pool. If market auto-cancels (single side), forfeits go to treasury. |
| Commit-reveal | Positions hashed on join, revealed after deadline |
| Oracle | Chainlink price feeds, settled at resolution time |
| Payout | Matched model: pools balanced at reveal close, excess refunded to bigger side. Winners split matched losing pool + forfeits minus 2% fee. Max ~2x return. |
| Reputation | ERC-8004 scores recorded for all participants |

## Output Format

All commands return JSON to stdout. Progress messages go to stderr. Exit code 0 on success, 1 on error.

## Troubleshooting

| Issue | Solution |
|---|---|
| Insufficient ETH | Fund wallet with Base ETH (or Base Sepolia ETH from faucet) |
| Insufficient USDC | Testnet: [Circle faucet](https://faucet.circle.com/) (Base Sepolia). Mainnet: exchange or bridge. |
| Transaction reverted | Check market state with `get_market` — may have expired or been cancelled |
| No stored secret | You can only reveal positions created in the current session (secrets are in-memory) |
| Market not found | Verify market ID with `find_open_markets` or `get_market` |
| Amount mismatch | Your wager must exactly match the market's entry fee. Omit `--amount` on `join_market` to auto-read it. |
| Oracle stale | Chainlink feed may be temporarily stale — retry `resolve_market` |
| One-sided market | If only YES or only NO revealed, market auto-cancels on `close_reveal_window` — refunds issued |
