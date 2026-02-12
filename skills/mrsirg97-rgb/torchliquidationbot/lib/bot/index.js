#!/usr/bin/env node
"use strict";
/**
 * torch-lending-monitor — read-only lending market scanner.
 *
 * displays lending parameters for tokens on Torch Market.
 * no wallet required. no signing. no state changes.
 *
 * usage:
 *   # show all migrated tokens with lending
 *   RPC_URL=<rpc> npx tsx src/index.ts
 *
 *   # show lending info for one token
 *   MINT=<mint> RPC_URL=<rpc> npx tsx src/index.ts
 */
Object.defineProperty(exports, "__esModule", { value: true });
const web3_js_1 = require("@solana/web3.js");
const torchsdk_1 = require("torchsdk");
const config_1 = require("./config");
const utils_1 = require("./utils");
// ---------------------------------------------------------------------------
// read-only info display
// ---------------------------------------------------------------------------
async function showLendingInfo(connection, mint) {
    const token = await (0, torchsdk_1.getToken)(connection, mint);
    const lending = await (0, torchsdk_1.getLendingInfo)(connection, mint);
    console.log(`\n=== lending info: ${token.name} (${token.symbol}) ===`);
    console.log(`status:                ${token.status}`);
    console.log(`token price:           ${(0, utils_1.sol)(token.price_sol)} SOL`);
    console.log(`interest rate:         ${(0, utils_1.bpsToPercent)(lending.interest_rate_bps)}`);
    console.log(`max LTV:               ${(0, utils_1.bpsToPercent)(lending.max_ltv_bps)}`);
    console.log(`liquidation threshold: ${(0, utils_1.bpsToPercent)(lending.liquidation_threshold_bps)}`);
    console.log(`liquidation bonus:     ${(0, utils_1.bpsToPercent)(lending.liquidation_bonus_bps)}`);
    console.log(`treasury SOL avail:    ${(0, utils_1.sol)(lending.treasury_sol_available)} SOL`);
    console.log(`total SOL lent:        ${lending.total_sol_lent ? (0, utils_1.sol)(lending.total_sol_lent) : (0, utils_1.sol)(0)} SOL`);
    console.log(`active loans:          ${lending.active_loans}`);
}
async function showAllLending(connection) {
    console.log('=== torch lending monitor ===\n');
    console.log('no MINT specified — showing all migrated tokens with lending\n');
    const { tokens } = await (0, torchsdk_1.getTokens)(connection, {
        status: 'migrated',
        sort: 'volume',
        limit: 10,
    });
    for (const t of tokens) {
        try {
            const lending = await (0, torchsdk_1.getLendingInfo)(connection, t.mint);
            console.log(`${t.symbol.padEnd(10)} | ` +
                `rate: ${(0, utils_1.bpsToPercent)(lending.interest_rate_bps).padEnd(7)} | ` +
                `loans: ${String(lending.active_loans).padEnd(4)} | ` +
                `avail: ${(0, utils_1.sol)(lending.treasury_sol_available)} SOL`);
        }
        catch {
            // token may not have lending enabled yet
        }
    }
}
// ---------------------------------------------------------------------------
// main — read-only only
// ---------------------------------------------------------------------------
async function main() {
    const config = (0, config_1.loadReadOnlyConfig)();
    const connection = new web3_js_1.Connection(config.rpcUrl, 'confirmed');
    const MINT = process.env.MINT;
    if (MINT) {
        await showLendingInfo(connection, MINT);
    }
    else {
        await showAllLending(connection);
    }
}
main();
//# sourceMappingURL=index.js.map