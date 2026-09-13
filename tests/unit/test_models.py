"""Unit tests for data models."""

import pytest
from src.models import Issue, CodeSubmission, ReviewResult
from datetime import datetime


def test_issue_creation():
    """Test Issue model creation."""
    issue = Issue(
        type="bug",
        severity="high",
        title="Null pointer exception",
        description="Variable may be None",
        line_start=10,
        line_end=12,
        suggestion="Add null check"
    )
    
    assert issue.type == "bug"
    assert issue.severity == "high"
    assert issue.line_start == 10


def test_code_submission_defaults():
    """Test CodeSubmission with defaults."""
    submission = CodeSubmission(code="print('hello')")
    
    assert submission.language == "python"
    assert submission.filename == "unnamed.py"
    assert "bug" in submission.review_types
    assert "security" in submission.review_types


def test_review_result_creation():
    """Test ReviewResult creation."""
    result = ReviewResult(
        submission_id="test_123",
        language="python",
        filename="test.py",
        summary="Test summary",
        review_time_seconds=2.5,
        model_used="gpt-4o-mini"
    )
    
    assert result.submission_id == "test_123"
    assert result.total_issues == 0
    assert result.review_time_seconds == 2.5


def test_issue_validation():
    """Test Issue validation."""
    # Valid severity
    issue = Issue(
        type="security",
        severity="critical",
        title="SQL Injection",
        description="Vulnerable query"
    )
    assert issue.severity == "critical"
    
    # Invalid severity should raise error
    with pytest.raises(ValueError):
        Issue(
            type="bug",
            severity="invalid",
            title="Test",
            description="Test"
        )
