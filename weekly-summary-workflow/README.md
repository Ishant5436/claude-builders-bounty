# Weekly GitHub Repo Summary (n8n Workflow)

This n8n workflow automates the generation of a weekly narrative summary for a GitHub repository. It fetches commits, closed issues, and merged PRs from the past 7 days, feeds them into Claude 3.5 Sonnet, and posts the resulting summary to a Discord channel.

## Features
- **Exportable n8n workflow** (.json file format)
- **Schedule Trigger:** Runs every Friday at 5:00 PM (`0 17 * * 5`).
- **Claude Integration:** Utilizes `claude-3-5-sonnet-20241022` to generate a high-quality summary.
- **Discord Integration:** Delivers the summary seamlessly via a Discord Webhook.
- **Configurable Variables:** Easily change the target GitHub repo, Discord Webhook, and output Language (EN/FR).

## Setup Instructions (4 Steps)

1. **Import the Workflow:** In your n8n workspace, click **"Add Workflow"**, select **"Import from File"**, and upload `workflow.json`.
2. **Configure Anthropic Credentials:** Open the `Claude API` node, click **"Select Credentials"**, and add your Anthropic API Key.
3. **Set Configuration Variables:** Open the `Config` node and update the three string variables:
   - `github_repo`: Your target repository (e.g., `owner/repo`).
   - `discord_webhook`: Your Discord channel's webhook URL.
   - `language`: The language for the summary (e.g., `EN`, `FR`).
4. **Activate:** Toggle the workflow to **Active** (top right corner) to run it automatically every Friday, or click **"Execute Workflow"** to test it immediately.
