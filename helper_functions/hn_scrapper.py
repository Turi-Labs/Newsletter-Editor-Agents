import requests
from datetime import datetime, timedelta

def fetch_hn_posts_by_date(date_str, min_points):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")

    # Calculate start/end timestamps for the 24-hour window
    start = int(target_date.replace(hour=0, minute=0, second=0).timestamp())
    end = int((target_date + timedelta(days=1)).replace(hour=0, minute=0, second=0).timestamp())

    params = {
        "tags": "story",               # Only stories (no comments/polls)
        "numericFilters": f"created_at_i>={start},created_at_i<{end},points>={min_points}",
        "hitsPerPage": 1000,           # Max allowed per request
        "page": 0
    }

    all_posts = []
    while True:
        response = requests.get(
            "https://hn.algolia.com/api/v1/search_by_date",
            params=params
        )
        response.raise_for_status()  # Raise HTTP errors (4xx/5xx)

        data = response.json()
        hits = data.get("hits", [])
        all_posts.extend(hits)

        # Check if more pages exist
        current_page = data.get("page", 0)
        total_pages = data.get("nbPages", 0)
        if current_page + 1 >= total_pages:
            break
        params["page"] = current_page + 1

    return all_posts

# example: 2025-03-20
def write_hn_posts(date: str, p: int, filename: str):
    posts = fetch_hn_posts_by_date(date, min_points=p)

    with open(filename, "w") as f:
        for post in posts:
            title = post.get("title", "No Title")
            url = post.get("url", "No URL")
            hn_url = f"https://news.ycombinator.com/item?id={post.get('objectID')}"
            points = post.get("points", 0)
            comments = post.get("num_comments", 0)

            f.write(f"Title: {title}\n")
            f.write(f"Story URL: {url}\n")
            f.write(f"Hacker News Post URL: {hn_url}\n")
            f.write(f"Points: {points}\n")
            f.write(f"Comments: {comments}\n")
            f.write("-" * 40 + "\n")
        
        f.write("end")
        f.write(f"\nTotal number of posts: {len(posts)}")