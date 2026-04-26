#!/usr/bin/env python3
"""
TRIBE v2 — Merch test runner

Predicts brain response to one or more stimuli (video / image / text / audio),
saves predictions as numpy arrays, and renders cortical activation plots.

Usage:
    python3 test_merch.py                    # runs all built-in samples
    python3 test_merch.py <path-or-url>      # runs single custom asset
    python3 test_merch.py --video v.mp4 --text "Limited drop. Only 100 pieces."

Output (in ./outputs/):
    <stem>_preds.npy        — (T, ~20484) cortical predictions
    <stem>_segments.csv     — timeline of stimulus segments
    <stem>_brain.png        — cortical heatmap snapshot
    <stem>_summary.json     — per-region stats (mean, peak, peak_time)
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np


CACHE = Path("./cache")
OUT = Path("./outputs")
CACHE.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)


SAMPLES = {
    "video_blender": {
        "kind": "video",
        "url": "https://download.blender.org/durian/trailer/sintel_trailer-480p.mp4",
    },
    "text_marketing": {
        "kind": "text",
        "content": (
            "Drop incoming. Friday 18:00 CET. 100 pieces only. "
            "Hand-printed in Berlin. Sign up for the early link."
        ),
    },
    "text_neutral": {
        "kind": "text",
        "content": (
            "The annual report covers fiscal year revenue, expenses, "
            "and operational metrics across all business units."
        ),
    },
}


def load_model():
    """Load TribeModel — first call downloads ~30 GB of weights."""
    from tribev2.demo_utils import TribeModel

    print("[load] TribeModel.from_pretrained('facebook/tribev2') — first run downloads weights...")
    t0 = time.time()
    model = TribeModel.from_pretrained("facebook/tribev2", cache_folder=CACHE)
    print(f"[load] done in {time.time() - t0:.1f}s")
    return model


def load_plotter():
    from tribev2.plotting import PlotBrain
    return PlotBrain(mesh="fsaverage5")


def prepare_input(model, *, video_path=None, text=None, audio_path=None, image_path=None):
    """Build events DataFrame from one or more inputs."""
    kwargs = {}
    if video_path:
        kwargs["video_path"] = Path(video_path)
    if text:
        text_path = CACHE / f"text_{abs(hash(text)) % 10**8}.txt"
        text_path.write_text(text)
        kwargs["text_path"] = text_path
    if audio_path:
        kwargs["audio_path"] = Path(audio_path)
    if image_path:
        kwargs["image_path"] = Path(image_path)
    if not kwargs:
        raise ValueError("at least one input required")
    return model.get_events_dataframe(**kwargs)


def predict(model, events_df, label):
    print(f"[predict {label}] events: {len(events_df)} segments")
    t0 = time.time()
    preds, segments = model.predict(events=events_df)
    elapsed = time.time() - t0
    print(f"[predict {label}] preds.shape = {preds.shape}  ({elapsed:.1f}s)")
    return preds, segments


def save_outputs(label, preds, segments, plotter, n_plot_timesteps=15):
    stem = OUT / label

    np.save(f"{stem}_preds.npy", preds)
    if hasattr(segments, "to_csv"):
        segments.to_csv(f"{stem}_segments.csv", index=False)
    else:
        with open(f"{stem}_segments.json", "w") as f:
            json.dump([str(s) for s in segments], f, indent=2)

    summary = {
        "shape": list(preds.shape),
        "mean_activation": float(preds.mean()),
        "max_activation": float(preds.max()),
        "min_activation": float(preds.min()),
        "peak_timestep": int(preds.mean(axis=1).argmax()),
        "top10_vertices": np.argsort(preds.mean(axis=0))[-10:].tolist(),
        "n_timesteps": int(preds.shape[0]),
        "n_vertices": int(preds.shape[1]),
    }
    with open(f"{stem}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[save {label}] preds + segments + summary written")
    print(f"        mean={summary['mean_activation']:.4f}  max={summary['max_activation']:.4f}")

    try:
        n = min(n_plot_timesteps, preds.shape[0])
        seg = segments[:n] if hasattr(segments, "__getitem__") else segments
        fig = plotter.plot_timesteps(
            preds[:n],
            segments=seg,
            cmap="fire",
            norm_percentile=99,
            vmin=0.6,
            alpha_cmap=(0, 0.2),
            show_stimuli=True,
        )
        fig.savefig(f"{stem}_brain.png", dpi=120, bbox_inches="tight")
        print(f"[save {label}] brain heatmap → {stem}_brain.png")
    except Exception as e:
        print(f"[save {label}] plot failed: {e}")


def run_sample(model, plotter, name, spec):
    print(f"\n========== {name} ==========")
    if spec["kind"] == "video":
        from tribev2.demo_utils import download_file
        path = CACHE / f"{name}.mp4"
        if not path.exists():
            download_file(spec["url"], path)
        df = prepare_input(model, video_path=path)
    elif spec["kind"] == "text":
        df = prepare_input(model, text=spec["content"])
    elif spec["kind"] == "image":
        df = prepare_input(model, image_path=Path(spec["path"]))
    elif spec["kind"] == "audio":
        df = prepare_input(model, audio_path=Path(spec["path"]))
    else:
        print(f"unknown kind: {spec['kind']}")
        return
    preds, segments = predict(model, df, name)
    save_outputs(name, preds, segments, plotter)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset", nargs="?", help="path or URL to image/video file")
    parser.add_argument("--video", help="video path")
    parser.add_argument("--image", help="image path")
    parser.add_argument("--text", help="raw text")
    parser.add_argument("--audio", help="audio path")
    parser.add_argument("--all-samples", action="store_true", help="run built-in samples")
    args = parser.parse_args()

    model = load_model()
    plotter = load_plotter()

    if args.video or args.image or args.text or args.audio:
        kwargs = {
            "video_path": args.video,
            "image_path": args.image,
            "text": args.text,
            "audio_path": args.audio,
        }
        kwargs = {k: v for k, v in kwargs.items() if v}
        df = prepare_input(model, **kwargs)
        label = Path(next(iter(kwargs.values()))).stem if not args.text else "custom_text"
        preds, segments = predict(model, df, label)
        save_outputs(label, preds, segments, plotter)
    elif args.asset:
        ext = Path(args.asset).suffix.lower()
        if ext in (".mp4", ".mov", ".avi", ".mkv", ".webm"):
            df = prepare_input(model, video_path=args.asset)
        elif ext in (".jpg", ".jpeg", ".png", ".webp"):
            df = prepare_input(model, image_path=args.asset)
        elif ext in (".wav", ".mp3", ".flac", ".m4a"):
            df = prepare_input(model, audio_path=args.asset)
        else:
            print(f"unknown extension: {ext}", file=sys.stderr)
            sys.exit(1)
        label = Path(args.asset).stem
        preds, segments = predict(model, df, label)
        save_outputs(label, preds, segments, plotter)
    else:
        for name, spec in SAMPLES.items():
            run_sample(model, plotter, name, spec)

    print("\n=== done ===")
    print(f"outputs: {OUT.resolve()}")


if __name__ == "__main__":
    main()
