# Security Notes
- Guardian is a defensive scanner. Signature definitions are encoded (`definitions/encoded/*.enc`) to avoid misuse; runtime decodes them before loading.
- No external download/shell execution in runtime code. `subprocess` use is limited to optional cron setup in `scripts/onboard.py` when explicitly invoked by the operator.
- Packaging excludes tests/assets/plaintext definition files via `.clawhubignore` to reduce false positives in security scans.
