<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

# 网络安全智能体团队

一个在日志文件中检测安全威胁的 4 智能体管道。原生构建在 Claude Code 智能体团队之上。

**此示例的存在是为了比较两种方法**：LangGraph（Python 框架）vs Claude Code 智能体团队（原生）。同一系统，两种架构。差异告诉你何时使用哪种。

---

## 架构

```
log-ingestor (haiku)
      ↓
anomaly-detector (sonnet)
      ↓
risk-classifier (sonnet)
      ↓
threat-reporter (sonnet)
      ↓
cyber-defense-report.md
```

每个智能体有单一职责，并通过共享 JSON 文件将数据传递给下一个。编排技能（`/cyber-defense-team`）序列化触发并报告结果。

**用法**：`/cyber-defense-team /var/log/nginx/access.log`

---

## LangGraph vs Claude Code 智能体团队

同一系统构建了两次。这里是完整的比较。

### LangGraph 版本（~150 行 Python）

```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json

# ─── State Definition ─────────────────────────────────────────────────────────
class DefenseState(TypedDict):
    raw_logs: str
    parsed_events: List[dict]
    anomalies: List[dict]
    risk_level: str      # LOW | MEDIUM | HIGH | CRITICAL
    report: str

# ─── Tools (Python functions the LLM can call) ────────────────────────────────
@tool
def detect_patterns(logs: str) -> List[dict]:
    """Extract structured events from raw log text."""
    events = []
    for line in logs.split("\n"):
        if any(k in line for k in ["ERROR", "FAILED", "UNAUTHORIZED"]):
            events.append({"type": "security_event", "raw": line})
        elif "WARNING" in line:
            events.append({"type": "warning", "raw": line})
    return events

@tool
def detect_anomalies(events: List[dict]) -> List[dict]:
    """Detect statistical anomalies in event patterns."""
    anomalies = []
    error_count = sum(1 for e in events if e["type"] == "security_event")
    if error_count > 5:
        anomalies.append({"type": "high_error_rate", "count": error_count, "severity": "HIGH"})
    return anomalies

@tool
def lookup_threat(event_type: str) -> dict:
    """Look up known threat signatures."""
    db = {
        "UNAUTHORIZED": {"description": "Auth bypass attempt"},
        "SQL_INJECTION": {"cve": "CVE-2021-1234", "description": "SQLi pattern"}
    }
    return db.get(event_type, {"description": "Unknown threat"})

# ─── LLM Setup ────────────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools([detect_patterns, detect_anomalies, lookup_threat])

# ─── Nodes (one function per agent role) ──────────────────────────────────────
def ingest_node(state: DefenseState) -> DefenseState:
    events = detect_patterns.invoke(state["raw_logs"])
    return {**state, "parsed_events": events}

def detect_node(state: DefenseState) -> DefenseState:
    anomalies = detect_anomalies.invoke(state["parsed_events"])
    return {**state, "anomalies": anomalies}

def classify_node(state: DefenseState) -> DefenseState:
    result = llm_with_tools.invoke([
        SystemMessage("Classify risk as LOW/MEDIUM/HIGH/CRITICAL."),
        HumanMessage(f"Anomalies: {json.dumps(state['anomalies'])}")
    ])
    risk = "HIGH" if state["anomalies"] else "LOW"
    return {**state, "risk_level": risk}

def report_node(state: DefenseState) -> DefenseState:
    result = llm_with_tools.invoke([
        SystemMessage("You are a Senior Security Analyst. Write a Markdown incident report."),
        HumanMessage(f"Risk: {state['risk_level']}\nAnomalies: {json.dumps(state['anomalies'])}")
    ])
    return {**state, "report": result.content}

# ─── Conditional Edge ─────────────────────────────────────────────────────────
def should_report(state: DefenseState) -> str:
    return "report" if state["anomalies"] else END

# ─── Graph Assembly ───────────────────────────────────────────────────────────
builder = StateGraph(DefenseState)
builder.add_node("ingest", ingest_node)
builder.add_node("detect", detect_node)
builder.add_node("classify", classify_node)
builder.add_node("report", report_node)

builder.set_entry_point("ingest")
builder.add_edge("ingest", "detect")
builder.add_edge("detect", "classify")
builder.add_conditional_edges("classify", should_report)
builder.add_edge("report", END)

# ─── Memory ───────────────────────────────────────────────────────────────────
checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# ─── Entry Point ──────────────────────────────────────────────────────────────
def analyze_logs(logs: str) -> str:
    config = {"configurable": {"thread_id": "security-session-1"}}
    result = app.invoke(
        {"raw_logs": logs, "parsed_events": [], "anomalies": [], "risk_level": "", "report": ""},
        config
    )
    return result.get("report", "No threats detected.")
```

