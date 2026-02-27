# 📡 Semantic Router 语义路由技能 / Semantic Router Skill

---

## 简介 / Introduction

Semantic Router 是一个可配置的**语义检查与模型路由技能**，支持用户自定义模型池和任务类型匹配规则。

*Semantic Router is a configurable semantic check and model routing skill that supports custom model pools and task type matching rules.*

**发布地址 / Publish Address:** https://clawhub.ai/skill/semantic-router

---

## ✨ 功能特性 / Features

| 特性 / Feature | 说明 / Description |
|----------------|-------------------|
| **两步检测 / Two-Step Detection** | Step 1 延续性检查 → Step 2 任务类型匹配 |
| **延续性判断 / Continuity Check** | 关键词 + 指示词 + 词汇重叠度 |
| **关键词优先级 / Keyword Priority** | P0(延续) > P1(开发) > P2(查询) > P3(内容) > P4(新会话) |
| **强制触发 / Force Trigger** | 通过 message injector 每次消息都执行语义检查 |
| **Fallback 回路 / Fallback Circuit** | Primary → Fallback1 → Fallback2，每2小时自动回切 |
| **自动切换 / Auto Switch** | 根据任务类型自动选择合适的模型池 |

---

## 🔍 两步检测流程 / Two-Step Detection Flow

### 核心逻辑 / Core Logic

**两步检测是优先级关系，不是替代关系**：

*Two-step detection is about priority, not replacement.*

```
用户消息 / User Message
    ↓
Step 1: 语义连续性检查 / Semantic Continuity Check (优先 / Priority)
    │
    ├── P0: 延续关键词 ["继续", "接着", "刚才", "下一步"] / Continue keywords
    │     → 保持当前池 / Keep current pool (B分支 / B-branch)
    │
    ├── P1: 指示词 ["这个", "那个", "它"] / Indicator words
    │     → 保持当前池 / Keep current pool (B分支 / B-branch)
    │
    └── P2: 词汇重叠度 Jaccard >= 0.1 / Vocabulary overlap
          → 保持当前池 / Keep current pool (B分支 / B-branch)
    
    ↓ 如果上面都不匹配 / If none match
    
Step 2: 任务类型匹配 / Task Type Matching
    ├── P1: 开发关键词 / Dev keywords → Intelligence 池 / pool
    ├── P2: 查询关键词 / Query keywords → Highspeed 池 / pool
    ├── P3: 内容关键词 / Content keywords → Humanities 池 / pool
    └── P4: 新会话 / New session → 高速池默认 / Highspeed default
```

### 关键点 / Key Points

1. **Step 1 优先于 Step 2** — 只有 Step 1 判断为"延续"才保持当前池
   *Step 1 takes priority - only if Step 1 determines "continue" do we keep the current pool*
2. **三种延续判断方式** / **Three ways to determine continuation**:
   - 延续关键词（最高优先级）/ Continue keywords (highest priority)
   - 指示词（这个/那个/它）/ Indicator words (this/that/it)
   - 上下文词汇重叠度（Jaccard >= 0.1）/ Context vocabulary overlap
3. **只有 Step 1 不匹配时才走 Step 2** / *Only when Step 1 doesn't match do we go to Step 2*

### 分支动作 / Branch Actions

| 分支 / Branch | 条件 / Condition | 动作 / Actions |
|--------------|------------------|---------------|
| **B分支** | 延续判断成功 / Continue detected | 保持当前模型池 / Keep current pool |
| **C分支** | 延续判断失败 / Continue failed | 1. 切换到目标模型池<br>2. 归档旧上下文<br>3. 插入上下文截止符 |

**C分支触发的三个动作**：
1. **切换模型池** — 根据任务类型切换到对应的模型池
2. **归档旧上下文** — 将之前的对话历史归档保存  
3. **插入截止符** — 在新上下文前插入 `[上下文截止符]` 标记

---

## 🏊 三池架构 / Three-Pool Architecture

