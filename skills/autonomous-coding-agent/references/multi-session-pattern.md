# Multi-Session Pattern

## Problem
Autonomous agents exhaust their context window during long tasks. A single session cannot implement 200 features.

## Solution
Create a fresh client for each iteration. State persists through the filesystem (feature_list.json + git).

## The Outer Loop

```python
async def run_autonomous(project_dir, model, max_iterations=None):
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists()
    iteration = 0

    while True:
        iteration += 1
        if max_iterations and iteration > max_iterations:
            break

        # Fresh client = fresh context window
        client = create_client(project_dir, model)

        # Choose prompt based on session type
        if is_first_run:
            prompt = get_initializer_prompt()
            is_first_run = False
        else:
            prompt = get_coding_prompt()

        # Run session
        async with client:
            status, response = await run_session(client, prompt, project_dir)

        # Auto-continue
        if status == "continue":
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)
        elif status == "error":
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)  # Retry
```

## Key Decisions

### Fresh Client Per Iteration
Each `create_client()` call creates a new SDK client with a clean context window. The agent starts fresh but reads `feature_list.json` to know where it left off.

### Two-Agent Pattern
- **Initializer (iteration 1)**: Reads the app specification, generates `feature_list.json` with all features and test cases
- **Coding Agent (iterations 2+)**: Reads `feature_list.json`, finds next pending feature, implements it, marks it as passing

### Auto-Continue
After each session, wait `AUTO_CONTINUE_DELAY_SECONDS` (default: 3) then start a new session automatically. This keeps the agent working continuously.

### Pause/Resume
- **Pause**: Ctrl+C stops the outer loop
- **Resume**: Run the script again. It detects `feature_list.json` exists and continues from where it left off

### State Persistence
State is stored in the filesystem, not in memory:
- `feature_list.json` — which features are pending/passing
- Git commits — code changes survive across sessions
- The project directory itself — all generated files persist

### Error Recovery
On error, the loop continues with a fresh session. Since state is on disk, the new session picks up where the previous one failed.

## Timing Expectations
- First session (initializer): 10-20+ minutes for generating 200 features
- Each coding session: 5-15 minutes per feature
- Full app: Many hours across dozens of sessions
