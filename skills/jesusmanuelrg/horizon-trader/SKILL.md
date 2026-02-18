---
name: horizon-trader
description: Trade prediction markets (Polymarket, Kalshi) - check positions, submit orders, manage risk, discover markets, and compute Kelly-optimal sizing.
emoji: "\U0001F4C8"
metadata:
  openclaw:
    requires:
      env:
        - HORIZON_API_KEY
    primaryEnv: HORIZON_API_KEY
    install:
      - id: pip
        kind: uv
        formula: horizon-sdk
        label: "Horizon SDK (pip install horizon-sdk)"
    homepage: https://docs.openclaw.ai/tools/clawhub
---

# Horizon Trader

You are a prediction market trading assistant powered by the Horizon SDK.

## When to use this skill

Use this skill when the user asks about:
- Checking their **positions**, **PnL**, or **portfolio status**
- **Submitting** or **canceling** orders on prediction markets
- **Discovering** or **searching** for markets or events on Polymarket or Kalshi
- Computing **Kelly-optimal** position sizes
- Managing **risk** controls (kill switch, stop-loss, take-profit)
- Checking **feed** prices or market data
- Looking up **wallet** activity, trades, positions, or profiles on Polymarket
- Analyzing **trade flow** or **top holders** for a market
- Running **Monte Carlo simulations** on portfolio risk
- Executing **cross-exchange arbitrage**
- Anything related to **prediction market trading**

## How to use

Run commands via the CLI script. All output is JSON.

```bash
python3 {baseDir}/scripts/horizon.py <command> [args...]
```

## Available commands

### Portfolio & Status
```bash
# Engine status: PnL, open orders, positions, kill switch, uptime
python3 {baseDir}/scripts/horizon.py status

# List all open positions
python3 {baseDir}/scripts/horizon.py positions

# List open orders (optionally for a specific market)
python3 {baseDir}/scripts/horizon.py orders [market_id]

# List recent fills
python3 {baseDir}/scripts/horizon.py fills
```

### Trading
```bash
# Submit a limit order: quote <market_id> <side> <price> <size>
# side: buy or sell, price: 0-1 (probability)
python3 {baseDir}/scripts/horizon.py quote <market_id> buy 0.55 10

# Cancel a single order
python3 {baseDir}/scripts/horizon.py cancel <order_id>

# Cancel all orders
python3 {baseDir}/scripts/horizon.py cancel-all
```

### Market Discovery
```bash
# Search for markets on an exchange
python3 {baseDir}/scripts/horizon.py discover <exchange> [query] [limit]

# Examples:
python3 {baseDir}/scripts/horizon.py discover polymarket "bitcoin"
python3 {baseDir}/scripts/horizon.py discover kalshi "election" 5
```

### Kelly Sizing
```bash
# Compute optimal position size: kelly <prob> <price> <bankroll> [fraction] [max_size]
python3 {baseDir}/scripts/horizon.py kelly 0.65 0.50 1000
python3 {baseDir}/scripts/horizon.py kelly 0.70 0.55 2000 0.5 50
```

### Risk Management
```bash
# Activate kill switch (emergency stop - cancels all orders)
python3 {baseDir}/scripts/horizon.py kill-switch on "market crash"

# Deactivate kill switch
python3 {baseDir}/scripts/horizon.py kill-switch off
```

### Feed Data & Health
```bash
# Get snapshot for a named feed
python3 {baseDir}/scripts/horizon.py feed <feed_name>

# List all feeds
python3 {baseDir}/scripts/horizon.py feeds

# Check feed staleness and health (optional threshold in seconds, default 30)
python3 {baseDir}/scripts/horizon.py feed-health [threshold]
```

### Contingent Orders
```bash
# List pending stop-loss/take-profit orders
python3 {baseDir}/scripts/horizon.py contingent
```

### Event Discovery
```bash
# Discover multi-outcome events on Polymarket
python3 {baseDir}/scripts/horizon.py discover-events "election"
python3 {baseDir}/scripts/horizon.py discover-events "" 5

# Get top markets by volume
python3 {baseDir}/scripts/horizon.py top-markets polymarket 10
python3 {baseDir}/scripts/horizon.py top-markets kalshi 5 "KXBTC"
```

### Wallet Analytics (Polymarket - no auth required)
```bash
# Trade history for a wallet
python3 {baseDir}/scripts/horizon.py wallet-trades 0x1234... [limit] [condition_id]

# Trade history for a market
python3 {baseDir}/scripts/horizon.py market-trades 0xabc... [limit] [side] [min_size]

# Open positions for a wallet (sort: TOKENS, CURRENT, CASHPNL, PERCENTPNL, etc.)
python3 {baseDir}/scripts/horizon.py wallet-positions 0x1234... 50 CURRENT

# Total portfolio value in USD
python3 {baseDir}/scripts/horizon.py wallet-value 0x1234...

# Public profile (pseudonym, bio, X handle)
python3 {baseDir}/scripts/horizon.py wallet-profile 0x1234...

# Top holders in a market
python3 {baseDir}/scripts/horizon.py top-holders 0xabc... [limit]

# Trade flow analysis (buy/sell volume, net flow, top buyers/sellers)
python3 {baseDir}/scripts/horizon.py market-flow 0xabc... [trade_limit] [top_n]
```

### Monte Carlo Simulation
```bash
# Simulate portfolio risk (uses current engine positions)
python3 {baseDir}/scripts/horizon.py simulate [scenarios] [seed]
python3 {baseDir}/scripts/horizon.py simulate 50000
python3 {baseDir}/scripts/horizon.py simulate 10000 42
```

### Arbitrage
```bash
# Execute atomic cross-exchange arb: arb <market_id> <buy_exchange> <sell_exchange> <buy_price> <sell_price> <size>
python3 {baseDir}/scripts/horizon.py arb will-btc-hit-100k kalshi polymarket 0.48 0.52 10
```

## Pipeline Features (v0.3.0)

The Horizon SDK also includes advanced pipeline components for automated strategies:

- **Regime Detection** (`regime_signal`) - volatility/trend regime classification (0=calm, 1=volatile)
- **Feed Guard** (`feed_guard`) - auto-activates kill switch when feeds go stale
- **Inventory Skew** (`inventory_skewer`) - shifts quotes to reduce position risk
- **Adaptive Spread** (`adaptive_spread`) - dynamically widens/narrows spread based on fill rate, volatility, and order imbalance
- **Execution Tracker** (`execution_tracker`) - monitors fill rate, slippage, and adverse selection
- **Multi-Strategy** - run different pipelines per market via dict config
- **Cross-Market Hedging** (`cross_hedger`) - generates hedge quotes when portfolio delta exceeds threshold

These are Python pipeline functions used with `hz.run()`. See the SDK documentation for usage.

## Output format

All commands return JSON. On success you get the data directly. On error you get `{"error": "message"}`.

## Important notes

- The `quote` command submits **real orders** (or paper orders depending on config). Always confirm with the user before submitting.
- The `kill-switch on` command is an **emergency stop** that cancels all orders immediately.
- Prices are **probabilities** between 0 and 1 (e.g., 0.65 = 65% implied probability).
- The exchange is configured via the `HORIZON_EXCHANGE` environment variable (default: paper).

Full documentation: https://docs.openclaw.ai/tools/clawhub
