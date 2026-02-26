# Changelog

## v1.2.4 - 2025-02-25
### Changed
- Backend simplified: Removed /api/live-test endpoint
- Live testing now skill-only (local OpenClaw required)
- Added honest documentation about limitations
- Fixed rate limiting with IP whitelist

### Fixed
- PDF generation attribute error (duration_ms -> test_duration_ms)
- Promo code validation

## v1.2.3 - 2025-02-25
### Added
- IP whitelist for development (145.224.96.221)
- Rate limiting improvements

## v1.2.2 - 2025-02-25
### Added
- Complete Live Testing with agentshield_security module
- 52 attack vectors
- Response analyzer with confidence scoring

## v1.2.1 - 2025-02-25
### Fixed
- PDF generation bug (TestResults attribute)

## v1.2.0 - 2025-02-25
### Added
- Live Security Test feature (initial implementation)
- New frontend tab for live testing
- Agent security assessment with real subagents

## v1.1.1 - 2025-02-24
### Changed
- Documentation honesty update
- "Security Audit" → "Security Assessment"
- "Security Score" → "Pattern Score"
- Added clear disclaimers

## v1.1.0 - 2025-02-24
### Added
- Live testing prototype
- Subagent integration
- Cost tracking

## v1.0.0 - 2025-02-23
### Added
- Token Optimizer
- Code Security Scan
- Agent Audit with certificates
- PDF report generation
