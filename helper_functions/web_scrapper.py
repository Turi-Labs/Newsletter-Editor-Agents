import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_main_content(url):
    try:
        logger.info(f"Attempting to extract content from URL: {url}")
        # Send HTTP GET request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
            
        # For Hacker News specifically
        if 'news.ycombinator.com' in url:
            logger.info("Processing Hacker News specific content")
            # Find the main content - for HN item pages, this is usually the post and comments
            main_content = soup.find('tr', class_='athing')
            if main_content:
                # Get the post title
                title = main_content.find('span', class_='titleline')
                
                # Get the post text (if any)
                post_text = soup.find('div', class_='toptext')
                
                # Get comments
                comments = soup.find_all('tr', class_='comtr')
                
                # Combine the content
                content = ""
                if title:
                    content += f"Title: {title.get_text(strip=True)}\n\n"
                if post_text:
                    content += f"Post: {post_text.get_text(strip=True)}\n\n"
                
                content += "Comments:\n"
                for comment in comments:
                    comment_text = comment.find('div', class_='comment')
                    if comment_text:
                        content += f"- {comment_text.get_text(strip=True)}\n\n"
                
                logger.info("Successfully extracted Hacker News content")
                return content
        
        logger.info("Processing generic website content")
        # Generic approach for other websites
        # Try to find main content containers
        main_content = None
        for container in ['main', 'article', 'div[role="main"]', '#content', '.content', '#main', '.main']:
            main_content = soup.select(container)
            if main_content:
                break
        
        # If no specific container found, use the body
        if not main_content:
            logger.info("No specific content container found, using body")
            main_content = soup.find('body')
            
        # Extract text
        if main_content:
            if isinstance(main_content, list):
                text = "\n".join([element.get_text(separator='\n', strip=True) for element in main_content])
            else:
                text = main_content.get_text(separator='\n', strip=True)
            
            # Clean up the text
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            logger.info("Successfully extracted generic website content")
            return "\n".join(lines)
        
        logger.warning("No main content found")
        return "No main content found."
        
    except Exception as e:
        logger.error(f"Error scraping content: {str(e)}")
        return f"Error scraping content: {str(e)}"
