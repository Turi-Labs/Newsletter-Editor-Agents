from crewai import LLM, Agent, Task, Crew
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = LLM(
    model="openai/o3-mini",
    temperature=0.8,
    stop=["END"],
    seed=42
)

def generate_summary(content: str, title: str) -> str:
    summary_agent = Agent(
        role='Content Summarizer',
        goal='Create concise, informative summaries of technical content',
        backstory='''You are an expert at distilling complex technical information into clear, 
        concise summaries that capture the key points while maintaining accuracy.''',
        llm=llm,
        verbose=False
    )
    
    summary_task = Task(
        description=f'''Summarize the following content about "{title}":
        
        {content}
        
        Create a concise 2-3 paragraph summary that captures:
        1. The main point or announcement
        2. Key technical details or findings
        3. Potential significance or implications
        
        Keep your summary factual and objective.''',
        expected_output='''You are an expert at distilling complex technical information into clear, 
        concise summaries that capture the key points while maintaining accuracy.''',
        agent=summary_agent
    )
    
    crew = Crew(
        agents=[summary_agent],
        tasks=[summary_task]
    )
    
    result = crew.kickoff()
    return result.tasks_output[0]

