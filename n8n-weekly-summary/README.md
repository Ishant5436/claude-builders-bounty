# Weekly Developer Summary

This directory contains an automated workflow to generate a weekly developer summary for a GitHub repository using Claude (`claude-sonnet-4-20250514`), and post the summary to Discord. It is provided in two flavors: an **n8n workflow** (exported JSON) and a standalone **Python script**.

## n8n Workflow Setup (5 Steps)

1. **Import the Workflow**: Open your n8n instance, click "Add Workflow", go to the top right options menu, select "Import from File", and upload `workflow.json`.
2. **Configure Repositories & Output**: Double-click the `Configuration` node (a "Set" node). Change `githubOwner`, `githubRepo`, `language` (e.g. `EN` or `FR`), and set your `discordWebhookUrl`.
3. **Set Up Credentials**: Open the `Get Commits`, `Get PRs`, and `Get Issues` nodes to create and select a "Header Auth" credential with your GitHub Token (if required for private repos). Do the same in the `Claude API` node to add your `x-api-key` Anthropic Token.
4. **Test Run**: Click the "Test Workflow" (or "Execute Workflow") button to verify that the webhook fires successfully to your Discord channel.
5. **Activate**: Toggle the workflow switch to **Active**. It will now run automatically every Friday at 5:00 PM.

## Python Script Setup (Alternative)

If you prefer to run this as a standalone script (e.g., via cron or a Claude Code task):

1. Install requirements: `pip install requests`
2. Set environment variables:
   ```bash
   export GITHUB_OWNER="claude-builders-bounty"
   export GITHUB_REPO="claude-builders-bounty"
   export GITHUB_TOKEN="<optional_for_rate_limits>"
   export ANTHROPIC_API_KEY="<your_key>"
   export DISCORD_WEBHOOK_URL="<your_discord_webhook>"
   export SUMMARY_LANGUAGE="EN"
   ```
3. Run the script: `python script.py`
