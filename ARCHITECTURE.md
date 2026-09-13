# 🏗️ Architecture Documentation

## System Overview

The AI Code Review Agent is a multi-agent system built using **LangGraph** for orchestrating specialized LLM agents that perform different aspects of code review.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │  Streamlit   │  │  REST API    │  │  Python SDK        │   │
│  │     UI       │  │  Client      │  │  (Direct Import)   │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬───────────┘   │
└─────────┼──────────────────┼───────────────────┼───────────────┘
          │                  │                   │
          └──────────────────┼───────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                      FastAPI Layer                               │
│                             │                                    │
│  ┌─────────────────────────▼─────────────────────────┐         │
│  │         FastAPI Application                        │         │
│  │  • /api/v1/review                                 │         │
│  │  • /api/v1/supported-languages                    │         │
│  │  • /health, /docs                                 │         │
│  └─────────────────────────┬─────────────────────────┘         │
└────────────────────────────┼────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                    Agent Orchestration Layer                     │
│                             │                                    │
│  ┌─────────────────────────▼─────────────────────────┐         │
│  │         ReviewOrchestrator (LangGraph)             │         │
│  │                                                     │         │
│  │  ┌─────────────────────────────────────────────┐  │         │
│  │  │         LangGraph State Machine             │  │         │
│  │  │                                             │  │         │
│  │  │  Entry → Bug → Security → Performance      │  │         │
│  │  │           ↓      ↓          ↓               │  │         │
│  │  │        Quality → Aggregator → END           │  │         │
│  │  └─────────────────────────────────────────────┘  │         │
│  └─────────────────────────────────────────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                     Specialized Agents Layer                     │
│                             │                                    │
│  ┌──────────────┬───────────┼───────────┬───────────────────┐  │
│  │              │           │           │                   │  │
│  ▼              ▼           ▼           ▼                   ▼  │
│┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
││   Bug    │ │ Security │ │   Perf   │ │     Quality      │   │
││ Detector │ │ Analyzer │ │ Reviewer │ │     Checker      │   │
│└────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────────────┘   │
│     │            │            │            │                  │
│     └────────────┴────────────┴────────────┘                  │
│                  │                                             │
│  Each agent uses specialized prompts & LLM calls              │
└───────────────────┼───────────────────────────────────────────┘
                    │
┌───────────────────┼───────────────────────────────────────────┐
│                LLM Provider Layer                              │
│                   │                                            │
│  ┌────────────────▼─────────────────────┐                    │
│  │      LangChain + OpenAI LLMs         │                    │
│  │  • GPT-4o-mini (default)             │                    │
│  │  • Configurable temperature          │                    │
│  │  • Token management                  │                    │
│  └──────────────────────────────────────┘                    │
└──────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Client Layer

#### Streamlit UI (`src/ui/app.py`)
- **Purpose**: Interactive web interface for code review
- **Features**:
  - Code editor with syntax highlighting
  - Real-time review results
  - Issue filtering by severity
  - Review configuration options
- **Tech**: Streamlit, HTTP requests to API

#### REST API Client
- Any HTTP client can interact with the FastAPI backend
- Well-documented with OpenAPI/Swagger

#### Python SDK
- Direct import and usage of `ReviewOrchestrator`
- No HTTP overhead
- Good for batch processing

### 2. FastAPI Layer (`src/api/`)

#### Main Application (`main.py`)
- **Framework**: FastAPI with async support
- **Endpoints**:
  - `POST /api/v1/review`: Submit code for review
  - `GET /api/v1/supported-languages`: List supported languages
  - `GET /api/v1/review-types`: List available review types
  - `GET /health`: Health check
- **Features**:
  - Request validation with Pydantic
  - CORS middleware
  - Error handling
  - Logging

### 3. Agent Orchestration Layer (`src/agents/`)

#### ReviewOrchestrator (`review_orchestrator.py`)
- **Core Technology**: LangGraph StateGraph
- **Responsibilities**:
  - Manages workflow state
  - Routes between specialized agents
  - Aggregates results
  - Computes metrics

#### Workflow Execution Modes

**Sequential Mode** (default):
```
Start → Bug → Security → Performance → Quality → Aggregator → End
```

**Parallel Mode** (if enabled):
```
Start → ┌─ Bug
        ├─ Security    → Aggregator → End
        ├─ Performance
        └─ Quality
```

#### State Management
- Uses `AgentState` Pydantic model
- Immutable state transitions
- Each agent updates specific state fields

### 4. Specialized Agents Layer (`src/agents/`)

#### Base Agent (`base_agent.py`)
- Abstract base class for all agents
- Common functionality:
  - Prompt formatting
  - LLM invocation
  - Response parsing
  - Issue extraction

#### Specialized Agents

| Agent | Focus | Key Checks |
|-------|-------|------------|
| **BugDetectorAgent** | Logic errors, crashes | Null checks, type errors, edge cases |
| **SecurityAnalyzerAgent** | Vulnerabilities | SQL injection, XSS, credential exposure |
| **PerformanceReviewerAgent** | Optimization | Algorithm complexity, N+1 queries |
| **QualityCheckerAgent** | Best practices | Code smells, naming, documentation |