| 池 / Pool | 任务类型 / Task Type | Primary | Fallback 1 | Fallback 2 |
|-----------|---------------------|---------|------------|-------------|
| **Highspeed** | 信息检索、网页搜索 / Info Retrieval, Web Search | gpt-4o-mini | glm-4.7-flashx | MiniMax-M2.5 |
| **Intelligence** | 开发、自动化、系统运维 / Dev, Automation, Ops | Codex | kimi-k2.5 | MiniMax-M2.5 |
| **Humanities** | 内容生成、多模态、问答 / Content, Multimodal, Q&A | GPT-4o | kimi-k2.5 | MiniMax-M2.5 |

---

## 📖 使用方法 / Usage

### 基础检测 / Basic Check
```bash
python3 semantic_check.py "查一下天气" "Intelligence"
```

### 带上下文检测 / Check with Context
```bash
python3 semantic_check.py "继续" "Intelligence" "帮我写个函数" "谢谢"
```

### Fallback 模式 / Fallback Mode
```bash
python3 semantic_check.py --fallback Codex kimi-k2.5 MiniMax-M2.5
```

---

## 🔧 自定义配置 / Custom Configuration

### 1. 自定义模型池 / Custom Model Pools

编辑 `config/pools.json`：

```json
{
  "你的池名": {
    "name": "显示名称",
    "description": "池描述",
    "primary": "主模型ID",
    "fallback_1": "备用模型1",
    "fallback_2": "备用模型2"
  }
}
```

### 2. 自定义任务匹配 / Custom Task Matching

编辑 `config/tasks.json`：

```json
{
  "任务类型名": {
    "keywords": ["关键词1", "关键词2"],
    "pool": "对应的池名"
  }
}
```

**关键词匹配规则 / Keyword Matching Rules**：
- `standalone: false`（默认）：关键词包含在文本中即匹配
- `standalone: true`：关键词必须完全匹配或作为开头

### 3. 环境变量覆盖 / Environment Variables

```bash
export CURRENT_POOL="Intelligence"
export PRIMARY_MODEL="你们自己的模型ID"
python3 semantic_check.py "你的消息"
```

---

## ⚡ 强制触发配置 / Force Trigger Config

通过 message injector 插件强制每次消息都触发语义检查：

*Force semantic check on every message:*

```json
{
  "plugins": {
    "entries": {
      "message-injector": {
        "enabled": true,
        "trigger": "always",
        "script": "python3 ~/.openclaw/workspace/skills/semantic-router/scripts/semantic_check.py"
      }
    }
  }
}
```

---

## 📦 安装 / Installation

```bash
# 从 ClawHub 安装 / Install from ClawHub
clawhub install semantic-router

# 或指定版本 / Or specify version
clawhub install semantic-router --version 1.2.2
```

---

## 📁 文件结构 / File Structure

```
semantic-router/
├── SKILL.md              # 技能说明 / Skill Description
├── README.md             # 使用指南 / User Guide
├── config/
│   ├── pools.json       # 模型池配置 / Model Pool Config
│   └── tasks.json       # 任务类型配置 / Task Type Config
└── scripts/
    └── semantic_check.py # 核心脚本 / Core Script
```

---

## 📝 版本历史 / Version History

| 版本 / Version | 更新内容 / Changes |
|----------------|-------------------|
| **1.2.2** | 修正两步检测流程描述，完善自定义配置说明 / Fix two-step detection description, improve custom config |
| **1.2.1** | 中英双语 README / Bilingual README |
| **1.2.0** | Fallback 回路自动化 / Fallback circuit automation |
| **1.1.0** | 两步检测机制 + 关键词优先级 / Two-step detection + keyword priority |
| **1.0.0** | 初始版本 / Initial release |

---

## 👤 作者 / Author

- **作者 / Author：** DeepEye (Sir 的数字分身 / Sir's Digital Twin)
- **联系 / Contact：** bubushi@126.com

---

*Generated on 2026-02-23*
