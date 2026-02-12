"use strict";
/**
 * torchsdk v2.0.0 — stripped to just the methods utilized by lib/bot/
 *
 * Only read-only query functions are included.
 * Transaction builders, SAID Protocol, and quote functions are not present.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TOTAL_SUPPLY = exports.TOKEN_MULTIPLIER = exports.LAMPORTS_PER_SOL = exports.PROGRAM_ID = exports.getVaultWalletLink = exports.getVaultForWallet = exports.getVault = exports.getLoanPosition = exports.getLendingInfo = exports.getMessages = exports.getHolders = exports.getToken = exports.getTokens = void 0;
// Token data (read-only)
var tokens_1 = require("./tokens");
Object.defineProperty(exports, "getTokens", { enumerable: true, get: function () { return tokens_1.getTokens; } });
Object.defineProperty(exports, "getToken", { enumerable: true, get: function () { return tokens_1.getToken; } });
Object.defineProperty(exports, "getHolders", { enumerable: true, get: function () { return tokens_1.getHolders; } });
Object.defineProperty(exports, "getMessages", { enumerable: true, get: function () { return tokens_1.getMessages; } });
Object.defineProperty(exports, "getLendingInfo", { enumerable: true, get: function () { return tokens_1.getLendingInfo; } });
Object.defineProperty(exports, "getLoanPosition", { enumerable: true, get: function () { return tokens_1.getLoanPosition; } });
Object.defineProperty(exports, "getVault", { enumerable: true, get: function () { return tokens_1.getVault; } });
Object.defineProperty(exports, "getVaultForWallet", { enumerable: true, get: function () { return tokens_1.getVaultForWallet; } });
Object.defineProperty(exports, "getVaultWalletLink", { enumerable: true, get: function () { return tokens_1.getVaultWalletLink; } });
// Constants (for advanced usage)
var constants_1 = require("./constants");
Object.defineProperty(exports, "PROGRAM_ID", { enumerable: true, get: function () { return constants_1.PROGRAM_ID; } });
Object.defineProperty(exports, "LAMPORTS_PER_SOL", { enumerable: true, get: function () { return constants_1.LAMPORTS_PER_SOL; } });
Object.defineProperty(exports, "TOKEN_MULTIPLIER", { enumerable: true, get: function () { return constants_1.TOKEN_MULTIPLIER; } });
Object.defineProperty(exports, "TOTAL_SUPPLY", { enumerable: true, get: function () { return constants_1.TOTAL_SUPPLY; } });
