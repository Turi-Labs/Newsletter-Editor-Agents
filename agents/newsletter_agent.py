from crewai import LLM, Agent, Task, Crew
import os
import yaml
from dotenv import load_dotenv
import markdown
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_prompts():
    try:
        with open('prompts/newsletter_agent.yaml', 'r') as file:
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

def craft_newsletter(research_notes: str, filepath: str):
    newsletter_writer = Agent(
        role=prompts['agent']['role'],
        goal=prompts['agent']['goal'],
        backstory=prompts['agent']['backstory'],
        llm=llm,
        verbose=False
    )

    newsletter_task = Task(
        description=prompts['task']['description'].format(research_notes=research_notes),
        expected_output=prompts['task']['expected_output'],
        agent=newsletter_writer
    )
    
    crew = Crew(
        agents=[newsletter_writer],
        tasks=[newsletter_task]
    )
    logger.info("Starting crew execution")
    result = crew.kickoff()
    logger.info(result)
    
    # Write the newsletter content to a file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(result.tasks_output[0]))    
    
    logger.info(f"Newsletter content written to {filepath}")

    # Extract the date from filepath
    date = filepath.split('/')[1]

    if not os.path.exists("newsletter"):
        os.makedirs("newsletter")   
    
    newsletter = str(result.tasks_output[0])
    
    # Convert markdown to HTML
    html_content = markdown.markdown(newsletter)    

    # Write the newsletter content to a file
    logger.info(f"Writing HTML content to newsletter/{date}.md")
    with open(f"newsletter/{date}.md", 'w', encoding='utf-8') as f:
        f.write(html_content)
    logger.info(f"Successfully wrote content to newsletter/{date}.md")
        
    logger.info("Newsletter generation completed")
    return result.tasks_output[0]
