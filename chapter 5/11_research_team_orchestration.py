"""
Research Team Orchestration Example

This example demonstrates a sophisticated multi-agent system where specialized
agents work together to conduct comprehensive research on a given topic.

Based on the actual OpenAI Agents SDK patterns from financial_research_agent
and customer_service examples.

Usage:
    python research_team_orchestration.py
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agents import Agent, Runner, function_tool, WebSearchTool, trace, custom_span, gen_trace_id

# Load environment variables
load_dotenv()

# Ensure API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
os.environ["OPENAI_API_KEY"] = api_key


# Research Data Models (following financial_research_agent pattern)
class ResearchItem(BaseModel):
    query: str
    reason: str
    agent_type: str  # "web", "academic", "industry"


class ResearchPlan(BaseModel):
    searches: List[ResearchItem]
    approach: str
    expected_duration: str


class ResearchSummary(BaseModel):
    summary: str
    key_findings: List[str]
    source_count: int
    confidence_score: float


class FinalReport(BaseModel):
    executive_summary: str
    key_findings: List[str]
    detailed_analysis: str
    recommendations: List[str]
    limitations: List[str]
    sources_consulted: int


# Mock tools for demonstration
@function_tool
def academic_search(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """Search academic papers and research publications"""
    return [
        {
            "title": f"Academic study: {query}",
            "authors": "Dr. Smith, Dr. Johnson",
            "journal": "Journal of Advanced Research",
            "year": "2024",
            "abstract": f"This peer-reviewed study examines {query} through rigorous methodology...",
    async def _perform_search(self, search_item: ResearchItem) -> Optional[ResearchSummary]:
        """Perform a single research search with the appropriate agent"""
        
        search_input = f"""
        Search Query: {search_item.query}
        Research Purpose: {search_item.reason}
        
        Conduct thorough research and provide a comprehensive summary.
        """
        
        try:
            # Route to appropriate agent based on type
            if search_item.agent_type == "web":
                agent = web_research_agent
            elif search_item.agent_type == "academic":
                agent = academic_research_agent
            elif search_item.agent_type == "industry":
                agent = industry_research_agent
            else:
                agent = web_research_agent  # Default
            
            result = await Runner.run(agent, search_input)
            return result.final_output_as(ResearchSummary)
            
        except Exception as e:
            print(f"   ❌ Search failed for '{search_item.query}': {e}")
            return None
    
    async def _synthesize_findings(self, topic: str, research_results: List[ResearchSummary]) -> FinalReport:
        """Synthesize all research findings into a final report"""
        
        with custom_span("Synthesis Phase"):
            print("📊 Phase 3: Synthesizing findings...")
            
            # Prepare synthesis input
            findings_summary = []
            total_sources = 0
            
            for i, result in enumerate(research_results, 1):
                findings_summary.append(f"""
                Research Stream {i}:
                Summary: {result.summary}
                Key Findings: {', '.join(result.key_findings)}
                Sources: {result.source_count}
                Confidence: {result.confidence_score}
                """)
                total_sources += result.source_count
            
            synthesis_input = f"""
            Research Topic: {topic}
            Total Research Streams: {len(research_results)}
            Total Sources Consulted: {total_sources}
            
            Research Findings:
            {''.join(findings_summary)}
            
            Create a comprehensive final report that synthesizes all findings.
            Include executive summary, key insights, detailed analysis, and actionable recommendations.
            """
            
            result = await Runner.run(synthesis_agent, synthesis_input)
            final_report = result.final_output_as(FinalReport)
            
            print(f"✅ Final report generated")
            print(f"   Sources consulted: {final_report.sources_consulted}")
            print(f"   Key findings: {len(final_report.key_findings)}")
            print(f"   Recommendations: {len(final_report.recommendations)}")
            
            return final_report


async def demonstrate_research_team():
    """Demonstration of the research team in action"""
    
    # Create research manager
    manager = ResearchTeamManager()
    
    # Execute research workflow
    result = await manager.run(
        "Impact of artificial intelligence on healthcare delivery and patient outcomes",
        "healthcare executives"
    )
    
    # Display results
    print("\n" + "🎯 RESEARCH COMPLETED" + "\n" + "=" * 50)
    print(f"Executive Summary:")
    print(f"  {result.executive_summary}")
    
    print(f"\nKey Findings ({len(result.key_findings)}):")
    for i, finding in enumerate(result.key_findings, 1):
        print(f"  {i}. {finding}")
    
    print(f"\nRecommendations ({len(result.recommendations)}):")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"  {i}. {rec}")
    
    print(f"\nSources Consulted: {result.sources_consulted}")
    
    if result.limitations:
        print(f"\nLimitations:")
        for limitation in result.limitations:
            print(f"  - {limitation}")
    
    print(f"\nDetailed Analysis Preview:")
    print(f"  {result.detailed_analysis[:300]}...")
    
    return result


if __name__ == "__main__":
    print("🚀 Research Team Orchestration Demo")
    print("=" * 50)
    print("This demo shows a multi-agent research team using actual SDK patterns")
    print("from the financial_research_agent and customer_service examples.\n")
    
    # Run the demonstration
    asyncio.run(demonstrate_research_team())
