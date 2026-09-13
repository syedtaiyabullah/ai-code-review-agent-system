"""
Quick script to test all sample files.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from src.agents import ReviewOrchestrator


async def review_file(filepath: Path, orchestrator: ReviewOrchestrator):
    """Review a single file and print results."""
    print(f"\n{'=' * 70}")
    print(f"Reviewing: {filepath.name}")
    print('=' * 70)
    
    code = filepath.read_text()
    
    result = await orchestrator.review_code(
        code=code,
        language="python",
        filename=filepath.name,
        review_types=["bug", "security", "performance", "quality"]
    )
    
    print(f"\nSummary: {result.summary}")
    print(f"Review Time: {result.review_time_seconds:.2f}s")
    print(f"\nIssue Breakdown:")
    print(f"  Critical: {result.critical_count}")
    print(f"  High: {result.high_count}")
    print(f"  Medium: {result.medium_count}")
    print(f"  Low: {result.low_count}")
    
    if result.issues:
        print(f"\nTop 3 Issues:")
        for idx, issue in enumerate(result.issues[:3], 1):
            print(f"  {idx}. [{issue.severity.upper()}] {issue.title}")
            print(f"     Line {issue.line_start}: {issue.description[:80]}...")
    
    return result


async def main():
    """Test all sample files."""
    print("\n" + "=" * 70)
    print("AI CODE REVIEW AGENT - TESTING SAMPLES")
    print("=" * 70)
    
    orchestrator = ReviewOrchestrator()
    samples_dir = Path("samples")
    
    # Files to review
    files_to_review = [
        samples_dir / "sample_buggy_code.py",
        samples_dir / "sample_good_code.py"
    ]
    
    results = {}
    
    for filepath in files_to_review:
        if filepath.exists():
            result = await review_file(filepath, orchestrator)
            results[filepath.name] = result
        else:
            print(f"\nWarning: {filepath} not found, skipping...")
    
    # Summary comparison
    print(f"\n{'=' * 70}")
    print("COMPARISON SUMMARY")
    print('=' * 70)
    
    for filename, result in results.items():
        print(f"\n{filename}:")
        print(f"  Total Issues: {result.total_issues}")
        print(f"  Critical: {result.critical_count}")
        print(f"  High: {result.high_count}")
        print(f"  Review Time: {result.review_time_seconds:.2f}s")
    
    print(f"\n{'=' * 70}")
    print("Testing completed!")
    print('=' * 70)


if __name__ == "__main__":
    asyncio.run(main())
