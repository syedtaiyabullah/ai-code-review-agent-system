# Sample Code for AI Code Review Agent

This directory contains sample code demonstrating different use cases of the AI Code Review Agent.

## 📁 Files

### 1. `sample_buggy_code.py`
**Purpose**: Intentionally buggy code for testing the review agent

**Contains**:
- Division by zero errors
- SQL injection vulnerabilities
- Resource leaks
- Hardcoded credentials
- Poor error handling
- Performance issues (O(n²) algorithms)
- Code quality problems

**Use this to**:
- Test the agent's detection capabilities
- See what kinds of issues it can find
- Demonstrate the agent's features

**Try it**:
```python
from src.agents import ReviewOrchestrator
import asyncio

async def review():
    with open('samples/sample_buggy_code.py', 'r') as f:
        code = f.read()
    
    orchestrator = ReviewOrchestrator()
    result = await orchestrator.review_code(
        code=code,
        language="python",
        filename="sample_buggy_code.py"
    )
    
    print(f"Found {result.total_issues} issues!")
    for issue in result.issues:
        print(f"- [{issue.severity}] {issue.title}")

asyncio.run(review())
```

---

### 2. `sample_good_code.py`
**Purpose**: Well-written code following best practices

**Contains**:
- Proper error handling
- Type hints
- Docstrings
- Input validation
- Parameterized queries
- Resource management (context managers)
- Efficient algorithms

**Use this to**:
- Show what clean code looks like
- Verify the agent doesn't produce false positives
- Demonstrate best practices

**Expected result**: Should have 0 or very few minor issues

---

### 3. `sample_api_usage.py`
**Purpose**: Examples of using the REST API

**Shows how to**:
- Make API requests to review code
- Handle different review types
- Parse results
- Save results to files

**Run it**:
```bash
# Terminal 1: Start API
uvicorn src.api.main:app --reload

# Terminal 2: Run samples
python samples/sample_api_usage.py
```

**Features**:
- Three different code examples
- Various review type combinations
- Result parsing and display
- Error handling

---

### 4. `sample_sdk_usage.py`
**Purpose**: Direct SDK usage without API

**Shows how to**:
- Import and use `ReviewOrchestrator` directly
- Review single files
- Batch review multiple files
- Use context for better reviews
- Focus on specific review types

**Run it**:
```bash
python samples/sample_sdk_usage.py
```

**Examples included**:
1. Basic code review
2. Security-focused review
3. Performance review
4. Batch review (multiple files)
5. Review with additional context

---

## 🚀 Quick Start

### Test Everything
```bash
# 1. Review buggy code
python -c "
import asyncio
from pathlib import Path
from src.agents import ReviewOrchestrator

async def test():
    code = Path('samples/sample_buggy_code.py').read_text()
    orchestrator = ReviewOrchestrator()
    result = await orchestrator.review_code(code, 'python', 'test.py')
    print(f'Found {result.total_issues} issues!')

asyncio.run(test())
"

# 2. Try API examples
python samples/sample_api_usage.py

# 3. Try SDK examples
python samples/sample_sdk_usage.py
```

---

## 📊 Expected Results

### `sample_buggy_code.py`
- **~10-15 issues** total
- **2-3 critical** (SQL injection, hardcoded secrets)
- **3-5 high** (division by zero, resource leaks)
- **Multiple medium/low** (code quality issues)

### `sample_good_code.py`
- **0-2 issues** (if any, likely minor quality suggestions)
- Demonstrates the agent doesn't produce false positives

---

## 🎯 Use Cases

### For Demos
1. Run `sample_sdk_usage.py` to show all capabilities
2. Compare `sample_buggy_code.py` vs `sample_good_code.py`
3. Live demo with `sample_api_usage.py`

### For Testing
1. Use `sample_buggy_code.py` to verify detection works
2. Use `sample_good_code.py` to check for false positives
3. Modify samples to test specific scenarios

### For Development
1. Use as templates for new test cases
2. Extend with more language examples
3. Add edge cases and corner cases

---

## 📝 Creating Your Own Samples

```python
# Template for new sample
code_to_review = '''
# Your code here
def your_function():
    pass
'''

# Option 1: Via SDK
from src.agents import ReviewOrchestrator
import asyncio

async def review():
    orchestrator = ReviewOrchestrator()
    result = await orchestrator.review_code(
        code=code_to_review,
        language="python",
        filename="your_code.py",
        review_types=["bug", "security", "performance", "quality"]
    )
    return result

result = asyncio.run(review())
print(result.summary)

# Option 2: Via API
import requests

response = requests.post(
    "http://localhost:8000/api/v1/review",
    json={
        "code": code_to_review,
        "language": "python",
        "review_types": ["bug", "security"]
    }
)

print(response.json())
```

---

## 🔧 Tips

1. **Start simple**: Begin with small code snippets
2. **Focus review types**: Use specific review_types for faster results
3. **Add context**: Provide context for better, more relevant reviews
4. **Batch process**: Review multiple files efficiently with SDK
5. **Save results**: Export results to JSON for analysis

---

## 📚 Next Steps

- Try reviewing your own code
- Integrate into your development workflow
- Create custom test cases
- Add samples for other languages (JavaScript, TypeScript, etc.)

---

Need help? Check:
- `../QUICKSTART.md` - Quick start guide
- `../GETTING_STARTED.md` - Detailed setup
- `../ARCHITECTURE.md` - System design
- `../example_usage.py` - Main examples
