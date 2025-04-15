## Scrape (Done):
- Action: Automatically fetch the top posts (e.g., ~200) from Hacker News daily using a script or automation tool.
- Output: A structured list of posts with Title, Story URL, HN Post URL, Points, and Comments.

## Filter (Done):
- Action: The AI agent (me) performs an initial pass on the scraped list. I'll analyze titles, source domains (from Story URLs), points, and comment counts against your criteria (AI keywords, known sources, "Show HN" tags, engagement metrics) to identify potentially relevant posts.
- Output: A shorter, prioritized list of candidate posts for deeper analysis.

## Deep Dive (Done):
- Action: For the filtered list, I'll use my tools to access and analyze the actual content behind the Story URL. This confirms relevance and allows me to accurately categorize posts as Significant News, Breakthrough Research, High-Impact Show HN, or Insightful Discussion based on the content, not just the title or link.
- Output: A curated list of confirmed relevant posts, categorized according to your priorities.

## Craft Newsletter (Done):
- Action: I take the curated, categorized list and generate concise summaries for each selected item. I'll then format these summaries along with the essential details (Title, Links, Points, Comments) into a polished structure ready for your newsletter.
- Output: The final content for your newsletter, ready to be sent out.

-----

- News/Announcements: Look for press release language, product launch details, funding amounts, policy discussions.
- Research: Identify paper structures (abstract, introduction, methodology), links to PDFs, technical jargon, mentions of benchmarks or novel techniques.
- Show HN: Assess the description, linked demo/repo, and determine if it's a genuinely useful or innovative AI tool/application.
- Insightful Discussions: While analyzing HN comments directly is harder without a dedicated API, high comment counts on a clearly AI-focused Story URL (whose content I can analyze) strongly suggests this category. I can summarize the topic being discussed based on the article.