Each agent:
1. Receives code + context
2. Uses specialized system prompt
3. Calls LLM with structured output
4. Parses JSON response into `Issue` objects
5. Returns list of issues

### 5. Prompt Engineering (`src/prompts/`)

#### System Prompts (`system_prompts.py`)
- Carefully crafted prompts for each agent
- Structured to encourage:
  - Specific issue identification
  - Line number reporting
  - Severity classification
  - Actionable suggestions
  - JSON output format

#### Prompt Structure
```
1. Agent role definition
2. List of checks to perform
3. Output format specification
4. Code context injection
5. JSON schema enforcement
```

### 6. Data Models (`src/models/`)

#### Core Models (`schemas.py`)

**Issue**
- Represents a single code issue
- Fields: type, severity, title, description, location, suggestion
- Validation with Pydantic

**CodeSubmission**
- Input schema for code review request
- Fields: code, language, filename, context, review_types

**ReviewResult**
- Complete review output
- Fields: issues, summary, metrics, metadata

**AgentState**
- LangGraph workflow state
- Tracks agent execution and intermediate results

### 7. Configuration (`src/config/`)

#### Settings (`settings.py`)
- Centralized configuration using Pydantic Settings
- Environment variable loading
- Type-safe configuration
- Validates required fields (e.g., API keys)

Categories:
- LLM configuration (model, temperature, tokens)
- API configuration (host, port)
- Review configuration (timeout, max length)
- MLOps configuration (MLflow, logging)

### 8. Utilities (`src/utils/`)

#### Logging (`logging_config.py`)
- Structured logging setup
- File + console output
- Log level configuration
- Separate loggers for different components

#### Metrics (`metrics.py`)
- `ReviewMetrics`: Track review performance
- `MetricsTracker`: Aggregate metrics over time
- `calculate_quality_metrics`: Compute precision/recall/F1

## Data Flow

### Review Request Flow

```
1. Client submits code
   ↓
2. FastAPI validates request
   ↓
3. ReviewOrchestrator initializes state
   ↓
4. LangGraph executes workflow:
   a. BugDetectorAgent analyzes → returns issues
   b. SecurityAnalyzerAgent analyzes → returns issues
   c. PerformanceReviewerAgent analyzes → returns issues
   d. QualityCheckerAgent analyzes → returns issues
   e. Aggregator combines + sorts issues
   ↓
5. ReviewResult created with:
   - All issues
   - Summary
   - Metrics
   ↓
6. Response returned to client
```

### State Transitions

```python
Initial State:
{
  "code": "...",
  "language": "python",
  "review_types": ["bug", "security"],
  "bug_issues": [],
  "security_issues": [],
  ...
}

After BugDetectorAgent:
{
  ...,
  "bug_issues": [Issue(...), Issue(...)],
  "agents_executed": ["bug_detector"]
}

After All Agents:
{
  ...,
  "all_issues": [sorted list of all issues],
  "summary": "Found 5 issues...",
  "agents_executed": ["bug_detector", "security_analyzer", ...]
}
```

## Scalability Considerations

### Horizontal Scaling
- FastAPI is ASGI-based → can run multiple workers
- Stateless design → easy to replicate
- Load balancer in front of multiple API instances

### Caching
- Can add Redis for:
  - Code → Review result caching (by hash)
  - Rate limiting
  - Session management

### Async Processing
- Already using `async/await`
- Can add Celery/RQ for:
  - Background review jobs
  - Large file processing
  - Scheduled reviews

### Database
- Currently stateless
- Can add PostgreSQL/MongoDB for:
  - Review history
  - User management
  - Analytics

## Extension Points

### Adding New Agents
1. Create agent class extending `BaseReviewAgent`
2. Define specialized prompt
3. Add node to LangGraph workflow
4. Update state schema if needed

### Supporting New Languages
1. Add language to supported list
2. Update prompts with language-specific patterns
3. Add language-specific tools (optional)

### Custom Rule Engine
1. Define rule format (YAML/JSON)
2. Create rule parser
3. Inject rules into agent prompts
4. Track rule violations in issues

## Security

- API keys stored in environment variables (never in code)
- Code submissions not persisted by default
- CORS configured (customize for production)
- Input validation with Pydantic
- Code length limits to prevent abuse
- Timeout protection

## Performance

- Average review time: 3-6 seconds (depends on code length)
- Parallel agent execution can reduce to 1-2 seconds
- LLM API calls are the bottleneck
- Can optimize with:
  - Smaller models for simple checks
  - Caching
  - Batching multiple files

## Monitoring

- Structured logging to files + stdout
- Optional MLflow integration for:
  - Experiment tracking
  - Metrics visualization
  - Model comparison
- Metrics collected:
  - Review latency
  - Issues per review
  - Agent execution times
  - API response times

## Future Enhancements

1. **Multi-file reviews**: Analyze entire projects
2. **Incremental reviews**: Diff-based reviews (only changed code)
3. **Learning from feedback**: RLHF loop to improve quality
4. **IDE plugins**: VS Code, JetBrains integration
5. **GitHub integration**: Automated PR reviews
6. **Custom agents**: Org-specific coding standards
7. **Code fixing**: Auto-generate fixes for issues
