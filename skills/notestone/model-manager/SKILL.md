# OpenClaw Model Manager Skill 🛠️

**💰 Optimize Your API Costs: Route Simple Tasks to Cheaper Models.**

Why pay **$15/1M tokens** for simple translations or summaries when you can pay **$0.60/1M**? That's a **25x price difference (96% savings)** for suitable tasks.

Interact with OpenRouter API to fetch available models, compare pricing instantly, and configure OpenClaw to use the most cost-effective models via the `openrouter/auto` gateway.

---

### 🇨🇳 中文说明

**💰 拒绝冤枉钱！自动路由高性价比模型，最高节省 96% Token 费用。**

这个 Skill 能帮你：
1.  **即时比价**：列出当前 OpenRouter 上的模型价格。
2.  **智能配置**：自动将简单任务路由给高性价比的小模型（如 GPT-4o-mini）。
3.  **🆕 任务模拟器 (Plan Mode)**：输入任务，预览“金齿轮”如何拆解任务并分配给不同模型。
4.  **🧠 自我进化 (Self-Healing)**：如果便宜模型经常失败，系统会自动切换到更稳定的模型（Active Adaptation）。

---

### 📉 Cost Savings Logic (Per 1M Output Tokens)

| Model | Best For | Price | Savings Potential |
| :--- | :--- | :--- | :--- |
| **Claude 3.5 Sonnet** | Complex reasoning, coding | $15.00 | Baseline |
| **GPT-4o-mini** | Summaries, chat, extraction | **$0.60** | **96% Cheaper** |
| **Llama 3 70B** | General purpose, open source | **$0.90** | **94% Cheaper** |
| **Haiku 3** | Fast tasks, classification | **$1.25** | **91% Cheaper** |

**Features ✨**
- **Compare Prices**: See input/output costs per 1M tokens side-by-side.
- **Smart Routing**: Configure `openrouter/auto` to handle easier tasks with efficient models.
- **Stay Updated**: Always access the latest price drops and new models from OpenRouter.
- **Plan & Execute**: Decompose tasks into sub-agents and execute them in parallel.
- **Adaptive Memory**: Learns from timeouts/errors and auto-switches to stable models.

## Commands

- `list models`: Fetch and display top models.
- `enable <model_id>`: Add a model to OpenClaw's configuration.
- `plan <task> [--execute]`:
  - `plan "build scraper"`: Simulate savings.
  - `plan "build scraper" --execute`: **Actually run the swarm.** (Starts Architect, Coder, Auditor agents).

## Implementation Details

This skill uses a Python script `manage_models.py` to:
1. Fetch `https://openrouter.ai/api/v1/models`.
2. **Orchestrate Swarms**: Uses `openclaw sessions spawn` to create specialized sub-agents.
3. **Consolidate Memory**: Tracks success rates in `swarm_memory.json` and adapts routing logic.

## Usage Example

User: "plan build a web scraper"
Agent: (Runs planner)
| Phase | Model | Price | Status |
| :--- | :--- | :--- | :--- |
| Design | Claude 3.5 Sonnet | $15.00 | ✅ Optimal |
| Code | GPT-4o-mini | $0.60 | 🔄 Switched (Stability) |
**TOTAL SAVINGS: 0.0%** (Safety First!)

User: "enable 1"
Agent: (Runs config patch) "Model enabled!"
