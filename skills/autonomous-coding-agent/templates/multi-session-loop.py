"""Multi-session autonomous coding loop.

Creates a fresh Claude SDK client per iteration so the context window
never fills up. State persists via feature_list.json + git commits.

Usage:
    python multi-session-loop.py /path/to/project --model claude-sonnet-4-20250514
"""

import asyncio
import json
import sys
from pathlib import Path

# -- CONFIGURE THESE ----------------------------------------------------------
AUTO_CONTINUE_DELAY_SECONDS = 3
# -- END CONFIG ---------------------------------------------------------------


def is_complete(project_dir: Path) -> bool:
    tests_file = project_dir / "feature_list.json"
    if not tests_file.exists():
        return False
    with open(tests_file) as f:
        features = json.load(f)
    return all(feat["status"] == "passing" for feat in features)


def print_progress(project_dir: Path) -> None:
    tests_file = project_dir / "feature_list.json"
    if not tests_file.exists():
        print("No feature_list.json yet (first run)")
        return
    with open(tests_file) as f:
        features = json.load(f)
    passing = sum(1 for f in features if f["status"] == "passing")
    pending = sum(1 for f in features if f["status"] == "pending")
    print(f"Progress: {passing}/{len(features)} passing, {pending} pending")


async def run_session(client, prompt: str, project_dir: Path) -> tuple[str, str]:
    """Run a single SDK session. Returns (status, response_text)."""
    # Replace with your actual SDK session runner
    # See sdk-client-setup.py for client creation
    raise NotImplementedError("Wire up your SDK client here")


async def run_autonomous(
    project_dir: Path,
    model: str,
    max_iterations: int | None = None,
) -> None:
    tests_file = project_dir / "feature_list.json"
    is_first_run = not tests_file.exists()
    iteration = 0

    while True:
        iteration += 1
        if max_iterations and iteration > max_iterations:
            print(f"Reached max iterations ({max_iterations})")
            break

        if is_complete(project_dir):
            print("All features passing! Done.")
            break

        print(f"\n{'='*60}")
        print(f"Iteration {iteration}")
        print_progress(project_dir)
        print(f"{'='*60}\n")

        # Fresh client = fresh context window
        # from sdk_client_setup import create_client
        # client = create_client(project_dir, model)
        client = None  # TODO: replace with create_client(...)

        if is_first_run:
            prompt = (
                "Read the spec file. Create feature_list.json with all features "
                "as testable requirements. Set all statuses to 'pending'."
            )
            is_first_run = False
        else:
            prompt = (
                "Read feature_list.json. Find the FIRST feature with status 'pending'. "
                "Implement it. Test it. If it works, update status to 'passing'. "
                "Commit your changes with git."
            )

        try:
            status, response = await run_session(client, prompt, project_dir)
        except Exception as exc:
            print(f"Session error: {exc}")
            status = "error"

        if status in ("continue", "error"):
            print(f"Waiting {AUTO_CONTINUE_DELAY_SECONDS}s before next iteration...")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python multi-session-loop.py <project_dir> [--model MODEL]")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()
    model_name = "claude-sonnet-4-20250514"

    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        model_name = sys.argv[idx + 1]

    asyncio.run(run_autonomous(project_path, model_name))
