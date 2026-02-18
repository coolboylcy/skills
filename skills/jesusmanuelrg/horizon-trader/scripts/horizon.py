#!/usr/bin/env python3
"""OpenClaw CLI entry point for Horizon SDK.

Usage: python3 horizon.py <command> [args...]

All output is JSON printed to stdout.
"""

from __future__ import annotations

import json
import os
import sys

# Remove this script's directory from sys.path to prevent self-shadowing
# (this file is named horizon.py, which would shadow the horizon package).
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p) != _script_dir]


def _print(data: object) -> None:
    print(json.dumps(data, indent=2))


def main() -> None:
    args = sys.argv[1:]
    if not args:
        _print({"error": "no command. try: status, positions, orders, fills, quote, cancel, cancel-all, discover, discover-events, top-markets, kelly, kill-switch, feed, feeds, feed-health, contingent, wallet-trades, market-trades, wallet-positions, wallet-value, wallet-profile, top-holders, market-flow, simulate, arb"})
        sys.exit(1)

    cmd = args[0]

    from horizon import tools

    if cmd == "status":
        _print(tools.engine_status())

    elif cmd == "positions":
        _print(tools.list_positions())

    elif cmd == "orders":
        market_id = args[1] if len(args) > 1 else None
        _print(tools.list_open_orders(market_id))

    elif cmd == "fills":
        limit = int(args[1]) if len(args) > 1 else 20
        _print(tools.list_recent_fills(limit))

    elif cmd == "quote":
        if len(args) < 5:
            _print({"error": "usage: quote <market_id> <side> <price> <size>"})
            sys.exit(1)
        _print(tools.submit_order(args[1], args[2], float(args[3]), float(args[4])))

    elif cmd == "cancel":
        if len(args) < 2:
            _print({"error": "usage: cancel <order_id>"})
            sys.exit(1)
        _print(tools.cancel_order(args[1]))

    elif cmd == "cancel-all":
        _print(tools.cancel_all_orders())

    elif cmd == "cancel-market":
        if len(args) < 2:
            _print({"error": "usage: cancel-market <market_id>"})
            sys.exit(1)
        _print(tools.cancel_market_orders(args[1]))

    elif cmd == "discover":
        exchange = args[1] if len(args) > 1 else "polymarket"
        query = args[2] if len(args) > 2 else ""
        limit = int(args[3]) if len(args) > 3 else 10
        _print(tools.discover(exchange, query, limit))

    elif cmd == "kelly":
        if len(args) < 4:
            _print({"error": "usage: kelly <prob> <price> <bankroll> [fraction] [max_size]"})
            sys.exit(1)
        prob = float(args[1])
        price = float(args[2])
        bankroll = float(args[3])
        fraction = float(args[4]) if len(args) > 4 else 0.25
        max_size = float(args[5]) if len(args) > 5 else 100.0
        _print(tools.kelly_sizing(prob, price, bankroll, fraction, max_size))

    elif cmd == "kill-switch":
        if len(args) < 2:
            _print({"error": "usage: kill-switch <on|off> [reason]"})
            sys.exit(1)
        if args[1] == "on":
            reason = args[2] if len(args) > 2 else "manual"
            _print(tools.activate_kill_switch(reason))
        elif args[1] == "off":
            _print(tools.deactivate_kill_switch())
        else:
            _print({"error": "usage: kill-switch <on|off> [reason]"})
            sys.exit(1)

    elif cmd == "feed":
        if len(args) < 2:
            _print({"error": "usage: feed <name>"})
            sys.exit(1)
        _print(tools.get_feed_snapshot(args[1]))

    elif cmd == "feeds":
        _print(tools.list_all_feeds())

    elif cmd == "parity":
        if len(args) < 2:
            _print({"error": "usage: parity <market_id>"})
            sys.exit(1)
        _print(tools.check_parity(args[1]))

    elif cmd == "contingent":
        _print(tools.list_contingent_orders())

    # --- Feed health ---

    elif cmd == "feed-health":
        threshold = float(args[1]) if len(args) > 1 else 30.0
        _print(tools.check_feed_health(threshold))

    # --- Discovery ---

    elif cmd == "discover-events":
        query = args[1] if len(args) > 1 else ""
        limit = int(args[2]) if len(args) > 2 else 10
        _print(tools.discover_event(query, limit))

    elif cmd == "top-markets":
        exchange = args[1] if len(args) > 1 else "polymarket"
        limit = int(args[2]) if len(args) > 2 else 10
        category = args[3] if len(args) > 3 else ""
        _print(tools.get_top_markets(exchange, limit, category))

    # --- Wallet analytics (Polymarket, no auth) ---

    elif cmd == "wallet-trades":
        if len(args) < 2:
            _print({"error": "usage: wallet-trades <address> [limit] [condition_id]"})
            sys.exit(1)
        address = args[1]
        limit = int(args[2]) if len(args) > 2 else 50
        cid = args[3] if len(args) > 3 else None
        _print(tools.wallet_trades(address, limit, cid))

    elif cmd == "market-trades":
        if len(args) < 2:
            _print({"error": "usage: market-trades <condition_id> [limit] [side] [min_size]"})
            sys.exit(1)
        cid = args[1]
        limit = int(args[2]) if len(args) > 2 else 50
        side = args[3] if len(args) > 3 else None
        min_size = float(args[4]) if len(args) > 4 else 0.0
        _print(tools.market_trades(cid, limit, side, min_size))

    elif cmd == "wallet-positions":
        if len(args) < 2:
            _print({"error": "usage: wallet-positions <address> [limit] [sort_by]"})
            sys.exit(1)
        address = args[1]
        limit = int(args[2]) if len(args) > 2 else 50
        sort_by = args[3] if len(args) > 3 else "CURRENT"
        _print(tools.wallet_positions(address, limit, sort_by))

    elif cmd == "wallet-value":
        if len(args) < 2:
            _print({"error": "usage: wallet-value <address>"})
            sys.exit(1)
        _print(tools.wallet_value(args[1]))

    elif cmd == "wallet-profile":
        if len(args) < 2:
            _print({"error": "usage: wallet-profile <address>"})
            sys.exit(1)
        _print(tools.wallet_profile(args[1]))

    elif cmd == "top-holders":
        if len(args) < 2:
            _print({"error": "usage: top-holders <condition_id> [limit]"})
            sys.exit(1)
        cid = args[1]
        limit = int(args[2]) if len(args) > 2 else 20
        _print(tools.market_top_holders(cid, limit))

    elif cmd == "market-flow":
        if len(args) < 2:
            _print({"error": "usage: market-flow <condition_id> [trade_limit] [top_n]"})
            sys.exit(1)
        cid = args[1]
        trade_limit = int(args[2]) if len(args) > 2 else 500
        top_n = int(args[3]) if len(args) > 3 else 10
        _print(tools.market_flow(cid, trade_limit, top_n))

    # --- Simulation ---

    elif cmd == "simulate":
        scenarios = int(args[1]) if len(args) > 1 else 10000
        seed = int(args[2]) if len(args) > 2 else None
        _print(tools.simulate_portfolio(scenarios, seed))

    # --- Arbitrage ---

    elif cmd == "arb":
        if len(args) < 7:
            _print({"error": "usage: arb <market_id> <buy_exchange> <sell_exchange> <buy_price> <sell_price> <size>"})
            sys.exit(1)
        _print(tools.execute_arb(
            args[1], args[2], args[3],
            float(args[4]), float(args[5]), float(args[6]),
        ))

    else:
        _print({"error": f"unknown command: {cmd}"})
        sys.exit(1)


if __name__ == "__main__":
    main()
