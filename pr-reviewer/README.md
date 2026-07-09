# Claude PR Reviewer Agent

A Claude Code sub-agent that takes a PR diff as input, analyzes it, and returns a structured Markdown review comment.

## Setup

1. Clone this repository or copy `claude-review.py`.
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Set your Anthropic API key:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```
4. (Optional) Set your GitHub token to avoid API rate limits:
   ```bash
   export GITHUB_TOKEN="your-github-token"
   ```

## Usage (CLI)

Run the script providing a GitHub PR URL:

```bash
./claude-review.py --pr https://github.com/owner/repo/pull/123
```

The script will fetch the PR diff and generate a structured review using Claude.

## Usage (GitHub Action)

You can easily integrate this reviewer into your GitHub Actions workflow. Create a file `.github/workflows/claude-review.yml` in your repository:

```yaml
name: Claude PR Reviewer

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: pip install requests
        
      - name: Run Claude Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_URL: ${{ github.event.pull_request.html_url }}
        run: |
          curl -sO https://raw.githubusercontent.com/claude-builders-bounty/claude-builders-bounty/main/pr-reviewer/claude-review.py
          chmod +x claude-review.py
          ./claude-review.py --pr "$PR_URL" > review.md
          
      - name: Comment PR
        uses: thollander/actions-comment-pull-request@v2
        with:
          filePath: review.md
```

Remember to add `ANTHROPIC_API_KEY` to your repository secrets.
