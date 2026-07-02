"""Reasoning - Chain-of-thought and analysis capabilities."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

from llm.client import LLMClient


@dataclass
class ReasoningStep:
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None
    result: Optional[Any] = None


class Reasoner:
    """Chain-of-thought reasoning engine."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
    
    async def think(self, problem: str, max_steps: int = 10) -> List[ReasoningStep]:
        """Perform chain-of-thought reasoning."""
        steps = []
        current_state = problem
        
        for i in range(max_steps):
            step = await self._reasoning_step(current_state, steps)
            steps.append(step)
            
            if step.result:
                break
            
            current_state = step.observation or step.thought
        
        return steps
    
    async def _reasoning_step(
        self, state: str, history: List[ReasoningStep]
    ) -> ReasoningStep:
        """Execute a single reasoning step."""
        history_text = self._format_history(history) if history else "No previous steps."
        
        prompt = f"""Problem: {state}

Previous reasoning:
{history_text}

Think step by step. What is the next thought? If you have reached a conclusion, state it clearly."""
        
        response = self.llm.complete(prompt)
        return ReasoningStep(thought=response)


class Analyzer:
    """Analyze text, code, and documents."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
    
    def analyze(
        self, content: str, analysis_types: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Analyze content with specified analysis types."""
        if analysis_types is None:
            analysis_types = ['key_points', 'sentiment', 'structure']
        
        results = {}
        for analysis_type in analysis_types:
            results[analysis_type] = self._perform_analysis(content, analysis_type)
        
        return results
    
    def _perform_analysis(self, content: str, analysis_type: str) -> str:
        """Perform a specific type of analysis."""
        prompts = {
            'key_points': f"""Extract the key points from this content:

{content}

List the main ideas and important details.""",
            
            'sentiment': f"""Analyze the sentiment of this content:

{content}

Provide a sentiment analysis with explanation.""",
            
            'structure': f"""Analyze the structure of this content:

{content}

Describe the organization and how ideas are presented."""
        }
        
        prompt = prompts.get(analysis_type, f"Analyze this content:\n{content}")
        return self.llm.complete(prompt)
    
    def _format_history(self, history: List[ReasoningStep]) -> str:
        """Format reasoning history for prompt."""
        return "\n".join(
            f"Step {i+1}: {step.thought}" + 
            (f"\n  Observation: {step.observation}" if step.observation else "")
            for i, step in enumerate(history)
        )