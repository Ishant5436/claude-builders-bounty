# Changelog Generator

A simple bash script that automatically generates a structured `CHANGELOG.md` from your project's git history since the last tag.

## How it Works
The script fetches all commits since the last git tag (or the first commit if no tags exist). It auto-categorizes them into `Added`, `Fixed`, `Changed`, and `Removed` based on conventional commit prefixes (e.g., `feat:`, `fix:`, `refactor:`).

## Setup in 3 Steps
1. Make the script executable:
   ```bash
   chmod +x changelog.sh
   ```
2. Place `changelog.sh` in the root of your git repository.
3. Run the script to generate `CHANGELOG.md`:
   ```bash
   ./changelog.sh
   ```
