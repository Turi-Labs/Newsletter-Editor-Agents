import re
from typing import List, Dict
from agents.filter_agent import run
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_hn_posts(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content by the separator (dashed lines)
    post_sections = re.split(r'-{3,}', content)
    
    posts = []
    for section in post_sections:
        # Skip empty sections or the final "end Total number of posts" section
        if not section.strip() or "end\nTotal number of posts:" in section:
            continue
        
        # Extract post information
        post_info = {}
        lines = section.strip().split('\n')
        
        for line in lines:
            if line.startswith('Title:'):
                post_info['title'] = line.replace('Title:', '').strip()
            elif line.startswith('Story URL:'):
                post_info['story_url'] = line.replace('Story URL:', '').strip()
            elif line.startswith('Hacker News Post URL:'):
                post_info['hn_url'] = line.replace('Hacker News Post URL:', '').strip()
            elif line.startswith('Points:'):
                post_info['points'] = line.replace('Points:', '').strip()
            elif line.startswith('Comments:'):
                post_info['comments'] = line.replace('Comments:', '').strip()
        
        if post_info:
            posts.append(post_info)
    
    return posts

def format_post(post: Dict[str, str]) -> str:
    return f"""Title: {post.get('title', '')}
            Story URL: {post.get('story_url', '')}
            Hacker News Post URL: {post.get('hn_url', '')}
            Points: {post.get('points', '')}
            Comments: {post.get('comments', '')}"""

def process_posts(file_path: str) -> List[str]:
    posts = parse_hn_posts(file_path)
    results = []
    
    logger.info(f"Found {len(posts)} posts to process")
    
    for i, post in enumerate(posts):
        logger.info(f"Processing post {i+1}/{len(posts)}: {post.get('title', '')[:50]}...")
        formatted_post = format_post(post)
        result = run(formatted_post)
        results.append({
            'title': post.get('title', ''),
            'link': post.get('story_url', ''),
            'result': result,
            'hn_url': post.get('hn_url', ''),
            'is_ai_related': 'True' in result  # Simple check if the result contains 'True'
        })
        logger.info(f"Result: {result}\n")
    
    return results

def save_results(results: List[Dict], output_file: str) -> None:
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# Hacker News AI Content Analysis Results\n\n")

        # Write detailed results
        file.write("## Detailed Results\n\n")
        for i, result in enumerate(results):
            if(result['is_ai_related']):
                file.write("------\n")
                file.write(f"### {i+1}. {result['title']}\n")
                file.write(f"Link: {result['link']}\n")
                file.write(f"Hn Link: {result['hn_url']}\n")

                
        # Count AI-related posts
        ai_related = sum(1 for r in results if r.get('is_ai_related', False))
        file.write("------\n")
        file.write(f"Total posts analyzed: {len(results)}\n")
        file.write(f"AI-related posts: {ai_related} ({ai_related/len(results)*100:.1f}%)\n\n")

def filter(input_file: str, output_file: str):
    try:
        results = process_posts(input_file)
        save_results(results, output_file)
        logger.info(f"Analysis complete! Results saved to {output_file}")
        
        # Print summary
        ai_related = sum(1 for r in results if r.get('is_ai_related', False))
        logger.info(f"\nSummary:")
        logger.info(f"Total posts analyzed: {len(results)}")
        logger.info(f"AI-related posts: {ai_related} ({ai_related/len(results)*100:.1f}%)")
        
    except Exception as e:
        logger.error(f"Error processing posts: {e}")