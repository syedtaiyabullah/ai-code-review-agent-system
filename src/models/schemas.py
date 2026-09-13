"""Data models and schemas for the code review system."""

from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class CodeSubmission(BaseModel):
    """Schema for code submission request."""
    
    code: str = Field(..., description="Source code to review")
    language: str = Field(default="python", description="Programming language")
    filename: str = Field(default="unnamed.py", description="File name")
    context: Optional[str] = Field(None, description="Additional context about the code")
    review_types: list[str] = Field(
        default=["bug", "security", "performance", "quality"],
        description="Types of reviews to perform"
    )


class Issue(BaseModel):
    """Schema for a single code issue."""
    
    type: Literal["bug", "security", "performance", "quality", "documentation"] = Field(
        ..., description="Category of the issue"
    )
    severity: Literal["critical", "high", "medium", "low", "info"] = Field(
        ..., description="Severity level"
    )
    title: str = Field(..., description="Short title of the issue")
    description: str = Field(..., description="Detailed description")
    line_start: Optional[int] = Field(None, description="Starting line number")
    line_end: Optional[int] = Field(None, description="Ending line number")
    code_snippet: Optional[str] = Field(None, description="Relevant code snippet")
    suggestion: Optional[str] = Field(None, description="Suggested fix or improvement")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0, description="Confidence score")


class ReviewResult(BaseModel):
    """Schema for complete review result."""
    
    submission_id: str = Field(..., description="Unique submission ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    language: str
    filename: str
    
    # Review results
    issues: list[Issue] = Field(default_factory=list)
    summary: str = Field(..., description="Overall review summary")
    
    # Metrics
    total_issues: int = Field(default=0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    medium_count: int = Field(default=0)
    low_count: int = Field(default=0)
    
    # Metadata
    review_time_seconds: float = Field(..., description="Time taken for review")
    model_used: str = Field(..., description="LLM model used")
    agents_executed: list[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "submission_id": "rev_123456",
                "language": "python",
                "filename": "app.py",
                "summary": "Found 3 issues: 1 security vulnerability, 2 code quality improvements needed.",
                "issues": [
                    {
                        "type": "security",
                        "severity": "high",
                        "title": "SQL Injection vulnerability",
                        "description": "Direct string interpolation in SQL query",
                        "line_start": 45,
                        "line_end": 47,
                        "suggestion": "Use parameterized queries instead"
                    }
                ],
                "total_issues": 3,
                "review_time_seconds": 5.2,
                "model_used": "gpt-4o-mini"
            }
        }


class AgentState(BaseModel):
    """State schema for LangGraph workflow."""
    
    # Input
    code: str
    language: str
    filename: str
    context: Optional[str] = None
    review_types: list[str]
    
    # Agent routing
    route: Optional[str] = None
    
    # Individual agent results
    bug_issues: list[Issue] = Field(default_factory=list)
    security_issues: list[Issue] = Field(default_factory=list)
    performance_issues: list[Issue] = Field(default_factory=list)
    quality_issues: list[Issue] = Field(default_factory=list)
    
    # Final output
    all_issues: list[Issue] = Field(default_factory=list)
    summary: str = ""
    agents_executed: list[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
