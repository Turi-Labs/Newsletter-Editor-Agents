from crewai import LLM, Agent, Task, Crew
import os
import yaml
from dotenv import load_dotenv

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
    print("Kick off crew")
    result = crew.kickoff()
    print(result)
    # print(result.tasks_output[0])
    # with open('usage_metrics.txt', 'a') as f:
    #     f.write(f"Usage Metrics for Newsletter Agent:\n")
    #     f.write(str(crew.usage_metrics))
    
    # Write the newsletter content to a file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(result.tasks_output[0]))    
    

    # Extract the date from filepath
    date = filepath.split('/')[1]

    if not os.path.exists("newsletter"):
        os.makedirs("newsletter")   
    
    newsletter = str(result.tasks_output[0])
    
    # Convert markdown to HTML
    import markdown
    html_content = markdown.markdown(newsletter)    

    # Write the newsletter content to a file
    with open(f"newsletter/{date}.md", 'w', encoding='utf-8') as f:
        f.write(html_content) 

    return result.tasks_output[0]


