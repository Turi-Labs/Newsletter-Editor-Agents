from typing import cast
from pydantic import BaseModel, Field
from crewai import LLM, Agent, Task, Crew
import os
import yaml
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = LLM(
    model="openai/o3-mini",
    temperature=0.8,
    stop=["END"],
    seed=42
)

class Agent1Format(BaseModel):
    flag: bool

def run(input):
    agent1 = Agent(
        role='AI News Analyst specializing in Hacker News',
        goal='Filter Hacker News posts to identify the most significant and impactful AI news, research, and projects.',
        backstory='''You are an expert AI analyst programmed to scan Hacker News, discerning true signals from noise.
        You understand the typical markers of important announcements, breakthrough research, and high-impact community projects within the AI field.
        You prioritize substance over hype and focus on identifying posts that truly matter for staying informed about AI advancements.''',
        llm=llm,
        verbose=True
    )


    task1 = Task(
        description=f'''Analyze a the string: {input}. 
        
        Based *only* on the title and links, evaluate if the post likely falls into one of the priority categories:
        
        1.  **Significant News & Announcements:** Major product launches (e.g., new models/news from OpenAI, Google, Anthropic), significant updates, major funding rounds, acquisitions, important policy/regulation news related to AI from key players or governments. Look for official sources mentioned or implied.
        2.  **Breakthrough Research & Papers:** Posts indicating influential research papers (e.g., mentioning arXiv, new techniques, architectures, benchmark results that suggest a leap forward). Look for terms like "new model," "state-of-the-art," "novel technique."
        3.  **High-Impact "Show HN" Projects:** Potential new open-source tools, libraries, datasets, or compelling AI applications shared by creators that seem to solve a real problem, demonstrate a novel capability, or could gain significant traction. Look for "Show HN" tag and descriptions implying usefulness or innovation.

        Exclude minor updates, tutorials, general discussions, opinion pieces, small personal projects unless they clearly signal high impact.
        Input: A list of Hacker News post titles.
        ''',
        agent=agent1,
        expected_output='''For each post title provided in the input, determine if it meets the criteria for a high-priority item (True) or not (False).
        Output the result as a boolean
        ''',
        output_pydantic=Agent1Format
    )

    
    # Create crew and execute
    crew = Crew(
        agents=[agent1],
        tasks=[task1]
    )
    
    results = crew.kickoff()
    
    print(results)

    agent1 = results.tasks_output[0]
    # print(type(agent1))
    # Print task outputs
    print("Task 1 Output:", agent1)
    # print(crew.usage_metrics)
    return str(agent1)