### Claude Code 版本（~60 行 YAML/Markdown）

四个智能体文件，一个技能文件。没有图组装、没有 TypedDict、没有样板代码。

```
examples/agents/cyber-defense/
├── log-ingestor.md       (~40 行)
├── anomaly-detector.md   (~50 行)
├── risk-classifier.md    (~55 行)
└── threat-reporter.md    (~45 行)

examples/skills/cyber-defense-team/
└── SKILL.md              (~70 行)
```

每个智能体文件是一个 YAML 前导（名称、模型、工具）+ 用简单英语描述的职责、输入、输出和约束的系统提示。技能文件使用 `Agent tool` 调用对智能体进行排序。

---

## 并排比较

| 维度 | LangGraph | Claude Code 智能体团队 |
|-----------|-----------|------------------------|
| **总代码量** | ~150 行 Python | ~60 行 YAML/Markdown |
| **状态管理** | 显式 `TypedDict` 定义 | 隐式 — 智能体之间的 JSON 文件 |
| **记忆** | 手动 `MemorySaver` 设置 | 原生（文件默认持久化） |
| **工具定义** | `@tool` 装饰的 Python 函数 | MCP 服务器或内置工具 |
| **条件逻辑** | `add_conditional_edges()` | 技能中的自然语言（"如果无异常，跳到步骤 5"） |
| **模型选择** | 所有节点一个模型 | 每个智能体单独配置（haiku 用于解析，sonnet 用于推理） |
| **调试** | `print()` + LangSmith（付费） | 原生 Claude Code UI |
| **新智能体角色** | 新函数 + `add_node()` + `add_edge()` | 新 `.md` 文件 |
| **上手难度** | 学习 LangGraph API | 阅读 Markdown 文件 |
| **部署** | FastAPI 或 Gradio（~50 多行） | `claude` CLI，完成 |
| **依赖** | `langgraph`、`langchain`、`langchain-openai` | 无（内置到 Claude Code 中） |

---

## 何时使用哪种

**使用 Claude Code 智能体团队当：**
- 你想快速行动 — 从原型到工作系统只需 30 分钟
- 你的团队包括非开发者，他们可能阅读或编辑智能体提示
- 管道是内部工具（不是公共 API 端点）
- 你需要频繁迭代智能体行为（编辑 `.md` 文件，完成）

**使用 LangGraph 当：**
- 你需要将系统嵌入更大的 Python 应用程序
- 你想将管道作为 REST API 暴露给外部消费者
- 你需要确定性的状态转换，必须进行单元测试
- 你的团队已经使用 Python 并拥有 LangGraph 专业知识

**诚实的权衡**：LangGraph 提供更多的程序化控制和 Python 生态系统访问。Claude Code 智能体团队提供更少的样板代码、更快的迭代和无基础设施维护。对于内部工具和知识工作管道，Claude Code 方法通常在总拥有成本上胜出。

---

## 此示例中的文件

| 文件 | 智能体角色 | 模型 | 职责 |
|------|-----------|-------|----------------|
| `log-ingestor.md` | 阶段 1 | haiku | 解析原始日志 → `cyber-defense-events.json` |
| `anomaly-detector.md` | 阶段 2 | sonnet | 检测模式 → `cyber-defense-anomalies.json` |
| `risk-classifier.md` | 阶段 3 | sonnet | 评分风险 → `cyber-defense-risk.json` |
| `threat-reporter.md` | 阶段 4 | sonnet | 生成报告 → `cyber-defense-report.md` |
| `../skills/cyber-defense-team/SKILL.md` | 编排器 | — | 序列化智能体、处理错误、总结 |

---

**灵感来源**：Maryam Miradi 的 SMART COMPASS 框架 — 同一系统，不同技术栈。
