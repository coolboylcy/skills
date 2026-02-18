# PromptLayer API Reference

Base URL: `https://api.promptlayer.com`
Auth: `Authorization: Bearer <PROMPTLAYER_API_KEY>`

## Prompt Templates

### Get Template
`POST /prompt-templates`
```json
{"prompt_name": "my-prompt", "label": "prod"}
```
Returns the prompt template with messages, model config, and metadata.

### List Templates
`GET /prompt-templates`

### Publish Template
`POST /prompt-templates/publish`
```json
{"prompt_name": "my-prompt", "commit_message": "updated tone"}
```

### Template Labels
- `GET /prompt-templates/labels` — list labels
- `POST /prompt-templates/labels` — create label
- `PATCH /prompt-templates/labels` — move label to version
- `DELETE /prompt-templates/labels` — delete label

## Logging & Tracking

### Log Request
`POST /log-request`
```json
{
  "function_name": "openai.chat.completions.create",
  "kwargs": {"model": "gpt-4", "messages": [...]},
  "request_response": {"choices": [...]},
  "request_start_time": 1234567890,
  "request_end_time": 1234567891
}
```
Returns `{"request_id": 123}`

### Track Score
`POST /track-score`
```json
{"request_id": 123, "score_name": "accuracy", "value": 0.95}
```

### Track Metadata
`POST /track-metadata`
```json
{"request_id": 123, "metadata": {"user_id": "abc", "session": "xyz"}}
```

### Track Group
`POST /track-group`
```json
{"request_id": 123, "group_id": 456}
```

### Track Prompt
`POST /track-prompt`
```json
{"request_id": 123, "prompt_name": "my-prompt", "prompt_input_variables": {"cake_type": "chocolate"}}
```

### Bulk Spans
`POST /spans-bulk`
```json
{"spans": [...]}
```

## Datasets

### List Datasets
`GET /datasets`

### Create Dataset Group
`POST /datasets`

### Create Version from File
`POST /datasets/{group_id}/versions/file`

### Create Version from Filter
`POST /datasets/{group_id}/versions/filter`

## Evaluations

### List Pipelines
`GET /report`

### Create Pipeline
`POST /report`

### Run Pipeline
`POST /report/{pipeline_id}/run`

### Get Report
`GET /report/{pipeline_id}`

### Get Report Score
`GET /report/{pipeline_id}/score`

### Add Columns
`POST /report/{pipeline_id}/columns`

## Agents

### List Agents
`GET /workflows`

### Create Agent
`POST /workflows`

### Update Agent
`PATCH /workflows/{agent_id}`

### Run Agent
`POST /workflows/{agent_id}/run`
```json
{"input_variables": {"key": "value"}}
```

### Get Execution Results
`GET /workflows/{agent_id}/versions/{version_id}/executions`

## Docs
- Full docs: https://docs.promptlayer.com
- Python SDK: https://docs.promptlayer.com/languages/python
- JS SDK: https://docs.promptlayer.com/languages/javascript
- MCP: https://docs.promptlayer.com/languages/mcp
