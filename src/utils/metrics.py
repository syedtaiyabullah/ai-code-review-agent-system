"""Metrics and evaluation utilities for code review quality."""

from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path


@dataclass
class ReviewMetrics:
    """Metrics for evaluating code review quality."""
    
    submission_id: str
    timestamp: datetime
    
    # Latency metrics
    total_time_seconds: float
    agent_times: Dict[str, float]
    
    # Issue metrics
    total_issues: int
    issues_by_severity: Dict[str, int]
    issues_by_type: Dict[str, int]
    
    # Model metrics
    model_used: str
    total_tokens: int = 0
    
    # Quality metrics (if ground truth available)
    precision: float = None
    recall: float = None
    f1_score: float = None
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary."""
        return {
            "submission_id": self.submission_id,
            "timestamp": self.timestamp.isoformat(),
            "total_time_seconds": self.total_time_seconds,
            "agent_times": self.agent_times,
            "total_issues": self.total_issues,
            "issues_by_severity": self.issues_by_severity,
            "issues_by_type": self.issues_by_type,
            "model_used": self.model_used,
            "total_tokens": self.total_tokens,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score
        }
    
    def save(self, path: Path):
        """Save metrics to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


class MetricsTracker:
    """Track and aggregate metrics across multiple reviews."""
    
    def __init__(self, save_dir: str = "data/metrics"):
        """Initialize metrics tracker.
        
        Args:
            save_dir: Directory to save metrics
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_history: List[ReviewMetrics] = []
    
    def log_review(self, metrics: ReviewMetrics):
        """Log review metrics.
        
        Args:
            metrics: Review metrics to log
        """
        self.metrics_history.append(metrics)
        
        # Save individual review
        metrics_file = self.save_dir / f"{metrics.submission_id}.json"
        metrics.save(metrics_file)
    
    def get_summary_stats(self) -> dict:
        """Get summary statistics across all reviews.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.metrics_history:
            return {}
        
        total_reviews = len(self.metrics_history)
        
        # Average latency
        avg_time = sum(m.total_time_seconds for m in self.metrics_history) / total_reviews
        
        # Average issues
        avg_issues = sum(m.total_issues for m in self.metrics_history) / total_reviews
        
        # Issues by severity
        severity_totals = {}
        for metrics in self.metrics_history:
            for severity, count in metrics.issues_by_severity.items():
                severity_totals[severity] = severity_totals.get(severity, 0) + count
        
        # Quality metrics (if available)
        precision_scores = [m.precision for m in self.metrics_history if m.precision is not None]
        recall_scores = [m.recall for m in self.metrics_history if m.recall is not None]
        f1_scores = [m.f1_score for m in self.metrics_history if m.f1_score is not None]
        
        return {
            "total_reviews": total_reviews,
            "average_time_seconds": round(avg_time, 2),
            "average_issues_per_review": round(avg_issues, 2),
            "total_issues_by_severity": severity_totals,
            "average_precision": round(sum(precision_scores) / len(precision_scores), 3) if precision_scores else None,
            "average_recall": round(sum(recall_scores) / len(recall_scores), 3) if recall_scores else None,
            "average_f1": round(sum(f1_scores) / len(f1_scores), 3) if f1_scores else None
        }
    
    def save_summary(self):
        """Save summary statistics to file."""
        summary = self.get_summary_stats()
        summary_file = self.save_dir / "summary.json"
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)


def calculate_quality_metrics(
    predicted_issues: List[dict],
    ground_truth_issues: List[dict],
    match_threshold: float = 0.8
) -> Dict[str, float]:
    """Calculate precision, recall, and F1 for issue detection.
    
    Args:
        predicted_issues: Issues found by the agent
        ground_truth_issues: Known ground truth issues
        match_threshold: Similarity threshold for matching issues
        
    Returns:
        Dictionary with precision, recall, and F1 scores
    """
    if not ground_truth_issues:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}
    
    if not predicted_issues:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}
    
    # Simple matching based on type and line numbers
    true_positives = 0
    
    for gt_issue in ground_truth_issues:
        for pred_issue in predicted_issues:
            # Check if types match
            if gt_issue.get("type") == pred_issue.get("type"):
                # Check if line numbers are close
                gt_line = gt_issue.get("line_start", 0)
                pred_line = pred_issue.get("line_start", 0)
                
                if abs(gt_line - pred_line) <= 2:  # Within 2 lines
                    true_positives += 1
                    break
    
    precision = true_positives / len(predicted_issues) if predicted_issues else 0
    recall = true_positives / len(ground_truth_issues) if ground_truth_issues else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1_score, 3),
        "true_positives": true_positives,
        "false_positives": len(predicted_issues) - true_positives,
        "false_negatives": len(ground_truth_issues) - true_positives
    }
