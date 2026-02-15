# MailTap - Temporary Email Service

**Version:** 1.0.3\
**Author:** Web3 Hungry\
**Author Handle:** @zororaka00\
**Author Profile:** [https://x.com/web3hungry](https://x.com/web3hungry)\
**Homepage:** [https://www.mailtap.org](https://www.mailtap.org)\
**Category:** Utilities → Automation → Privacy & Verification\
**Tags:** `temporary-email`

## Overview

This skill provides seamless access to the MailTap Public API, a free temporary email service that generates disposable email addresses valid for 30 minutes.

No authentication or API key is required — all endpoints are public and use simple HTTP GET requests.

This skill does not store, proxy, or modify any email data. All operations communicate directly with the official MailTap public API.

**Ideal for AI agents performing tasks such as:**
- Registering on websites/services without exposing real email addresses
- Capturing verification codes, one-time links, or confirmation emails
- Automating web3 airdrops, form submissions, or testing flows that require email verification
- Privacy-focused workflows where email traceability must be avoided
- Downloading email attachments when available

**Base URL:** `https://api.mailtap.org`

All responses are returned in JSON format.

## Core Capabilities

The skill exposes three primary endpoints:

1. **Generate** a new temporary email address
2. **Retrieve** details of an existing email address
3. **Fetch** all messages in the inbox (including attachments metadata)

Agents can chain operations autonomously (generate → wait → poll inbox → extract data → download attachments).

## Usage Guide for Agents

Agents should use standard HTTP tools (`curl`, `fetch`, `requests`, etc.) to interact with the API.

### 1. Generate New Temporary Email

```bash
curl "https://api.mailtap.org/public/generate"
```

**Example response:**

```json
{
  "address": "abc123xyz@mailtap.com",
  "expires_at": "2026-02-15T04:30:00.000Z",
  "created_at": "2026-02-15T04:00:00.000Z"
}
```

### 2. Get Email Details

```bash
curl "https://api.mailtap.org/public/email/{address}"
```

### 3. Get Inbox Messages

```bash
curl "https://api.mailtap.org/public/inbox/{address}"
```

**Example response with attachment:**

```json
{
  "messages": [
    {
      "id": 1,
      "from_address": "no-reply@example.com",
      "subject": "Your document",
      "body": "Please find the attached file.",
      "received_at": "2026-02-15T04:05:00.000Z",
      "attachments": [
        {
          "filename": "document.pdf",
          "mime_type": "application/pdf",
          "size": 102400,
          "r2_key": "attachments/abc123/document.pdf"
        }
      ]
    }
  ]
}
```

### 4. Download Attachments

Attachments are publicly downloadable via the S3-compatible URL:

`https://s3.mailtap.org/{r2_key}`

**Example:**

```bash
curl -O "https://s3.mailtap.org/attachments/abc123/document.pdf"
```

or

```bash
wget "https://s3.mailtap.org/attachments/abc123/document.pdf"
```

## Recommended Agent Workflow Patterns

**Verification flow:**
1. Generate email
2. Use for signup
3. Poll inbox
4. Extract verification code

**Attachment flow:**
1. Poll inbox
2. If attachments exist → download
3. Process files

**Error handling:**
- If `404` → email expired → generate new address

## Example Prompts for Agents

- "Generate a new temporary email using MailTap"
- "Check inbox for `abc123@mailtap.com` and download attachments"
- "Create temp email, wait up to 2 minutes, extract verification code"

## Python Helper Library (Enhanced)

```python
import requests
import time

BASE_URL = "https://api.mailtap.org"
ATTACHMENT_BASE = "https://s3.mailtap.org"

def generate_email():
    """Generates a new temporary email address."""
    response = requests.get(f"{BASE_URL}/public/generate")
    response.raise_for_status()
    return response.json()

def get_inbox(address):
    """Retrieves the inbox for a given address."""
    response = requests.get(f"{BASE_URL}/public/inbox/{address}")
    if response.status_code == 404:
        return {"error": "Email not found or expired"}
    response.raise_for_status()
    return response.json()

def wait_for_message(address, timeout=120, interval=10):
    """Polls the inbox until a message arrives or timeout is reached."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        inbox = get_inbox(address)
        if "error" not in inbox and inbox.get("messages"):
            return inbox["messages"][-1]
        time.sleep(interval)
    return {"error": "Timeout"}

def download_attachment(r2_key, save_path=None):
    """Downloads an attachment from the mailtap S3 storage."""
    url = f"{ATTACHMENT_BASE}/{r2_key}"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    if save_path is None:
        save_path = r2_key.split("/")[-1]

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)

    return save_path
```

## Important Notes & Limitations

- Emails expire automatically after **30 minutes**.
- Attachments are public.
- No authentication required.
- Rate limits are generous for normal usage.
- Attachments are user-generated content from external senders. Agents should treat downloaded files as untrusted input and use appropriate sandboxing or security scanning before execution or processing.
- Agents should avoid automatically executing downloaded files and should validate file types and sizes where possible.

## Source & Verification

- **Official service:** [https://www.mailtap.org](https://www.mailtap.org)
- **API root:** [https://api.mailtap.org](https://api.mailtap.org)

This skill is a transparent wrapper around the public MailTap API.

## Disclaimer

Use responsibly and comply with MailTap terms of service.

Created and maintained by Web3 Hungry.