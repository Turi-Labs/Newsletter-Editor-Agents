from typing import cast
from pydantic import BaseModel, Field
from crewai import LLM, Agent, Task, Crew
import os
import yaml
from dotenv import load_dotenv

def load_prompts():
    try:
        with open('prompts/filter_agent.yaml', 'r') as file:
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

class Agent1Format(BaseModel):
    flag: bool

def run(input):
    agent1 = Agent(
        role=prompts['agent']['role'],
        goal=prompts['agent']['goal'],
        backstory=prompts['agent']['backstory'],
        llm=llm,
        verbose=True
    )


    task1 = Task(
        description=prompts['task']['description'].format(input=input),
        agent=agent1,
        expected_output=prompts['task']['expected_output'],
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

