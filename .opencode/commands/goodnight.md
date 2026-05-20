---
description: Stage all changes, commit, and push to origin
---

Run these git commands in order:

1. `git add .`
2. `git commit -m "<commit-message>"` — see below for how to determine the commit message
3. `git push origin`

If any command fails, stop and report the error. Do not proceed if the previous step failed.

**Determine the commit message from $ARGUMENTS:**
- If `$ARGUMENTS` is "UA", use "AGENTS.md file has been updated with new requirement"
- If `$ARGUMENTS` is "CA", use "Codebase has been changed"
- If `$ARGUMENTS` is "PK", use "New package(s) has been added to the project"
- If `$ARGUMENTS` is "DATA", use "New data has been added to the project"
- If `$ARGUMENTS` is "REMOVE", use "Removed package(s) from the project or Codebase has been changed"
- If `$ARGUMENTS` is empty or not provided, use "goodnight commit"
- Otherwise, use `$ARGUMENTS` as the commit message directly
