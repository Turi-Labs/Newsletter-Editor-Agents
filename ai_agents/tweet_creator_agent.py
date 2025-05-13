from crewai import LLM, Agent, Task, Crew
import os
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

def load_prompts():
    try:
        with open('prompts/tweet_creator_agent.yaml', 'r') as file:
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

class resp(BaseModel):
    tweet: str
    link: str

def create_tweet(summary: str) -> str:
    creator_agent = Agent(
        role=prompts['agent']['role'],
        goal=prompts['agent']['goal'],
        backstory=prompts['agent']['backstory'],
        llm=llm,
        verbose=False
    )
    
    creator_task = Task(
        description=prompts['task']['description'].format(summary=summary),
        expected_output=prompts['task']['expected_output'],
        agent=creator_agent,
        output_pydantic=resp
    )
    
    crew = Crew(
        agents=[creator_agent],
        tasks=[creator_task]
    )
    
    result = crew.kickoff()
    print(result)
    task_output = crew.tasks[0].output
    # print(task_output)
    # with open('usage_metrics.txt', 'a') as f:
    #     f.write(f"Usage Metrics for Summary Agent:\n")
    #     f.write(str(crew.usage_metrics))
    
    return task_output.pydantic

