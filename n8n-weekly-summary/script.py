import os
import requests
import json
from datetime import datetime, timedelta

def get_github_activity(owner, repo, github_token=None):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    since_date = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
    
    # Get Commits
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    commits_res = requests.get(commits_url, headers=headers, params={"since": since_date})
    commits = commits_res.json() if commits_res.status_code == 200 else []
    
    # Get merged PRs
    prs_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    prs_res = requests.get(prs_url, headers=headers, params={"state": "closed", "sort": "updated", "direction": "desc"})
    all_prs = prs_res.json() if prs_res.status_code == 200 else []
    
    week_ago = datetime.utcnow() - timedelta(days=7)
    merged_prs = []
    for pr in all_prs:
        if pr.get('merged_at'):
            merged_time = datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
            if merged_time > week_ago:
                merged_prs.append(pr)
    
    # Get Issues
    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    issues_res = requests.get(issues_url, headers=headers, params={"state": "closed", "since": since_date})
    all_issues = issues_res.json() if issues_res.status_code == 200 else []
    closed_issues = [i for i in all_issues if 'pull_request' not in i]
    
    return commits, merged_prs, closed_issues

def format_activity(commits, prs, issues):
    commits_text = "\n".join([f"- {c['commit']['message'].splitlines()[0]} by {c['commit']['author']['name']}" for c in commits])
    prs_text = "\n".join([f"- #{pr['number']} {pr['title']} by {pr['user']['login']}" for pr in prs])
    issues_text = "\n".join([f"- #{i['number']} {i['title']} by {i['user']['login']}" for i in issues])
    
    return (
        commits_text or "No commits this week.",
        prs_text or "No merged PRs this week.",
        issues_text or "No closed issues this week."
    )

def generate_summary(commits_text, prs_text, issues_text, anthropic_key, language="EN"):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": anthropic_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    prompt = f"""You are a developer relations manager. Summarize the following weekly GitHub activity into an engaging narrative summary. Use the following language: {language}.

Commits:
{commits_text}

Merged PRs:
{prs_text}

Closed Issues:
{issues_text}"""

    data = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['content'][0]['text']
    else:
        raise Exception(f"Failed to call Anthropic API: {response.text}")

def send_to_discord(webhook_url, summary):
    data = {
        "content": f"**Weekly Developer Summary**\n\n{summary}"
    }
    requests.post(webhook_url, json=data)

if __name__ == "__main__":
    owner = os.getenv("GITHUB_OWNER", "claude-builders-bounty")
    repo = os.getenv("GITHUB_REPO", "claude-builders-bounty")
    github_token = os.getenv("GITHUB_TOKEN")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
    language = os.getenv("SUMMARY_LANGUAGE", "EN")
    
    if not anthropic_key or not discord_webhook:
        print("Please set ANTHROPIC_API_KEY and DISCORD_WEBHOOK_URL environment variables.")
        exit(1)
        
    print(f"Fetching GitHub activity for {owner}/{repo}...")
    commits, prs, issues = get_github_activity(owner, repo, github_token)
    
    c_text, p_text, i_text = format_activity(commits, prs, issues)
    
    print("Generating summary with Claude...")
    summary = generate_summary(c_text, p_text, i_text, anthropic_key, language)
    
    print("Sending to Discord...")
    send_to_discord(discord_webhook, summary)
    
    print("Done!")
