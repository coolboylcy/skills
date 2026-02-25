# GitHub

## Base URL
```
https://api.github.com
```

## Authentication
```bash
curl https://api.github.com/user \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json"
```

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /user | GET | Current user |
| /repos/:owner/:repo | GET | Get repo |
| /repos/:owner/:repo/issues | GET | List issues |
| /repos/:owner/:repo/issues | POST | Create issue |
| /repos/:owner/:repo/pulls | GET | List PRs |
| /repos/:owner/:repo/pulls | POST | Create PR |
| /repos/:owner/:repo/contents/:path | GET | Get file content |
| /search/repositories | GET | Search repos |

## Quick Examples

### List Repos
```bash
curl https://api.github.com/user/repos \
  -H "Authorization: Bearer $GITHUB_TOKEN"
```

### Create Issue
```bash
curl -X POST https://api.github.com/repos/OWNER/REPO/issues \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bug report",
    "body": "Description here",
    "labels": ["bug"]
  }'
```

### Create Pull Request
```bash
curl -X POST https://api.github.com/repos/OWNER/REPO/pulls \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New feature",
    "head": "feature-branch",
    "base": "main",
    "body": "PR description"
  }'
```

### Get File Content
```bash
curl https://api.github.com/repos/OWNER/REPO/contents/README.md \
  -H "Authorization: Bearer $GITHUB_TOKEN"
# Content is base64 encoded
```

### Search Repositories
```bash
curl "https://api.github.com/search/repositories?q=language:python+stars:>1000" \
  -H "Authorization: Bearer $GITHUB_TOKEN"
```

## Common Traps

- File content is base64 encoded
- Rate limit: 5000 req/hour (authenticated)
- Pagination via Link header, not body
- Accept header affects response format
- Some endpoints require specific scopes

## Rate Limits

- Authenticated: 5000 requests/hour
- Unauthenticated: 60 requests/hour
- Search: 30 requests/minute

Check with:
```bash
curl -I https://api.github.com/users/octocat
# X-RateLimit-Remaining header
```

## Official Docs
https://docs.github.com/en/rest
