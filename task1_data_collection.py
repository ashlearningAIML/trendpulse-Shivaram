# -----------------------------------------
# TrendPulse - Task 1: Fetch Data from API
# -----------------------------------------
# This script fetches top stories from HackerNews,
# categorizes them based on keywords,
# and saves the data into a JSON file.
# -----------------------------------------

import requests
import time
import json
import os
from datetime import datetime
import urllib3

# Disable SSL warnings (Mac Python fix)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base API URL
BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Required header
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keyword mapping (case-insensitive)
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# -----------------------------
# Fetch top story IDs
# -----------------------------
def get_top_story_ids():
    try:
        response = requests.get(
            f"{BASE_URL}/topstories.json",
            headers=headers,
            verify=False   # SSL fix
        )
        return response.json()[:500]
    except Exception as e:
        print("Error fetching top stories:", e)
        return []

# -----------------------------
# Fetch individual story
# -----------------------------
def get_story(story_id):
    try:
        response = requests.get(
            f"{BASE_URL}/item/{story_id}.json",
            headers=headers,
            verify=False   # SSL fix
        )
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}:", e)
        return None

# -----------------------------
# Categorize story based on title
# -----------------------------
def get_category(title):
    if not title:
        return None

    title = title.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category

    return None

# -----------------------------
# Main execution
# -----------------------------
def main():
    print("Fetching top stories...")

    story_ids = get_top_story_ids()

    collected_data = []

    # Track count per category
    category_count = {cat: 0 for cat in categories}

    for story_id in story_ids:
        story = get_story(story_id)

        if not story:
            continue

        title = story.get("title", "")
        category = get_category(title)

        if not category:
            continue

        if category_count[category] >= 25:
            continue

        record = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(record)
        category_count[category] += 1

        # Stop if all categories filled
        if all(count >= 25 for count in category_count.values()):
            break

    # Sleep once per category (requirement)
    for _ in categories:
        time.sleep(2)

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories.")
    print(f"Saved to {filename}")

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()