from ai_agents.summary_agent import generate_summary
from helper_functions.web_scrapper import extract_main_content
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Write code to extract all links
def extract_links_from_results(content):
    links = []
    lines = content.split('\n')
    
    current_title = None
    current_hn_link = None
    
    for line in lines:
        # Extract title (starts with ###)
        if line.startswith('### '):
            current_title = line.replace('### ', '').strip()
        
        elif line.startswith('Link: '):
            current_link = line.replace('Link: ', '').strip()
        
        # Extract HN link
        elif line.startswith('Hn Link: '):
            current_hn_link = line.replace('Hn Link: ', '').strip()
            
            # If we have both title and link, add them to our results
            if current_title and current_hn_link:
                links.append((current_title, current_hn_link, current_link))
                current_title = None
                current_hn_link = None
                current_link = None
    
    return links

def get_links(filename: str):
    logger.info(f"Reading links from file: {filename}")
    with open(filename, 'r') as file:
        content = file.read()
    # Get the links
    extracted_links = extract_links_from_results(content)
    logger.info(f"Extracted {len(extracted_links)} links from file")
    return extracted_links

# Send links to the extract method
def get_link_content(extracted_links):
    content = []
    for title, hn_link, link in extracted_links:
        logger.info(f"Extracting content from link: {link}")
        c = extract_main_content(hn_link)
        content.append((title, c, link))
    return content

# Send summaries to ai agent
def send_to_ai(content):
    summaries = []
    for title, text, link in content:
        logger.info(f"Generating summary for: {title}")
        summary = generate_summary(text, title, link)
        summaries.append(summary)
    return summaries
