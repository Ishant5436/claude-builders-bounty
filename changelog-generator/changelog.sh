#!/usr/bin/env bash
# Generates a CHANGELOG.md based on git history since the last tag.

set -e

# Get the last tag, or fallback to the first commit
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)
if [ -z "$LAST_TAG" ]; then
  echo "No commits found in the repository."
  exit 1
fi

echo "Fetching commits since $LAST_TAG..."

# Output file
OUT_FILE="CHANGELOG.md"

# Fetch commit messages since the last tag
# We use standard conventional commits to categorize.
# Format: <type>: <message>

ADDED=$(git log ${LAST_TAG}..HEAD --pretty=format:"* %s (%h)" --grep="^feat:\|^add:" -i)
FIXED=$(git log ${LAST_TAG}..HEAD --pretty=format:"* %s (%h)" --grep="^fix:\|^bug:" -i)
CHANGED=$(git log ${LAST_TAG}..HEAD --pretty=format:"* %s (%h)" --grep="^refactor:\|^chore:\|^update:\|^change:\|^docs:\|^style:\|^test:\|^ci:\|^build:" -i)
REMOVED=$(git log ${LAST_TAG}..HEAD --pretty=format:"* %s (%h)" --grep="^remove:\|^rm:\|^delete:" -i)

# Clear or create the file
echo "# Changelog" > $OUT_FILE
echo "" >> $OUT_FILE
echo "## Recent Changes (Since $LAST_TAG)" >> $OUT_FILE

if [ -n "$ADDED" ]; then
    echo "" >> $OUT_FILE
    echo "### Added" >> $OUT_FILE
    echo "$ADDED" >> $OUT_FILE
fi

if [ -n "$FIXED" ]; then
    echo "" >> $OUT_FILE
    echo "### Fixed" >> $OUT_FILE
    echo "$FIXED" >> $OUT_FILE
fi

if [ -n "$CHANGED" ]; then
    echo "" >> $OUT_FILE
    echo "### Changed" >> $OUT_FILE
    echo "$CHANGED" >> $OUT_FILE
fi

if [ -n "$REMOVED" ]; then
    echo "" >> $OUT_FILE
    echo "### Removed" >> $OUT_FILE
    echo "$REMOVED" >> $OUT_FILE
fi

# Include an 'Other' section for uncategorized commits
OTHER=$(git log ${LAST_TAG}..HEAD --pretty=format:"* %s (%h)" --invert-grep --grep="^feat:\|^add:\|^fix:\|^bug:\|^refactor:\|^chore:\|^update:\|^change:\|^docs:\|^style:\|^test:\|^ci:\|^build:\|^remove:\|^rm:\|^delete:" -i)
if [ -n "$OTHER" ]; then
    echo "" >> $OUT_FILE
    echo "### Other" >> $OUT_FILE
    echo "$OTHER" >> $OUT_FILE
fi

echo "CHANGELOG.md generated successfully!"
