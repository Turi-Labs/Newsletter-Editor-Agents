from crewai import LLM, Agent, Task, Crew
import os
import yaml
from dotenv import load_dotenv

def load_prompts():
    try:
        with open('prompts/summary_agent.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise Exception("prompts.yaml file not found")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing YAML file: {e}")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
prompts = load_prompts()


llm = LLM(
    model="openai/o3-mini",
    temperature=0.8,
    stop=["END"],
    seed=42
)

def generate_summary(content: str, title: str) -> str:
    summary_agent = Agent(
        role=prompts['agent']['role'],
        goal=prompts['agent']['goal'],
        backstory=prompts['agent']['backstory'],
        llm=llm,
        verbose=False
    )
    
    summary_task = Task(
        description=prompts['task']['description'].format(title=title, content=content),
        expected_output=prompts['task']['expected_output'],
        agent=summary_agent
    )
    
    crew = Crew(
        agents=[summary_agent],
        tasks=[summary_task]
    )
    
    result = crew.kickoff()

    with open('usage_metrics.txt', 'a') as f:
        f.write(f"Usage Metrics for Summary Agent:\n")
        f.write(str(crew.usage_metrics))
    
    return result.tasks_output[0]

