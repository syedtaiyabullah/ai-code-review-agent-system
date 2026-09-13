"""
Sample code showing how to use the AI Code Review Agent API.
"""

import requests
import json


# API endpoint
API_URL = "http://localhost:8000"


def review_code_snippet(code: str, language: str = "python", 
                       review_types: list = None) -> dict:
    """
    Submit code for review via API.
    
    Args:
        code: Source code to review
        language: Programming language
        review_types: Types of reviews to perform
        
    Returns:
        Review result dictionary
    """
    if review_types is None:
        review_types = ["bug", "security", "performance", "quality"]
    
    payload = {
        "code": code,
        "language": language,
        "filename": f"code.{language}",
        "review_types": review_types
    }
    
    response = requests.post(f"{API_URL}/api/v1/review", json=payload)
    response.raise_for_status()
    
    return response.json()


def main():
    """Example usage of the API."""
    
    # Example 1: Review a simple function
    code1 = '''
def divide(a, b):
    return a / b
'''
    
    print("=" * 60)
    print("Example 1: Simple Division Function")
    print("=" * 60)
    
    result1 = review_code_snippet(code1, language="python", 
                                  review_types=["bug"])
    
    print(f"\nSubmission ID: {result1['submission_id']}")
    print(f"Total Issues: {result1['total_issues']}")
    print(f"Summary: {result1['summary']}")
    
    if result1['issues']:
        print("\nIssues Found:")
        for issue in result1['issues']:
            print(f"  - [{issue['severity'].upper()}] {issue['title']}")
            print(f"    {issue['description']}")
            if issue.get('suggestion'):
                print(f"    Suggestion: {issue['suggestion']}")
    
    # Example 2: Review code with security focus
    code2 = '''
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return db.execute(query)
'''
    
    print("\n" + "=" * 60)
    print("Example 2: Login Function (Security Review)")
    print("=" * 60)
    
    result2 = review_code_snippet(code2, language="python",
                                  review_types=["security"])
    
    print(f"\nSubmission ID: {result2['submission_id']}")
    print(f"Critical Issues: {result2['critical_count']}")
    print(f"High Issues: {result2['high_count']}")
    
    if result2['issues']:
        print("\nSecurity Issues:")
        for issue in result2['issues']:
            print(f"  - {issue['title']}")
            print(f"    Line {issue.get('line_start', 'N/A')}")
            print(f"    {issue['description']}")
    
    # Example 3: Full review
    code3 = '''
import pickle

def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def process(items):
    result = []
    for i in range(len(items)):
        for j in range(len(items)):
            if items[i] > items[j]:
                result.append((items[i], items[j]))
    return result
'''
    
    print("\n" + "=" * 60)
    print("Example 3: Full Code Review")
    print("=" * 60)
    
    result3 = review_code_snippet(code3, language="python",
                                  review_types=["bug", "security", 
                                              "performance", "quality"])
    
    print(f"\nSubmission ID: {result3['submission_id']}")
    print(f"Review Time: {result3['review_time_seconds']:.2f}s")
    print(f"Model Used: {result3['model_used']}")
    print(f"\nIssue Breakdown:")
    print(f"  Critical: {result3['critical_count']}")
    print(f"  High: {result3['high_count']}")
    print(f"  Medium: {result3['medium_count']}")
    print(f"  Low: {result3['low_count']}")
    
    print(f"\nAgents Executed: {', '.join(result3['agents_executed'])}")
    
    # Save full result to file
    with open('review_result.json', 'w') as f:
        json.dump(result3, f, indent=2)
    print("\nFull result saved to review_result.json")


if __name__ == "__main__":
    # Make sure API is running first!
    try:
        health = requests.get(f"{API_URL}/health")
        if health.status_code == 200:
            print("✓ API is running")
            print()
            main()
        else:
            print("✗ API returned error")
    except requests.exceptions.ConnectionError:
        print("✗ API is not running!")
        print("\nPlease start the API first:")
        print("  uvicorn src.api.main:app --reload")
