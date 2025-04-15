from agents.summary_agent import generate_summary
from helper_functions.web_scrapper import extract_main_content

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
        
        # Extract HN link
        elif line.startswith('Hn Link: '):
            current_hn_link = line.replace('Hn Link: ', '').strip()
            
            # If we have both title and link, add them to our results
            if current_title and current_hn_link:
                links.append((current_title, current_hn_link))
                current_title = None
                current_hn_link = None
    
    return links

def get_links(filename: str):
    with open(filename, 'r') as file:
        content = file.read()
    # Get the links
    extracted_links = extract_links_from_results(content)
    # print(extracted_links)
    return extracted_links

# Send links to the extract method
def get_link_content(extracted_links):
    content = []
    for title, link in extracted_links:
        print(link)
        c = extract_main_content(link)
        # print(c)
        content.append((title, c))
    return content

# Send summaries to ai agent
def send_to_ai(content):
    summaries = []
    for title, text in content:
        summary = generate_summary(text, title)
        summaries.append(summary)
    return summaries

