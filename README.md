# AI Code Review Agent 🤖

An intelligent, multi-agent code review system powered by LangGraph and LLMs that provides comprehensive, context-aware code analysis.

## 🎯 Overview

This AI Code Review Agent uses agentic workflows to perform automated code reviews across multiple dimensions:
- **Bug Detection**: Identifies potential bugs, logic errors, and edge cases
- **Security Analysis**: Detects security vulnerabilities and unsafe patterns
- **Performance Optimization**: Suggests performance improvements
- **Code Quality**: Enforces best practices and coding standards
- **Documentation Review**: Checks code documentation completeness

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Input                         │
│              (Code + Context)                        │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Router Agent  │ ◄─── Intent Classification
         └────────┬───────┘
                  │
    ┌─────────────┼─────────────┬─────────────┐
    ▼             ▼             ▼             ▼
┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Bug   │  │ Security │  │   Perf   │  │ Quality  │
│Detector│  │ Analyzer │  │ Reviewer │  │ Checker  │
└───┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
    │            │             │             │
    └────────────┴─────────────┴─────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Aggregator &  │
         │   Prioritizer  │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Review Report  │
         └────────────────┘
```

### Key Components

1. **LangGraph Workflow Engine**
   - Multi-agent orchestration
   - State management
   - Conditional routing

2. **Specialized Review Agents**
   - Each agent focuses on specific review aspects
   - Parallel execution for faster reviews
   - LLM-powered analysis

3. **FastAPI Backend**
   - RESTful API endpoints
   - Async processing
   - WebSocket support for real-time updates

4. **Evaluation Framework**
   - Metrics tracking (precision, recall, latency)
   - Human feedback loop
   - MLflow experiment tracking

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different review dimensions
- **Context-Aware Analysis**: Understands project structure and coding standards
- **Priority-Based Reporting**: Issues ranked by severity and impact
- **Incremental Reviews**: Review only changed code (diff-based)
- **Language Support**: Python, JavaScript, TypeScript (extensible)
- **Integration Ready**: GitHub webhooks, GitLab CI, pre-commit hooks

## 📋 Tech Stack

- **Agents**: LangChain, LangGraph, OpenAI/Anthropic LLMs
- **Backend**: FastAPI, Uvicorn
- **Storage**: Vector store (FAISS/Chroma) for code embeddings
- **MLOps**: MLflow, DVC
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Frontend**: Streamlit

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-code-review-agent.git
cd ai-code-review-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 🔧 Configuration

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ai-code-review-agent
```

## 💻 Usage

### API Server

```bash
# Start the FastAPI server
uvicorn src.api.main:app --reload --port 8000
```

### Streamlit UI

```bash
# Launch the Streamlit interface
streamlit run src/ui/app.py
```

### Python SDK

```python
from src.agents.review_orchestrator import ReviewOrchestrator

# Initialize the agent
reviewer = ReviewOrchestrator()

# Review code
result = reviewer.review_code(
    code=your_code,
    language="python",
    context={"filename": "app.py"}
)

print(result.summary)
for issue in result.issues:
    print(f"{issue.severity}: {issue.message}")
```

## 📊 Evaluation Metrics

- **Review Accuracy**: Precision/Recall on identified issues
- **Coverage**: % of potential issues detected
- **Latency**: Average review time
- **User Satisfaction**: Feedback ratings

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=src tests/
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t ai-code-review-agent .

# Run container
docker run -p 8000:8000 --env-file .env ai-code-review-agent

# Or use Docker Compose
docker-compose up
```

## 📈 Roadmap

- [ ] Multi-language support (Java, Go, Rust)
- [ ] Custom rule engine for org-specific standards
- [ ] IDE plugins (VS Code, JetBrains)
- [ ] Self-learning from human feedback
- [ ] Diff-based incremental reviews
- [ ] Team collaboration features

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👤 Author

**Taiyabullah**
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub: [Your GitHub](https://github.com/yourusername)
- Email: syedtaiyabullah@gmail.com

## 🙏 Acknowledgments

Built with LangChain, LangGraph, and FastAPI. Inspired by modern code review practices and agentic AI systems.
