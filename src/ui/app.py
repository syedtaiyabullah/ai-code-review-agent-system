"""Streamlit UI for AI Code Review Agent."""

import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .severity-critical { color: #ff0000; font-weight: bold; }
    .severity-high { color: #ff6600; font-weight: bold; }
    .severity-medium { color: #ff9900; }
    .severity-low { color: #3399ff; }
    .severity-info { color: #999999; }
    .issue-card {
        border-left: 4px solid #ccc;
        padding: 10px;
        margin: 10px 0;
        background-color: #f9f9f9;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)


def get_severity_color(severity: str) -> str:
    """Get color for severity level."""
    colors = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🔵",
        "info": "⚪"
    }
    return colors.get(severity, "⚪")


def main():
    """Main Streamlit application."""
    
    # Header
    st.title("🤖 AI Code Review Agent")
    st.markdown("**Intelligent multi-agent code review powered by LLMs**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Language selection
        languages = ["python", "javascript", "typescript", "java", "go", "rust", "cpp", "c"]
        language = st.selectbox(
            "Programming Language",
            languages,
            index=0
        )
        
        # Filename
        filename = st.text_input(
            "File Name",
            value=f"code.{language}",
            help="Name of the file being reviewed"
        )
        
        # Review types
        st.subheader("Review Types")
        review_bug = st.checkbox("🐛 Bug Detection", value=True)
        review_security = st.checkbox("🔒 Security Analysis", value=True)
        review_performance = st.checkbox("⚡ Performance Review", value=True)
        review_quality = st.checkbox("✨ Code Quality", value=True)
        
        # Additional context
        context = st.text_area(
            "Additional Context (Optional)",
            placeholder="Provide any additional context about the code...",
            height=100
        )
        
        st.divider()
        
        # API Status
        st.subheader("API Status")
        try:
            response = requests.get(f"{API_URL}/health", timeout=2)
            if response.status_code == 200:
                st.success("✅ API Connected")
                health_data = response.json()
                st.caption(f"Model: {health_data.get('model', 'N/A')}")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ API Offline")
            st.caption("Start the API with: `uvicorn src.api.main:app`")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Code Input")
        
        # Code input
        code_input = st.text_area(
            "Enter your code here:",
            height=400,
            placeholder="Paste your code here for review...",
            help="The code will be analyzed by multiple specialized agents"
        )
        
        # Submit button
        if st.button("🚀 Review Code", type="primary", use_container_width=True):
            if not code_input.strip():
                st.error("Please enter some code to review")
            else:
                # Prepare review types
                review_types = []
                if review_bug:
                    review_types.append("bug")
                if review_security:
                    review_types.append("security")
                if review_performance:
                    review_types.append("performance")
                if review_quality:
                    review_types.append("quality")
                
                if not review_types:
                    st.error("Please select at least one review type")
                else:
                    # Make API request
                    with st.spinner("🔍 Analyzing code..."):
                        try:
                            response = requests.post(
                                f"{API_URL}/api/v1/review",
                                json={
                                    "code": code_input,
                                    "language": language,
                                    "filename": filename,
                                    "context": context if context else None,
                                    "review_types": review_types
                                },
                                timeout=120
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state["review_result"] = result
                                st.success("✅ Review completed!")
                            else:
                                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                                
                        except requests.exceptions.Timeout:
                            st.error("❌ Request timed out. The code might be too complex.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.header("📊 Review Results")
        
        # Display results if available
        if "review_result" in st.session_state:
            result = st.session_state["review_result"]
            
            # Summary metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Total Issues", result["total_issues"])
            with col_m2:
                st.metric("Critical", result["critical_count"])
            with col_m3:
                st.metric("High", result["high_count"])
            with col_m4:
                st.metric("Review Time", f"{result['review_time_seconds']:.1f}s")
            
            # Summary
            st.info(f"**Summary:** {result['summary']}")
            
            # Issues
            if result["issues"]:
                st.subheader("🔍 Issues Found")
                
                # Filter by severity
                severity_filter = st.multiselect(
                    "Filter by severity:",
                    ["critical", "high", "medium", "low", "info"],
                    default=["critical", "high", "medium"]
                )
                
                filtered_issues = [
                    issue for issue in result["issues"]
                    if issue["severity"] in severity_filter
                ]
                
                # Display issues
                for idx, issue in enumerate(filtered_issues, 1):
                    severity_emoji = get_severity_color(issue["severity"])
                    
                    with st.expander(
                        f"{severity_emoji} **{issue['title']}** ({issue['severity'].upper()})",
                        expanded=(issue["severity"] in ["critical", "high"])
                    ):
                        st.markdown(f"**Type:** {issue['type'].capitalize()}")
                        st.markdown(f"**Description:** {issue['description']}")
                        
                        if issue.get("line_start"):
                            st.markdown(f"**Location:** Line {issue['line_start']}" +
                                      (f" - {issue['line_end']}" if issue.get('line_end') else ""))
                        
                        if issue.get("code_snippet"):
                            st.code(issue["code_snippet"], language=language)
                        
                        if issue.get("suggestion"):
                            st.success(f"💡 **Suggestion:** {issue['suggestion']}")
                        
                        st.caption(f"Confidence: {issue.get('confidence', 0.8):.0%}")
            else:
                st.success("🎉 No issues found! Your code looks great!")
            
            # Metadata
            with st.expander("ℹ️ Review Metadata"):
                st.json({
                    "submission_id": result["submission_id"],
                    "timestamp": result["timestamp"],
                    "model_used": result["model_used"],
                    "agents_executed": result["agents_executed"]
                })
        else:
            st.info("👈 Enter your code and click 'Review Code' to start the analysis")
            
            # Example code
            st.subheader("📚 Example")
            with st.expander("Click to see example code with issues"):
                st.code('''
def calculate_average(numbers):
    sum = 0
    for num in numbers:
        sum += num
    return sum / len(numbers)

# Issues:
# 1. Division by zero if list is empty
# 2. Using 'sum' as variable name (shadows built-in)
# 3. No input validation
                ''', language="python")


if __name__ == "__main__":
    main()
