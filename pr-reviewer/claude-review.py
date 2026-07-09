#!/usr/bin/env python3
import argparse
import os
import re
import sys
import requests

def get_pr_diff(pr_url):
    # Convert https://github.com/owner/repo/pull/123 to API URL
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_url)
    if not match:
        print("Invalid PR URL format. Expected: https://github.com/owner/repo/pull/123")
        sys.exit(1)
    owner, repo, pr_number = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    headers = {'Accept': 'application/vnd.github.v3.diff'}
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        headers['Authorization'] = f"token {github_token}"
        
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch PR diff: {response.status_code} {response.text}")
        sys.exit(1)
    return response.text

def review_diff(diff, api_key):
    prompt = f"""You are an expert code reviewer. Analyze the following pull request diff and provide a structured Markdown review comment.

The output must exactly follow this format:

### Summary of Changes
(2-3 sentences summarizing the changes)

### Identified Risks
- (List of risks, or "No major risks identified.")

### Improvement Suggestions
- (List of suggestions, or "No suggestions.")

### Confidence Score
(Low / Medium / High)

Here is the diff:
```diff
{diff}
```
"""
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "system": "You are a helpful, expert code reviewer.",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
    if response.status_code != 200:
        print(f"Failed to get review from Anthropic: {response.status_code} {response.text}")
        sys.exit(1)
        
    return response.json()['content'][0]['text']

def main():
    parser = argparse.ArgumentParser(description="Claude PR Reviewer Agent")
    parser.add_argument('--pr', required=True, help="GitHub PR URL (e.g., https://github.com/owner/repo/pull/123)")
    args = parser.parse_args()
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set the ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)
        
    diff = get_pr_diff(args.pr)
    if not diff.strip():
        print("The PR diff is empty.")
        sys.exit(0)
        
    review = review_diff(diff, api_key)
    print(review)

if __name__ == "__main__":
    main()
