"""File Search Tool Example

Shows how to use FileSearchTool for document analysis:
- FileSearchTool for searching uploaded documents
- Vector store integration for semantic search
- Document citations and references
- Knowledge base querying capabilities

Usage:
    python 04_file_search.py
"""

import asyncio
from agents import Agent, Runner, FileSearchTool

# Create document assistant with file search
document_assistant = Agent(
    name="Document Assistant",
    instructions="""You are a document research assistant. Search through 
    uploaded documents to find relevant information and provide detailed 
    answers with specific citations from the documents.""",
    tools=[
        FileSearchTool(
            vector_store_ids=["vs_abc123"],
            max_num_results=5,
            include_search_results=True,
        )
    ],
)

# Create legal research assistant
legal_assistant = Agent(
    name="Legal Research Assistant", 
    instructions="""You are a legal research assistant specializing in contract analysis.
    Search through legal documents to find relevant clauses, precedents, and 
    regulatory information. Always cite specific document sections.""",
    tools=[
        FileSearchTool(
            vector_store_ids=["vs_legal456"],
            max_num_results=3,
            include_search_results=True,
        )
    ],
)

# Create policy analyst
policy_analyst = Agent(
    name="Policy Analyst",
    instructions="""You are a policy analyst who reviews organizational policies 
    and procedures. Search through policy documents to answer compliance questions
    and provide guidance based on official documentation.""",
    tools=[
        FileSearchTool(
            vector_store_ids=["vs_policy789"],
            max_num_results=4,
            include_search_results=True,
        )
    ],
)

async def demo_file_search():
    """Demonstrate file search across different document types"""
    
    queries = [
        ("document_assistant", "What are the key findings from the quarterly report?"),
        ("legal_assistant", "Find clauses related to intellectual property rights"),
        ("document_assistant", "Summarize the main recommendations from the research paper"),
        ("policy_analyst", "What is the company policy on remote work arrangements?"),
        ("legal_assistant", "Search for any liability limitations in the contracts"),
        ("policy_analyst", "Find information about data retention policies")
    ]
    
    print("📄 FILE SEARCH DEMONSTRATION")
    print("Using FileSearchTool for document analysis and knowledge retrieval")
    print("=" * 70)
    
    for i, (agent_type, query) in enumerate(queries, 1):
        # Select appropriate agent
        if agent_type == "document_assistant":
            agent = document_assistant
        elif agent_type == "legal_assistant":
            agent = legal_assistant
        else:
            agent = policy_analyst
        
        print(f"\n{i}️⃣ Agent: {agent.name}")
        print(f"Query: {query}")
        print("-" * 50)
        
        try:
            result = await Runner.run(agent, query)
            print(f"Response: {result.final_output}")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Note: This requires actual vector stores with uploaded documents")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_file_search())
