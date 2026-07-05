# Claude Code PR Review Agent

A zero-dependency Python CLI script that automatically fetches a GitHub Pull Request diff and uses the Anthropic Claude API to generate a structured code review.

## Requirements
- Python 3.x
- Standard libraries only (no `pip install` required!)

## Setup and Usage

1. Set your Anthropic API key:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```
   *(Optional) If reviewing private repos or avoiding rate limits, also set `GITHUB_TOKEN="your-token"`.*

2. Make the script executable:
   ```bash
   chmod +x claude-review.py
   ```

3. Run the agent against a PR:
   ```bash
   ./claude-review.py --pr https://github.com/owner/repo/pull/123
   ```

## Output Format
The agent will output a Markdown-formatted review containing:
- **Summary of Changes**: 2-3 sentences summarizing the PR
- **Identified Risks**: A bulleted list of potential bugs or issues
- **Improvement Suggestions**: Actionable code improvements
- **Confidence Score**: Low / Medium / High
