---
name: agentpmt-agentaddress
description: Generate an AgentAddress wallet and use it to buy AgentPMT credits with x402, then invoke external tools with wallet signatures.
homepage: https://www.agentpmt.com/agentaddress
---

# AgentPMT AgentAddress + External Purchase Flow

Use this skill when the user wants an autonomous agent to:
- create its own AgentAddress wallet,
- purchase AgentPMT credits,
- and spend those credits on external tool calls.

Always target AgentPMT Next.js external endpoints (`/api/external/...`), not internal backend container routes.

## Required Endpoints

- `POST /api/external/agentaddress`
- `POST /api/external/credits/purchase`
- `POST /api/external/auth/session`
- `POST /api/external/tools/{productId}/invoke`
- `POST /api/external/credits/balance` (optional balance check)

## Flow

1. Generate wallet (no auth):
- Call `POST /api/external/agentaddress`.
- Save `evmAddress`, `evmPrivateKey`, and `mnemonic` securely.

2. Purchase credits with `x402`:
- Send first purchase request:
  - body: `{"wallet_address":"<address>","credits":500,"payment_method":"x402"}`
- Expect `402` and read `PAYMENT-REQUIRED` header (base64 JSON).
- Build EIP-3009 `TransferWithAuthorization` signature for USDC:
  - from: agent wallet
  - to: returned `payTo`
  - value: returned `amount`
  - validAfter / validBefore / nonce
- Send second purchase request with `PAYMENT-SIGNATURE` header (base64 JSON payload with signature + authorization).

3. Get session nonce:
- Call `POST /api/external/auth/session` with `{"wallet_address":"<address>"}`.

4. Sign tool invocation message (EIP-191 / personal_sign):
- Canonicalize parameters JSON and compute lowercase SHA-256 hash.
- Build message exactly:
```
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
action:invoke
product:{product_id}
payload:{payload_hash}
```
- Sign with the agent private key.

5. Invoke tool:
- Call `POST /api/external/tools/{productId}/invoke` with:
  - `wallet_address`
  - `session_nonce`
  - `request_id` (unique per request)
  - `signature`
  - `parameters`

## Safety Rules

- Never expose or log private keys/mnemonics in plaintext output.
- Never place secrets in prompt text when avoidable.
- Use fresh `request_id` values to avoid replay errors.
- Keep `wallet` lowercase in signed message payload.
- If credits are insufficient (`402`), purchase additional credits before retrying.

## Reference

For concrete request examples, use:
- `{baseDir}/examples/agentpmt_external_wallet_flow.md`
