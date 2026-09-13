# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-14

### Added
- Initial release of AI Code Review Agent
- Multi-agent architecture using LangGraph
- Four specialized review agents:
  - Bug Detector Agent
  - Security Analyzer Agent
  - Performance Reviewer Agent
  - Code Quality Checker Agent
- FastAPI REST API with endpoints:
  - POST /api/v1/review - Submit code for review
  - GET /api/v1/supported-languages - List supported languages
  - GET /api/v1/review-types - List review types
  - GET /health - Health check
- Interactive Streamlit UI with:
  - Code editor
  - Real-time review results
  - Issue filtering
  - Severity visualization
- Configuration management with Pydantic Settings
- Comprehensive testing suite:
  - Unit tests for models and agents
  - Integration tests for API
- Docker deployment support:
  - Dockerfile for containerization
  - Docker Compose with API, UI, and MLflow
- CI/CD pipeline with GitHub Actions
- Metrics and evaluation framework
- Structured logging
- OpenAI LLM integration via LangChain
- Documentation:
  - README with overview and features
  - QUICKSTART guide
  - ARCHITECTURE documentation
  - CONTRIBUTING guidelines
- Example usage script with sample code reviews

### Supported Languages
- Python
- JavaScript
- TypeScript
- Java
- Go
- Rust
- C++
- C

### Review Types
- Bug Detection
- Security Analysis
- Performance Review
- Code Quality

## [Unreleased]

### Planned
- Multi-file project analysis
- Diff-based incremental reviews
- GitHub integration for PR reviews
- IDE plugins (VS Code, JetBrains)
- Custom rule engine
- Self-learning from feedback
- Additional language support
- Vector-based code similarity detection
- Code fix suggestions with diffs
