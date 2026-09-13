# Contributing to AI Code Review Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, professional, and inclusive. We welcome contributions from everyone.

## How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/yourusername/ai-code-review-agent.git
cd ai-code-review-agent
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 3. Make Changes

Follow the coding standards below.

### 4. Test Your Changes

```bash
# Run tests
pytest

# Run linting
flake8 src/
black --check src/

# Format code
black src/
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Test updates
- `chore:` - Build/dependency updates

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- OpenAI API key

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest flake8 black pytest-cov

# Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Running Locally

```bash
# Start API
uvicorn src.api.main:app --reload

# Start UI
streamlit run src/ui/app.py

# Run example
python example_usage.py
```

## Coding Standards

### Python Style

- Follow **PEP 8**
- Use **Black** for formatting (line length: 88)
- Use **type hints** for function parameters and returns
- Write **docstrings** for classes and functions

Example:

```python
def analyze_code(
    code: str,
    language: str,
    options: Optional[dict] = None
) -> ReviewResult:
    """Analyze code and return review result.
    
    Args:
        code: Source code to analyze
        language: Programming language
        options: Optional analysis options
        
    Returns:
        ReviewResult with issues found
    """
    # Implementation
    pass
```

### Project Structure

```
src/
├── agents/         # Agent implementations
├── api/            # FastAPI application
├── config/         # Configuration
├── models/         # Data models
├── prompts/        # Agent prompts
├── tools/          # Utility tools
├── ui/             # Streamlit UI
└── utils/          # Utilities

tests/
├── unit/           # Unit tests
└── integration/    # Integration tests
```

### Testing Guidelines

- Write **unit tests** for new functions/classes
- Write **integration tests** for API endpoints
- Aim for **>80% code coverage**
- Use **pytest fixtures** for common setup

Example test:

```python
def test_bug_detector_agent():
    """Test bug detection agent."""
    agent = BugDetectorAgent()
    code = "def divide(a, b):\n    return a / b"
    
    issues = await agent.analyze(
        code=code,
        language="python",
        filename="test.py"
    )
    
    assert len(issues) > 0
    assert any("division by zero" in issue.description.lower() 
               for issue in issues)
```

## Adding New Features

### Adding a New Agent

1. Create agent class in `src/agents/`:

```python
from src.agents.base_agent import BaseReviewAgent

class MyCustomAgent(BaseReviewAgent):
    def __init__(self):
        super().__init__(
            agent_name="my_custom_agent",
            system_prompt=MY_CUSTOM_PROMPT
        )
```

2. Add prompt to `src/prompts/system_prompts.py`:

```python
MY_CUSTOM_PROMPT = """
You are a custom review agent...
"""
```

3. Add to orchestrator workflow in `src/agents/review_orchestrator.py`

4. Write tests in `tests/unit/test_agents.py`

5. Update documentation

### Adding a New Review Type

1. Update `Issue` type enum in `src/models/schemas.py`
2. Create corresponding agent
3. Update API documentation
4. Add to Streamlit UI options

### Supporting a New Language

1. Add language to supported list in `src/api/main.py`
2. Test with example code in that language
3. Update documentation

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`black src/`)
- [ ] No linting errors (`flake8 src/`)
- [ ] Documentation updated
- [ ] Commit messages follow conventions

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guide
```

## Reporting Issues

### Bug Reports

Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternatives considered
- Additional context

## Documentation

### Code Documentation

- Use **docstrings** for all public functions/classes
- Include parameter descriptions
- Include return value descriptions
- Add usage examples for complex functions

### Project Documentation

- Update README.md for major features
- Update ARCHITECTURE.md for structural changes
- Update QUICKSTART.md for setup changes
- Keep CHANGELOG.md updated

## Review Process

1. Automated checks run on PR
2. Maintainer reviews code
3. Feedback provided (if needed)
4. Approval and merge
5. Release notes updated

## Questions?

- Open an issue for questions
- Check existing issues first
- Use GitHub Discussions for general questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- GitHub contributors list
- CHANGELOG.md
- Project README

Thank you for contributing! 🎉
