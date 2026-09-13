"""Base agent class for all review agents."""

import json
from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import settings
from src.models import Issue


class BaseReviewAgent:
    """Base class for specialized review agents."""
    
    def __init__(self, agent_name: str, system_prompt: str):
        """Initialize the base agent.
        
        Args:
            agent_name: Name of the agent
            system_prompt: System prompt for the agent
        """
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )
    
    def _format_prompt(self, code: str, language: str, filename: str, context: str = "") -> str:
        """Format the prompt with code and metadata.
        
        Args:
            code: Source code to review
            language: Programming language
            filename: Name of the file
            context: Additional context
            
        Returns:
            Formatted prompt string
        """
        return self.system_prompt.format(
            code=code,
            language=language,
            filename=filename,
            context=context
        )
    
    def _parse_response(self, response: str, issue_type: str) -> list[Issue]:
        """Parse LLM response into Issue objects.
        
        Args:
            response: Raw LLM response
            issue_type: Type of issues (bug, security, etc.)
            
        Returns:
            List of Issue objects
        """
        try:
            # Try to extract JSON from markdown code blocks
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            # Parse JSON
            issues_data = json.loads(response)
            
            # Handle both list and dict with 'issues' key
            if isinstance(issues_data, dict) and "issues" in issues_data:
                issues_data = issues_data["issues"]
            
            if not isinstance(issues_data, list):
                issues_data = [issues_data]
            
            # Convert to Issue objects
            issues = []
            for issue_dict in issues_data:
                # Ensure type is set
                issue_dict["type"] = issue_dict.get("type", issue_type)
                
                # Validate and create Issue
                try:
                    issue = Issue(**issue_dict)
                    issues.append(issue)
                except Exception as e:
                    print(f"[{self.agent_name}] Warning: Could not parse issue: {e}")
                    continue
            
            return issues
            
        except json.JSONDecodeError as e:
            print(f"[{self.agent_name}] Error parsing JSON response: {e}")
            print(f"Response: {response[:500]}")
            return []
        except Exception as e:
            print(f"[{self.agent_name}] Unexpected error: {e}")
            return []
    
    async def analyze(
        self,
        code: str,
        language: str,
        filename: str,
        context: str = ""
    ) -> list[Issue]:
        """Analyze code and return issues.
        
        Args:
            code: Source code to review
            language: Programming language
            filename: Name of the file
            context: Additional context
            
        Returns:
            List of Issue objects
        """
        # Format prompt
        prompt = self._format_prompt(code, language, filename, context)
        
        # Call LLM
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        # Parse response
        issue_type = self.agent_name.replace("_agent", "")
        issues = self._parse_response(response.content, issue_type)
        
        print(f"[{self.agent_name}] Found {len(issues)} issues")
        return issues
