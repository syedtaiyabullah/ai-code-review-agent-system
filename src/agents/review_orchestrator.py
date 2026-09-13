"""Main orchestrator using LangGraph for multi-agent code review workflow."""

import asyncio
import uuid
from datetime import datetime
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from src.config import settings
from src.models import Issue, ReviewResult
from src.agents.specialized_agents import (
    BugDetectorAgent,
    SecurityAnalyzerAgent,
    PerformanceReviewerAgent,
    QualityCheckerAgent
)


class WorkflowState(TypedDict):
    """State for the LangGraph workflow."""
    code: str
    language: str
    filename: str
    context: str
    review_types: List[str]
    bug_issues: List[Issue]
    security_issues: List[Issue]
    performance_issues: List[Issue]
    quality_issues: List[Issue]
    all_issues: List[Issue]
    summary: str
    agents_executed: List[str]


class ReviewOrchestrator:
    """Orchestrates multi-agent code review workflow using LangGraph."""
    
    def __init__(self):
        """Initialize the orchestrator with specialized agents."""
        self.bug_agent = BugDetectorAgent()
        self.security_agent = SecurityAnalyzerAgent()
        self.performance_agent = PerformanceReviewerAgent()
        self.quality_agent = QualityCheckerAgent()
        
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=settings.temperature
        )
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for code review.
        
        Returns:
            Compiled StateGraph workflow
        """
        # Define the state graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes for each agent
        workflow.add_node("bug_detector", self._run_bug_detector)
        workflow.add_node("security_analyzer", self._run_security_analyzer)
        workflow.add_node("performance_reviewer", self._run_performance_reviewer)
        workflow.add_node("quality_checker", self._run_quality_checker)
        workflow.add_node("aggregator", self._aggregate_results)
        
        # Define the workflow edges
        workflow.set_entry_point("bug_detector")
        
        if settings.enable_parallel_agents:
            # Parallel execution: all agents run independently
            workflow.add_edge("bug_detector", "security_analyzer")
            workflow.add_edge("security_analyzer", "performance_reviewer")
            workflow.add_edge("performance_reviewer", "quality_checker")
            workflow.add_edge("quality_checker", "aggregator")
        else:
            # Sequential execution
            workflow.add_edge("bug_detector", "security_analyzer")
            workflow.add_edge("security_analyzer", "performance_reviewer")
            workflow.add_edge("performance_reviewer", "quality_checker")
            workflow.add_edge("quality_checker", "aggregator")
        
        workflow.add_edge("aggregator", END)
        
        # Compile the graph
        return workflow.compile()
    
    async def _run_bug_detector(self, state: WorkflowState) -> WorkflowState:
        """Run bug detection agent.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with bug issues
        """
        if "bug" not in state["review_types"]:
            return state
        
        print("[Orchestrator] Running Bug Detector...")
        issues = await self.bug_agent.analyze(
            code=state["code"],
            language=state["language"],
            filename=state["filename"],
            context=state.get("context") or ""
        )
        
        return {
            **state,
            "bug_issues": issues,
            "agents_executed": state.get("agents_executed", []) + ["bug_detector"]
        }
    
    async def _run_security_analyzer(self, state: WorkflowState) -> WorkflowState:
        """Run security analysis agent.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with security issues
        """
        if "security" not in state["review_types"]:
            return state
        
        print("[Orchestrator] Running Security Analyzer...")
        issues = await self.security_agent.analyze(
            code=state["code"],
            language=state["language"],
            filename=state["filename"],
            context=state.get("context") or ""
        )
        
        return {
            **state,
            "security_issues": issues,
            "agents_executed": state.get("agents_executed", []) + ["security_analyzer"]
        }
    
    async def _run_performance_reviewer(self, state: WorkflowState) -> WorkflowState:
        """Run performance review agent.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with performance issues
        """
        if "performance" not in state["review_types"]:
            return state
        
        print("[Orchestrator] Running Performance Reviewer...")
        issues = await self.performance_agent.analyze(
            code=state["code"],
            language=state["language"],
            filename=state["filename"],
            context=state.get("context") or ""
        )
        
        return {
            **state,
            "performance_issues": issues,
            "agents_executed": state.get("agents_executed", []) + ["performance_reviewer"]
        }
    
    async def _run_quality_checker(self, state: WorkflowState) -> WorkflowState:
        """Run code quality checker agent.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with quality issues
        """
        if "quality" not in state["review_types"]:
            return state
        
        print("[Orchestrator] Running Quality Checker...")
        issues = await self.quality_agent.analyze(
            code=state["code"],
            language=state["language"],
            filename=state["filename"],
            context=state.get("context") or ""
        )
        
        return {
            **state,
            "quality_issues": issues,
            "agents_executed": state.get("agents_executed", []) + ["quality_checker"]
        }
    
    async def _aggregate_results(self, state: WorkflowState) -> WorkflowState:
        """Aggregate and prioritize all issues.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with aggregated results
        """
        print("[Orchestrator] Aggregating results...")
        
        # Combine all issues
        all_issues = (
            state.get("bug_issues", []) +
            state.get("security_issues", []) +
            state.get("performance_issues", []) +
            state.get("quality_issues", [])
        )
        
        # Sort by severity (critical > high > medium > low > info)
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        all_issues.sort(key=lambda x: severity_order.get(x.severity, 5))
        
        # Generate summary
        issue_counts = {
            "critical": sum(1 for i in all_issues if i.severity == "critical"),
            "high": sum(1 for i in all_issues if i.severity == "high"),
            "medium": sum(1 for i in all_issues if i.severity == "medium"),
            "low": sum(1 for i in all_issues if i.severity == "low"),
            "info": sum(1 for i in all_issues if i.severity == "info")
        }
        
        # Create summary
        summary_parts = []
        if issue_counts["critical"] > 0:
            summary_parts.append(f"{issue_counts['critical']} critical")
        if issue_counts["high"] > 0:
            summary_parts.append(f"{issue_counts['high']} high")
        if issue_counts["medium"] > 0:
            summary_parts.append(f"{issue_counts['medium']} medium")
        if issue_counts["low"] > 0:
            summary_parts.append(f"{issue_counts['low']} low")
        
        if summary_parts:
            summary = f"Found {len(all_issues)} total issues: {', '.join(summary_parts)} severity."
        else:
            summary = "No issues found. Code looks good!"
        
        return {
            **state,
            "all_issues": all_issues,
            "summary": summary
        }
    
    async def review_code(
        self,
        code: str,
        language: str = "python",
        filename: str = "unnamed.py",
        context: str = None,
        review_types: list[str] = None
    ) -> ReviewResult:
        """Execute the complete code review workflow.
        
        Args:
            code: Source code to review
            language: Programming language
            filename: File name
            context: Additional context
            review_types: Types of reviews to perform
            
        Returns:
            ReviewResult with all findings
        """
        start_time = datetime.utcnow()
        
        # Default review types
        if review_types is None:
            review_types = ["bug", "security", "performance", "quality"]
        
        # Initialize state as dict
        initial_state = {
            "code": code,
            "language": language,
            "filename": filename,
            "context": context,
            "review_types": review_types,
            "bug_issues": [],
            "security_issues": [],
            "performance_issues": [],
            "quality_issues": [],
            "all_issues": [],
            "summary": "",
            "agents_executed": []
        }
        
        print(f"\n[Orchestrator] Starting code review for {filename}")
        print(f"[Orchestrator] Review types: {', '.join(review_types)}")
        
        # Execute workflow
        final_state = await self.workflow.ainvoke(initial_state)
        
        # Handle dict or AgentState response
        if isinstance(final_state, dict):
            all_issues = final_state.get("all_issues", [])
            summary = final_state.get("summary", "")
            agents_executed = final_state.get("agents_executed", [])
        else:
            all_issues = final_state.all_issues
            summary = final_state.summary
            agents_executed = final_state.agents_executed
        
        # Calculate metrics
        end_time = datetime.utcnow()
        review_time = (end_time - start_time).total_seconds()
        
        issue_counts = {
            "critical": sum(1 for i in all_issues if i.severity == "critical"),
            "high": sum(1 for i in all_issues if i.severity == "high"),
            "medium": sum(1 for i in all_issues if i.severity == "medium"),
            "low": sum(1 for i in all_issues if i.severity == "low")
        }
        
        # Create result
        result = ReviewResult(
            submission_id=f"rev_{uuid.uuid4().hex[:8]}",
            timestamp=start_time,
            language=language,
            filename=filename,
            issues=all_issues,
            summary=summary,
            total_issues=len(all_issues),
            critical_count=issue_counts["critical"],
            high_count=issue_counts["high"],
            medium_count=issue_counts["medium"],
            low_count=issue_counts["low"],
            review_time_seconds=review_time,
            model_used=settings.default_model,
            agents_executed=agents_executed
        )
        
        print(f"\n[Orchestrator] Review complete!")
        print(f"[Orchestrator] {result.summary}")
        print(f"[Orchestrator] Review time: {review_time:.2f}s")
        
        return result
