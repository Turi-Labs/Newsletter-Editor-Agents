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
        with open('prompts/summary_agent.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error("prompts.yaml file not found")
        raise Exception("prompts.yaml file not found")
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise Exception(f"Error parsing YAML file: {e}")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
logger.info("API key loaded")
prompts = load_prompts()
logger.info("Prompts loaded successfully")


llm = LLM(
    model="openai/o3-mini",
    stop=["END"],
    seed=42
)

def generate_summary(content: str, title: str, link: str) -> str:
    logger.info(f"Generating summary for title: {title}")
    
    summary_agent = Agent(
        role=prompts['agent']['role'],
        goal=prompts['agent']['goal'],
        backstory=prompts['agent']['backstory'],
        llm=llm,
        verbose=False
    )
    
    summary_task = Task(
        description=prompts['task']['description'].format(title=title, content=content, link = link),
        expected_output=prompts['task']['expected_output'],
        agent=summary_agent
    )
    
    crew = Crew(
        agents=[summary_agent],
        tasks=[summary_task]
    )
    
    logger.info("Starting crew execution")
    result = crew.kickoff()
    logger.info("Crew execution completed")
    
    logger.info("Summary generation completed")
    return result.tasks_output[0]
