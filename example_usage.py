"""Example usage of the AI Code Review Agent."""

import asyncio
from src.agents import ReviewOrchestrator
from src.config import settings


# Example 1: Simple code with issues
EXAMPLE_CODE_1 = '''
def calculate_average(numbers):
    sum = 0
    for num in numbers:
        sum += num
    return sum / len(numbers)

def get_user_by_id(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return result
'''

# Example 2: More complex code
EXAMPLE_CODE_2 = '''
import pickle
import os

def load_config(filename):
    with open(filename, 'rb') as f:
        config = pickle.load(f)
    return config

def process_data(data):
    results = []
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] > data[j]:
                results.append((data[i], data[j]))
    return results

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        self.users[username] = password
    
    def verify_user(self, username, password):
        return self.users.get(username) == password
'''


async def main():
    """Run example code reviews."""
    
    print("=" * 80)
    print("AI CODE REVIEW AGENT - EXAMPLE USAGE")
    print("=" * 80)
    print(f"\nModel: {settings.default_model}")
    print(f"Parallel Agents: {settings.enable_parallel_agents}\n")
    
    # Initialize orchestrator
    orchestrator = ReviewOrchestrator()
    
    # Example 1: Review simple code
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Simple Code with Common Issues")
    print("=" * 80)
    print("\nCode:")
    print(EXAMPLE_CODE_1)
    print("\n" + "-" * 80)
    
    result1 = await orchestrator.review_code(
        code=EXAMPLE_CODE_1,
        language="python",
        filename="example1.py",
        review_types=["bug", "security", "quality"]
    )
    
    print(f"\n[Review Summary]:")
    print(f"   {result1.summary}")
    print(f"\n[Issues Found]: {result1.total_issues}")
    print(f"   Critical: {result1.critical_count}")
    print(f"   High: {result1.high_count}")
    print(f"   Medium: {result1.medium_count}")
    print(f"   Low: {result1.low_count}")
    print(f"\n[Review Time]: {result1.review_time_seconds:.2f}s")
    print(f"[Agents]: {', '.join(result1.agents_executed)}")
    
    if result1.issues:
        print("\n" + "-" * 80)
        print("DETAILED ISSUES:")
        print("-" * 80)
        for idx, issue in enumerate(result1.issues, 1):
            print(f"\n{idx}. [{issue.severity.upper()}] {issue.title}")
            print(f"   Type: {issue.type}")
            print(f"   Description: {issue.description}")
            if issue.line_start:
                print(f"   Location: Line {issue.line_start}")
            if issue.suggestion:
                print(f"   [Suggestion]: {issue.suggestion}")
    
    # Example 2: Review more complex code
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Complex Code with Multiple Issues")
    print("=" * 80)
    print("\nCode:")
    print(EXAMPLE_CODE_2)
    print("\n" + "-" * 80)
    
    result2 = await orchestrator.review_code(
        code=EXAMPLE_CODE_2,
        language="python",
        filename="example2.py",
        review_types=["bug", "security", "performance", "quality"]
    )
    
    print(f"\n[Review Summary]:")
    print(f"   {result2.summary}")
    print(f"\n[Issues Found]: {result2.total_issues}")
    print(f"   Critical: {result2.critical_count}")
    print(f"   High: {result2.high_count}")
    print(f"   Medium: {result2.medium_count}")
    print(f"   Low: {result2.low_count}")
    print(f"\n[Review Time]: {result2.review_time_seconds:.2f}s")
    print(f"[Agents]: {', '.join(result2.agents_executed)}")
    
    if result2.issues:
        print("\n" + "-" * 80)
        print("DETAILED ISSUES (Top 5):")
        print("-" * 80)
        for idx, issue in enumerate(result2.issues[:5], 1):
            print(f"\n{idx}. [{issue.severity.upper()}] {issue.title}")
            print(f"   Type: {issue.type}")
            print(f"   Description: {issue.description}")
            if issue.line_start:
                print(f"   Location: Line {issue.line_start}")
            if issue.suggestion:
                print(f"   [Suggestion]: {issue.suggestion}")
    
    print("\n" + "=" * 80)
    print("EXAMPLES COMPLETED")
    print("=" * 80)
    print("\nTo use the API:")
    print("  1. Start the API: uvicorn src.api.main:app --reload")
    print("  2. Start the UI: streamlit run src/ui/app.py")
    print("  3. Visit: http://localhost:8501")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
