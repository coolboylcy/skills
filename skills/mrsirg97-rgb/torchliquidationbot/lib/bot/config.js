"use strict";
/**
 * config.ts — loads environment variables into a typed ReadOnlyConfig.
 *
 * no wallet loaded, no keypair decoded, no signing possible.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadReadOnlyConfig = loadReadOnlyConfig;
const LOG_LEVELS = ['debug', 'info', 'warn', 'error'];
function loadReadOnlyConfig() {
    const rpcUrl = process.env.RPC_URL;
    if (!rpcUrl)
        throw new Error('RPC_URL env var is required');
    const logLevel = (process.env.LOG_LEVEL ?? 'info');
    if (!LOG_LEVELS.includes(logLevel)) {
        throw new Error(`LOG_LEVEL must be one of: ${LOG_LEVELS.join(', ')}`);
    }
    return { rpcUrl, logLevel };
}
//# sourceMappingURL=config.js.map