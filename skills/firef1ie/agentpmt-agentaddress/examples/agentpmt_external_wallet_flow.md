# AgentPMT External Wallet Flow (x402 + Signed Invoke)

Base URL:
- `https://www.agentpmt.com`

## 1) Generate AgentAddress (no auth)

```bash
curl -s -X POST "https://www.agentpmt.com/api/external/agentaddress" \
  -H "Content-Type: application/json"
```

Expected shape:

```json
{
  "success": true,
  "data": {
    "evmAddress": "0x...",
    "evmPrivateKey": "0x...",
    "mnemonic": "..."
  }
}
```

## 2) x402 purchase (handshake)

Step A: request payment requirements.

```bash
curl -i -s -X POST "https://www.agentpmt.com/api/external/credits/purchase" \
  -H "Content-Type: application/json" \
  -d '{"wallet_address":"0xAGENT","credits":500,"payment_method":"x402"}'
```

Parse `PAYMENT-REQUIRED` response header. Decode from base64 to JSON.

Step B: produce EIP-3009 `TransferWithAuthorization` signature and retry with `PAYMENT-SIGNATURE`.

```bash
curl -s -X POST "https://www.agentpmt.com/api/external/credits/purchase" \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <base64-json-payload>" \
  -d '{"wallet_address":"0xAGENT","credits":500,"payment_method":"x402"}'
```

## 3) Create signed session

```bash
curl -s -X POST "https://www.agentpmt.com/api/external/auth/session" \
  -H "Content-Type: application/json" \
  -d '{"wallet_address":"0xAGENT"}'
```

Save `session_nonce`.

## 4) Build signature for invoke

Canonical payload hash:
- `payload_hash = sha256(canonical_json(parameters))`
- canonical JSON must be sorted keys and no extra spaces.

Message template:

```text
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
action:invoke
product:{product_id}
payload:{payload_hash}
```

Sign with agent private key using EIP-191 (`personal_sign` style).

## 5) Invoke tool

```bash
curl -s -X POST "https://www.agentpmt.com/api/external/tools/<productId>/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_address":"0xAGENT",
    "session_nonce":"<session_nonce>",
    "request_id":"invoke-<uuid>",
    "signature":"0x<signature>",
    "parameters":{"action":"get_instructions"}
  }'
```

Optional credit check:

```bash
curl -s -X POST "https://www.agentpmt.com/api/external/credits/balance" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_address":"0xAGENT",
    "session_nonce":"<session_nonce>",
    "request_id":"balance-<uuid>",
    "signature":"0x<signature>"
  }'
```
