# 🚀 Quickstart Guide

Get up and running with the AI Code Review Agent in 5 minutes!

## Prerequisites

- Python 3.11+
- OpenAI API key
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-code-review-agent.git
cd ai-code-review-agent
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

## Usage

### Option 1: Run Example Script

The fastest way to see the agent in action:

```bash
python example_usage.py
```

This will review two example code snippets and show detailed results.

### Option 2: Use the API

Start the FastAPI server:

```bash
uvicorn src.api.main:app --reload
```

Then visit:
- API Documentation: http://localhost:8000/docs
- API Root: http://localhost:8000

#### Example API Request

```python
import requests

code = '''
def divide(a, b):
    return a / b
'''

response = requests.post(
    "http://localhost:8000/api/v1/review",
    json={
        "code": code,
        "language": "python",
        "filename": "math.py",
        "review_types": ["bug", "security"]
    }
)

result = response.json()
print(f"Found {result['total_issues']} issues")
for issue in result['issues']:
    print(f"- [{issue['severity']}] {issue['title']}")
```

### Option 3: Use the Streamlit UI

Launch the interactive web interface:

```bash
streamlit run src/ui/app.py
```

Then visit: http://localhost:8501

1. Paste your code in the left panel
2. Select review types (bug, security, performance, quality)
3. Click "Review Code"
4. View results in the right panel

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Start all services (API + UI + MLflow)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- API: http://localhost:8000
- UI: http://localhost:8501
- MLflow: http://localhost:5000

### Build Docker Image

```bash
docker build -t ai-code-review-agent .
docker run -p 8000:8000 --env-file .env ai-code-review-agent
```

## Testing

Run the test suite:

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=src tests/
```

## Next Steps

- **Customize Prompts**: Edit `src/prompts/system_prompts.py` to tune agent behavior
- **Add Languages**: Extend language support in the API
- **Custom Agents**: Create specialized agents for your use case
- **CI/CD Integration**: Use GitHub webhooks for automated PR reviews
- **Evaluation**: Add ground truth data and run evaluations

## Troubleshooting

### API Key Error

```
Error: OpenAI API key not found
```

**Solution**: Make sure your `.env` file has a valid `OPENAI_API_KEY`

### Module Not Found

```
ModuleNotFoundError: No module named 'langchain'
```

**Solution**: Install dependencies with `pip install -r requirements.txt`

### Port Already in Use

```
Error: Address already in use
```

**Solution**: Change the port in `.env` or stop the process using the port:

```bash
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000
```

## Support

- **Documentation**: See [README.md](README.md) for detailed docs
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions

## Example Output

```
[Orchestrator] Starting code review for example.py
[Orchestrator] Review types: bug, security, performance, quality

[bug_detector] Found 2 issues
[security_analyzer] Found 1 issues
[performance_reviewer] Found 1 issues
[quality_checker] Found 3 issues

[Orchestrator] Review complete!
[Orchestrator] Found 7 total issues: 1 high, 3 medium, 3 low severity.
[Orchestrator] Review time: 4.23s

📊 Review Summary:
   Found 7 total issues: 1 high, 3 medium, 3 low severity.

📝 Issues Found: 7
   Critical: 0
   High: 1
   Medium: 3
   Low: 3

⏱️  Review Time: 4.23s
🤖 Agents: bug_detector, security_analyzer, performance_reviewer, quality_checker
```

Happy code reviewing! 🎉
