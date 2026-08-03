# Progress Tracking

## Feature List JSON

The `feature_list.json` file is the single source of truth for progress:

```json
[
  {"name": "User can create an account with email and password", "status": "passing"},
  {"name": "User can log in with valid credentials", "status": "passing"},
  {"name": "Dashboard shows user's recent activity", "status": "pending"},
  {"name": "User can send a message in chat", "status": "pending"}
]
```

## Schema

Each feature has:
- **name**: Human-readable description of the feature/test case
- **status**: `"pending"` (not yet implemented) or `"passing"` (implemented and working)

## How the Agent Uses It

### Initializer Agent (Session 1)
Creates the file from the app specification:
```
Prompt: "Read the spec file. Create feature_list.json with all features.
         Each feature should be a testable requirement.
         Set all statuses to 'pending'."
```

### Coding Agent (Sessions 2+)
Reads the file and implements the next pending feature:
```
Prompt: "Read feature_list.json. Find the FIRST feature with status 'pending'.
         Implement it. Test it. If it works, update status to 'passing'.
         Commit your changes with git."
```

## Git as Persistence Layer

After implementing each feature, the agent commits:
```
git add -A && git commit -m "Implement: [feature name]"
```

This means:
- Code changes survive across sessions
- You can inspect the git log to see progress
- You can revert to any point if something breaks
- The agent can read git history to understand context

## Resumability

When the script restarts:
1. Check if `feature_list.json` exists
2. If yes: skip initialization, go straight to coding
3. Read the file, count pending vs passing
4. Continue from the first pending feature

```python
tests_file = project_dir / "feature_list.json"
is_first_run = not tests_file.exists()

if not is_first_run:
    with open(tests_file) as f:
        features = json.load(f)
    passing = sum(1 for f in features if f["status"] == "passing")
    pending = sum(1 for f in features if f["status"] == "pending")
    print(f"Progress: {passing}/{len(features)} features passing, {pending} pending")
```

## Completion Detection

The agent is done when all features are "passing":

```python
def is_complete(project_dir):
    with open(project_dir / "feature_list.json") as f:
        features = json.load(f)
    return all(f["status"] == "passing" for f in features)
```
