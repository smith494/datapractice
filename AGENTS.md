# AGENTS.md — DataPractice

# CRITICAL RULES - MUST FOLLOW

## RESPONSES

- Keep responses concise and to the point - unless the user asks otherwise

## PLANNING MODE

- Always ask clarifying questions
- Never assume design, tech stack or features
- Use deep-dive sub-agents to assist with research
- Use deep-dive sub-agents to review the different aspects of your plan before presenting to the user

## CHANGE / EDIT MODE

- Never implement features yourself when possible - use sub-agents!
- Identify changes from the plan that can be implemented in parallel, and use sub-agents to implement the features efficiently
- When using sub-agents to implement features, act as a coordinator only
- Use the best model for the task - premium models for complex tasks (like coding) and mid-tier models for simpler tasks, like documentation
- After completing features (large or small), always run commands like lint, type check and next build to check code quality

## Security & Boundary Protocol

### Absolute Constraints (Never Do)

- NEVER hardcode or inline API keys, bearer tokens, passwords, private SSH keys, JWT tokens, or database connection strings
- NEVER commit, read, or print the raw contents of `.env` files to terminal outputs or logs
- NEVER bypass or disable security warning banners, linters, or git hooks
- NEVER use `eval()`, `exec()`, or pass unsanitized user inputs directly into system shells
- NEVER use `--no-verify` to bypass git hooks under any circumstance

### Credential Handling

- All secrets must be stored exclusively in `.env` files or your local secrets manager
- Ensure all `.env` files are properly included in `.gitignore` to prevent source control commits
- If a code change requires authentication, write a placeholder using `process.env.VARIABLE_NAME` (Node), `os.environ.get()` (Python), etc. Immediately add the template name to `.env.example`

### Secure Code Generation & Refactoring

- **Path Traversal Prevention:** When writing file handling routines, validate that file paths are constrained to the intended workspace. Do not use unvalidated user input to resolve file paths.
- **Dependency Management:** When adding new packages, always pin exact versions (e.g., `package@1.2.3`, not `package@latest`) to prevent dependency confusion attacks. Check the package name against typos before installing.
- **Database Queries:** Always use parameterized queries or trusted ORMs. Never concatenate strings to form SQL statements.

### Failure State Handling

- If a file read or command execution inadvertently displays a credential in the terminal output, purge your context immediately, clear your terminal history, and notify the user to rotate the credential.
- If a git hook fails due to a `detect-secrets` trigger, stop execution immediately.

## Environment

- Python 3.14.5 venv at `./.venv` — activate or use `.venv/bin/python` / `.venv/bin/pip` directly.
- Dependencies in `requirements.txt`: `faker`, `pandas`, `jupyter`.

## Commands

```sh
.venv/bin/pip install -r requirements.txt   # install deps
.venv/bin/jupyter notebook                  # launch notebook server
```

## Project

- Single notebook: `faker_data_generation.ipynb` — generates fake user data (name, email, job, address, company) via Faker, exports to `fake_data.csv`.
- No tests, no linters, no CI, no build system.

## Git Commit Workflow

When the user asks to run git add/commit/push locally:

1. Run `git add .`
2. Determine the commit message from `/shortcut`:
   - If `/shortcut` is "UA", use "AGENTS.md file has been updated with new requirement"
   - If `/shortcut` is "CA", use "Codebase has been changed"
   - If `/shortcut` is "PK", use "New package(s) has been added to the project"
   - If `/shortcut` is "DATA", use "New data has been added to the project"
   - If `/shortcut` is "REMOVE", use "Removed package(s) from the project or Codebase has been changed"
   - If `/shortcut` is empty or not provided, ask the user to type a custom commit message before proceeding
   - Otherwise, use `/shortcut` as the commit message directly
3. Run `git commit -m "<message>"`
4. Run `git push origin`
5. If any step fails, stop and report the error
