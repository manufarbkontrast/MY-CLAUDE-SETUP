"""Feature list management for autonomous coding agents.

Provides helpers to create, read, update, and check completion of
the feature_list.json that drives multi-session progress.

Usage:
    from feature_tracker import FeatureTracker

    tracker = FeatureTracker(Path("./my-project"))
    tracker.create_from_spec(["User can sign up", "User can log in"])
    tracker.mark_passing("User can sign up")
    print(tracker.summary())
"""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Feature:
    name: str
    status: str  # "pending" | "passing"


class FeatureTracker:
    """Manages the feature_list.json file."""

    def __init__(self, project_dir: Path) -> None:
        self.path = project_dir / "feature_list.json"

    # -- Read ------------------------------------------------------------------

    def exists(self) -> bool:
        return self.path.exists()

    def load(self) -> list[Feature]:
        with open(self.path) as f:
            raw = json.load(f)
        return [Feature(name=item["name"], status=item["status"]) for item in raw]

    def next_pending(self) -> Feature | None:
        for feat in self.load():
            if feat.status == "pending":
                return feat
        return None

    def is_complete(self) -> bool:
        return all(feat.status == "passing" for feat in self.load())

    # -- Write (immutable: always writes a new file) ---------------------------

    def create_from_spec(self, feature_names: list[str]) -> list[Feature]:
        features = [Feature(name=name, status="pending") for name in feature_names]
        self._save(features)
        return features

    def mark_passing(self, feature_name: str) -> list[Feature]:
        updated = [
            Feature(name=feat.name, status="passing")
            if feat.name == feature_name
            else feat
            for feat in self.load()
        ]
        self._save(updated)
        return updated

    # -- Summary ---------------------------------------------------------------

    def summary(self) -> str:
        features = self.load()
        passing = sum(1 for f in features if f.status == "passing")
        pending = sum(1 for f in features if f.status == "pending")
        total = len(features)
        return f"{passing}/{total} passing, {pending} pending"

    # -- Internal --------------------------------------------------------------

    def _save(self, features: list[Feature]) -> None:
        data = [{"name": f.name, "status": f.status} for f in features]
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)


# -- Standalone usage ----------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python feature-tracker.py <project_dir>")
        sys.exit(1)

    tracker = FeatureTracker(Path(sys.argv[1]))

    if not tracker.exists():
        print("No feature_list.json found.")
        sys.exit(1)

    print(tracker.summary())
    next_feat = tracker.next_pending()
    if next_feat:
        print(f"Next pending: {next_feat.name}")
    else:
        print("All features passing!")
