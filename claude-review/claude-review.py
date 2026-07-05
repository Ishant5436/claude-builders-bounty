#!/usr/bin/env python3
import argparse
import urllib.request
import urllib.error
import json
import os
import sys

def fetch_diff(pr_url):
    # GitHub conveniently provides diffs by appending .diff to the PR URL
    diff_url = pr_url.rstrip("/") + ".diff"
    req = urllib.request.Request(diff_url)
    
    # If a GITHUB_TOKEN is present, use it to avoid rate limits
    gh_token = os.environ.get("GITHUB_TOKEN")
    if gh_token:
        req.add_header("Authorization", f"Bearer {gh_token}")
        
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error fetching diff: {e}")
        sys.exit(1)

def analyze_with_claude(diff_content):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is missing.")
        sys.exit(1)
        
    url = "https://api.anthropic.com/v1/messages"
    
    prompt = f"""You are an expert software engineer reviewing a pull request.
Here is the git diff of the PR:

```diff
{diff_content[:80000]} # Truncate if extremely large, though Anthropic context handles much more
```

Analyze the code changes and provide a structured Markdown review.
Your response MUST strictly include the following sections and nothing else:

### Summary of Changes
(2-3 sentences summarizing the PR)

### Identified Risks
- (list potential bugs, security issues, or regressions)

### Improvement Suggestions
- (list actionable code improvements or refactors)

### Confidence Score
(Low / Medium / High)
"""

    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", "2023-06-01")
    req.add_header("content-type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            return res_json['content'][0]['text']
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"Anthropic API Error: {e.code} {e.reason}")
        print(error_body)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Claude PR Review Agent")
    parser.add_argument("--pr", required=True, help="GitHub Pull Request URL (e.g., https://github.com/owner/repo/pull/123)")
    args = parser.parse_args()
    
    print(f"Fetching diff for {args.pr}...")
    diff_text = fetch_diff(args.pr)
    
    if not diff_text.strip():
        print("Diff is empty. Nothing to review.")
        sys.exit(0)
        
    print("Analyzing diff with Claude...")
    review = analyze_with_claude(diff_text)
    
    print("\n--- Review Output ---\n")
    print(review)
    print("\n---------------------\n")

if __name__ == "__main__":
    main()
