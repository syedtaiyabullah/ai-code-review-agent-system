"""
Sample code showing direct SDK usage (without API).
Import and use the ReviewOrchestrator directly.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from src.agents import ReviewOrchestrator


async def example_basic_review():
    """Example 1: Basic code review."""
    print("=" * 60)
    print("Example 1: Basic Code Review")
    print("=" * 60)
    
    code = '''
def calculate_total(items):
    sum = 0
    for item in items:
        sum += item
    return sum
'''
    
    orchestrator = ReviewOrchestrator()
    result = await orchestrator.review_code(
        code=code,
        language="python",
        filename="calculator.py",
        review_types=["bug", "quality"]
    )
    
    print(f"\nSummary: {result.summary}")
    print(f"Issues found: {result.total_issues}")
    print(f"Review time: {result.review_time_seconds:.2f}s")


async def example_security_focused():
    """Example 2: Security-focused review."""
    print("\n" + "=" * 60)
    print("Example 2: Security-Focused Review")
    print("=" * 60)
    
    code = '''
import os
import subprocess

def run_command(user_input):
    os.system(user_input)
    
def execute_query(user_id):
    query = f"DELETE FROM users WHERE id = {user_id}"
    db.execute(query)
    
API_KEY = "sk-1234567890abcdef"
'''
    
    orchestrator = ReviewOrchestrator()
    result = await orchestrator.review_code(
        code=code,
        language="python",
        filename="dangerous.py",
        review_types=["security"]
    )
    
    print(f"\nCritical Issues: {result.critical_count}")
    print(f"High Issues: {result.high_count}")
    
    for issue in result.issues:
        print(f"\n[{issue.severity.upper()}] {issue.title}")
        print(f"  Line {issue.line_start}: {issue.description}")
        if issue.suggestion:
            print(f"  Fix: {issue.suggestion}")


async def example_performance_review():
    """Example 3: Performance review."""
    print("\n" + "=" * 60)
    print("Example 3: Performance Review")
    print("=" * 60)
    
    code = '''
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates

def build_string(items):
    result = ""
    for item in items:
        result += str(item) + ","
    return result

def search(data, target):
    for item in data:
        if item == target:
            return True
    return False
'''
    
    orchestrator = ReviewOrchestrator()
    result = await orchestrator.review_code(
        code=code,
        language="python",
        filename="slow_code.py",
        review_types=["performance"]
    )
    
    print(f"\nPerformance Issues: {result.total_issues}")
    
    for idx, issue in enumerate(result.issues, 1):
        print(f"\n{idx}. {issue.title} (Line {issue.line_start})")
        print(f"   {issue.description}")
        if issue.suggestion:
            print(f"   Optimization: {issue.suggestion}")


async def example_batch_review():
    """Example 4: Review multiple files."""
    print("\n" + "=" * 60)
    print("Example 4: Batch Review Multiple Files")
    print("=" * 60)
    
    files = {
        "auth.py": '''
def check_password(password):
    if password == "admin123":
        return True
    return False
''',
        "database.py": '''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute(query)
''',
        "utils.py": '''
def divide(a, b):
    return a / b

def average(numbers):
    return sum(numbers) / len(numbers)
'''
    }
    
    orchestrator = ReviewOrchestrator()
    
    for filename, code in files.items():
        print(f"\nReviewing: {filename}")
        result = await orchestrator.review_code(
            code=code,
            language="python",
            filename=filename,
            review_types=["bug", "security"]
        )
        
        print(f"  Issues: {result.total_issues} "
              f"(Critical: {result.critical_count}, "
              f"High: {result.high_count})")


async def example_with_context():
    """Example 5: Review with additional context."""
    print("\n" + "=" * 60)
    print("Example 5: Review with Context")
    print("=" * 60)
    
    code = '''
def process_payment(amount, user_id):
    balance = get_balance(user_id)
    if balance >= amount:
        balance -= amount
        update_balance(user_id, balance)
        return True
    return False
'''
    
    context = """
This is a payment processing function in a banking application.
It handles user payments and must be thread-safe and secure.
Multiple users can make payments concurrently.
"""
    
    orchestrator = ReviewOrchestrator()
    result = await orchestrator.review_code(
        code=code,
        language="python",
        filename="payment.py",
        context=context,
        review_types=["bug", "security"]
    )
    
    print(f"\nContext-aware review completed")
    print(f"Issues found: {result.total_issues}")
    
    for issue in result.issues:
        print(f"\n- {issue.title}")
        print(f"  {issue.description}")


async def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("AI CODE REVIEW AGENT - SDK USAGE EXAMPLES")
    print("=" * 70 + "\n")
    
    await example_basic_review()
    await example_security_focused()
    await example_performance_review()
    await example_batch_review()
    await example_with_context()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
