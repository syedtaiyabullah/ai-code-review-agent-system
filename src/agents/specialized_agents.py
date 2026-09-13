"""Specialized review agents for different aspects of code review."""

from src.agents.base_agent import BaseReviewAgent
from src.prompts import (
    BUG_DETECTOR_PROMPT,
    SECURITY_ANALYZER_PROMPT,
    PERFORMANCE_REVIEWER_PROMPT,
    QUALITY_CHECKER_PROMPT
)


class BugDetectorAgent(BaseReviewAgent):
    """Agent specialized in detecting bugs and logic errors."""
    
    def __init__(self):
        super().__init__(
            agent_name="bug_detector",
            system_prompt=BUG_DETECTOR_PROMPT
        )


class SecurityAnalyzerAgent(BaseReviewAgent):
    """Agent specialized in security vulnerability detection."""
    
    def __init__(self):
        super().__init__(
            agent_name="security_analyzer",
            system_prompt=SECURITY_ANALYZER_PROMPT
        )


class PerformanceReviewerAgent(BaseReviewAgent):
    """Agent specialized in performance optimization."""
    
    def __init__(self):
        super().__init__(
            agent_name="performance_reviewer",
            system_prompt=PERFORMANCE_REVIEWER_PROMPT
        )


class QualityCheckerAgent(BaseReviewAgent):
    """Agent specialized in code quality and best practices."""
    
    def __init__(self):
        super().__init__(
            agent_name="quality_checker",
            system_prompt=QUALITY_CHECKER_PROMPT
        )
