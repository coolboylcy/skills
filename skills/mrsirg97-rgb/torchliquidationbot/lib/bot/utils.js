"use strict";
/**
 * utils.ts — shared helpers.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.sol = sol;
exports.bpsToPercent = bpsToPercent;
const torchsdk_1 = require("torchsdk");
function sol(lamports) {
    return (lamports / torchsdk_1.LAMPORTS_PER_SOL).toFixed(4);
}
function bpsToPercent(bps) {
    return (bps / 100).toFixed(2) + '%';
}
//# sourceMappingURL=utils.js.map