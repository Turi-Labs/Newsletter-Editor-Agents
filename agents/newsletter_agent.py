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

def craft_newsletter(research_notes: str, filepath: str):
    newsletter_writer = Agent(
        role='Professional Newsletter Editor',
        goal='Create an engaging, well-structured newsletter from research notes',
        backstory='''
        You are an experienced newsletter editor with expertise in transforming complex research notes
        into clear, engaging, and well-organized newsletters. You excel at identifying key themes,
        maintaining consistency in tone, and presenting information in a reader-friendly format.
        Your strength lies in creating compelling narratives while maintaining accuracy and attention to detail.
        ''',
        llm=llm,
        verbose=False
    )

    newsletter_task = Task(
        description=f'''
        Using the provided research notes, create a comprehensive newsletter that:
        1. Starts with an engaging executive summary
        2. Organizes information into clear, logical sections
        3. Highlights key findings and insights
        4. Includes relevant statistics and data points
        5. Maintains a professional yet accessible tone
        6. Ends with key takeaways or action items

        Research Notes to process:
        {research_notes}
        ''',
        expected_output='''
        A well-formatted newsletter with:
        - Title
        - Executive Summary
        - Main Content (organized in sections)
        - Key Takeaways
        - Call to Action (if applicable)

        The newsletter should be detailed yet concise, maintaining professional language while being
        accessible to a general audience. Format using appropriate markdown for readability.
        ''',
        agent=newsletter_writer
    )
    
    crew = Crew(
        agents=[newsletter_writer],
        tasks=[newsletter_task]
    )
    
    result = crew.kickoff()
    # print(result.tasks_output[0])

    # Write the newsletter content to a file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result.tasks_output[0])    
    
    return result.tasks_output[0]


