import os
import json
import re
from collections import Counter
from jira_utils.config.paths import CATEGORY_PATH

STOPWORDS = set([
    'the', 'is', 'in', 'at', 'to', 'a', 'an', 'and', 'of', 'for', 'on', 'with', 'this', 'that', 'by', 'as', 'from'
])

def load_existing_categories():
    if os.path.exists(CATEGORY_PATH):
        with open(CATEGORY_PATH, "r") as f:
            return json.load(f)
    return {}

def save_categories(category_map):
    with open(CATEGORY_PATH, "w") as f:
        json.dump(category_map, f, indent=2)

def infer_dynamic_categories(summaries, top_n=10):
    all_words = []
    for summary in summaries:
        tokens = re.findall(r'\w+', summary.lower())
        filtered = [w for w in tokens if w not in STOPWORDS]
        all_words.extend(filtered)
    common = Counter(all_words).most_common(top_n)
    return {word: word for word, _ in common}

def merge_categories(existing, new):
    updated = existing.copy()
    for key, value in new.items():
        if key not in existing:
            updated[key] = value + " (new)"
    return updated

def categorize_summary_dynamic(summary, keyword_map):
    words = set(re.findall(r'\w+', summary.lower())) - STOPWORDS
    for keyword in keyword_map:
        if keyword in words:
            return keyword_map[keyword]
    return "uncategorized"