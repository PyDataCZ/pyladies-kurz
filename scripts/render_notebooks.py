#!/usr/bin/env python3
"""Render saved notebooks and execute a small, representative notebook set."""

from __future__ import annotations

import json
import hashlib
import re
import shutil
from pathlib import Path

from nbclient import NotebookClient
from nbconvert import HTMLExporter
import nbformat


ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lessons"
BUILD = ROOT / "_build" / "notebooks"
EXECUTED = {
    "pandas-core",
    "visualization-basics",
    "univariate-and-time-series-analysis",
    "pandas-joins",
}


def notebook_sources(path: Path) -> str:
    notebook = json.loads(path.read_text())
    return "".join(part for cell in notebook["cells"] for part in cell.get("source", []))


def validate_assets(path: Path) -> None:
    source = notebook_sources(path)
    asset_pattern = r"(?<![\w/])assets/[\w-]+(?:\.[\w-]+)*\.(?:png|jpg|jpeg|gif|svg|csv|tsv|gz|zip|html|pdf|parquet|xlsx|ods|sqlite|txt)"
    for ref in re.findall(asset_pattern, source):
        if not (path.parent / ref).is_file():
            raise SystemExit(f"missing local asset {ref} referenced by {path}")
    for ref in re.findall(r"(?:\.\./)+[\w-]+/[\w.-]+|\./[\w.-]+", source):
        target = (path.parent / ref.split("?")[0]).resolve()
        if not target.is_file():
            raise SystemExit(f"missing local asset {ref} referenced by {path}")


def render(notebook_path: Path, output_dir: Path) -> None:
    exporter = HTMLExporter(template_name="lab")
    body, _ = exporter.from_filename(str(notebook_path))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{notebook_path.stem}.html").write_text(body)


def copy_topic(topic: Path, destination: Path) -> None:
    shutil.copytree(topic, destination, dirs_exist_ok=True)


def main() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    saved = BUILD / "saved"
    executed = BUILD / "executed"
    notebooks = sorted(LESSONS.glob("*/*.ipynb"))
    if len(notebooks) != 33:
        raise SystemExit(f"expected 33 notebooks, found {len(notebooks)}")

    source_hashes = {
        path: hashlib.sha256(path.read_bytes()).digest() for path in notebooks
    }
    for source in notebooks:
        validate_assets(source)
        topic = source.parent
        target_topic = saved / topic.name
        copy_topic(topic, target_topic)
        render(target_topic / source.name, target_topic)

    for topic_name in sorted(EXECUTED):
        source_topic = LESSONS / topic_name
        target_topic = executed / topic_name
        copy_topic(source_topic, target_topic)
        primary = target_topic / f"{topic_name}.ipynb"
        notebook = nbformat.read(primary, as_version=4)
        client = NotebookClient(notebook, timeout=600, kernel_name="python3")
        client.execute(cwd=str(target_topic))
        nbformat.write(notebook, primary)
        render(primary, target_topic)
    changed = [path for path, digest in source_hashes.items() if hashlib.sha256(path.read_bytes()).digest() != digest]
    if changed:
        raise SystemExit("rendering modified source notebooks:\n" + "\n".join(map(str, changed)))
    print(f"rendered {len(notebooks)} saved notebooks and {len(EXECUTED)} executed notebooks")


if __name__ == "__main__":
    main()
