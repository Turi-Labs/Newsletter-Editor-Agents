from typing import cast
from pydantic import BaseModel, Field
from crewai import LLM, Agent, Task, Crew
import os
import yaml
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_prompts():
    try:
        with open('prompts/filter_agent.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise Exception("prompts.yaml file not found")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing YAML file: {e}")

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
logger.info(f"Using API key")
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
        verbose=False
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
    
    logger.info(results)

    agent1 = results.tasks_output[0]
    
    return str(agent1)
