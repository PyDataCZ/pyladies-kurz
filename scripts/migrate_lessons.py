#!/usr/bin/env python3
"""Migrate the legacy lessons/pydata tree to semantic lesson directories."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lessons"
LEGACY = LESSONS / "pydata"

MAPPING = {
    "api": "api",
    "classification_bonus": "classification-bonus",
    "classification_metrics": "classification-metrics",
    "classification_resume": "classification-summary",
    "clt": "central-limit-theorem",
    "dashboards": "dashboards",
    "databases": "databases",
    "eda-univariate-timeseries": "univariate-and-time-series-analysis",
    "homework_revisited": "homework-revisited",
    "install": "installation",
    "intro_classification": "classification-introduction",
    "intro_regression": "regression-introduction",
    "ml1_home_prep": "machine-learning-home-preparation",
    "multivariate": "multivariate-analysis",
    "notebook": "jupyter-notebook",
    "null_and_outliers": "missing-values-and-outliers",
    "pandas": "pandas-basics",
    "pandas_core": "pandas-core",
    "pandas_correlations": "pandas-correlations",
    "pandas_groupby": "pandas-groupby",
    "pandas_joins": "pandas-joins",
    "pandas_types": "pandas-data-types",
    "pca": "principal-component-analysis",
    "profiling": "pandas-profiling",
    "regression_exercises": "regression-exercises",
    "regression_metrics": "regression-metrics",
    "regression_resume": "regression-summary",
    "scikitlearn_api": "scikit-learn-api",
    "scikitlearn_resume": "scikit-learn-summary",
    "univariate": "univariate-analysis",
    "visualization_basics": "visualization-basics",
    "webscraping": "web-scraping",
}

MARKDOWN_TOPICS = {"classification_resume", "install", "ml1_home_prep", "notebook", "scikitlearn_resume"}

AUXILIARY = {
    ("clt", "images.ipynb"): "generate-images.ipynb",
    ("eda-univariate-timeseries", "reseni.ipynb"): "solutions.ipynb",
    ("eda-univariate-timeseries", "weather_data.ipynb"): "prepare-weather-data.ipynb",
    ("homework_revisited", "index_na_hodinu.ipynb"): "classroom-version.ipynb",
    ("homework_revisited", "index_na_hodinu_2025.ipynb"): "classroom-version-2025.ipynb",
    ("regression_exercises", "static/excercise.ipynb"): "population-exercise.ipynb",
}


def destination(source_name: str) -> Path:
    return LESSONS / MAPPING[source_name]


def expected_primary(source_name: str) -> str:
    suffix = ".md" if source_name in MARKDOWN_TOPICS else ".ipynb"
    return f"{MAPPING[source_name]}{suffix}"


def rewritten(text: str, topic: str, asset_names: set[str]) -> str:
    text = text.replace(
        "http://github.com/simecek/naucse.python.cz/blob/master/lessons/pydata/pca/static/protein_expr.zip?raw=true",
        "assets/protein_expr.zip",
    )
    text = text.replace(
        "http://github.com/simecek/naucse.python.cz/blob/master/lessons/pydata/pca/static/ML_small.csv?raw=true",
        "assets/ML_small.csv",
    )
    for old, new in sorted(MAPPING.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(f"lessons/pydata/{old}/", f"lessons/{new}/")
        text = text.replace(f"lessons/pydata/{old}", f"lessons/{new}")
        text = text.replace(f"pydata/{old}/", f"lessons/{new}/")
        text = text.replace(f"../{old}/", f"../{new}/")
    if topic == "notebook":
        text = text.replace(
            "https://github.com/PyDataCZ/naucse.python.cz/tree/master/lessons/pydata",
            "https://github.com/PyDataCZ/pyladies-kurz/tree/main/lessons/jupyter-notebook",
        )
    text = text.replace("lessons/pydata/", "lessons/")
    text = text.replace("static/excercise.ipynb", "population-exercise.ipynb")
    text = text.replace("assets/excercise.ipynb", "population-exercise.ipynb")
    text = text.replace("static/", "assets/")
    text = re.sub(r"(?<![\w/-])index_na_hodinu_2025\.ipynb", "classroom-version-2025.ipynb", text)
    text = re.sub(r"(?<![\w/-])index_na_hodinu\.ipynb", "classroom-version.ipynb", text)
    text = text.replace("weather_data.ipynb", "prepare-weather-data.ipynb")
    text = text.replace("reseni.ipynb", "solutions.ipynb")
    text = text.replace("images.ipynb", "generate-images.ipynb")
    if topic == "eda-univariate-timeseries":
        text = text.replace("./prague-meteostat.parquet", "assets/praha-meteostat.parquet")
    if topic == "intro_classification":
        text = re.sub(
            r"\.\./classification-bonus/(?!classification-bonus\.ipynb)",
            "../classification-bonus/classification-bonus.ipynb",
            text,
        )
        text = re.sub(
            r"\.\./classification-metrics/(?!classification-metrics\.ipynb)",
            "../classification-metrics/classification-metrics.ipynb",
            text,
        )
    if topic == "visualization_basics":
        text = text.replace("../pandas_types/countries.csv", "assets/countries.csv")
        text = text.replace("../pandas-data-types/countries.csv", "assets/countries.csv")
    if topic == "pandas_groupby":
        text = text.replace(
            "https://raw.githubusercontent.com/PyDataCZ/pyladies-kurz/main/lessons/pandas-groupby/serk.csv",
            "https://raw.githubusercontent.com/PyDataCZ/pyladies-kurz/main/lessons/pandas-groupby/assets/serk.csv",
        )
    if topic == "databases":
        for filename in ("movies.sqlite", "world.sqlite"):
            text = text.replace(
                f"https://github.com/PyDataCZ/pyladies-kurz/raw/main/lessons/databases/{filename}",
                f"https://github.com/PyDataCZ/pyladies-kurz/raw/main/lessons/databases/assets/{filename}",
            )
            text = text.replace(f"sqlite:///{filename}", f"sqlite:///assets/{filename}")
    for name in sorted(asset_names, key=len, reverse=True):
        text = text.replace(f"./{name}", f"assets/{name}")
        text = re.sub(rf"(?<![\w/.-]){re.escape(name)}(?![\w.-])", f"assets/{name}", text)
    return text


def rewrite_file(path: Path, topic: str, asset_names: set[str]) -> None:
    if path.suffix == ".ipynb":
        notebook = json.loads(path.read_text())
        for cell in notebook.get("cells", []):
            cell["source"] = [rewritten(part, topic, asset_names) for part in cell.get("source", [])]
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")
    elif path.suffix in {".md", ".yml", ".txt", ".py"}:
        path.write_text(rewritten(path.read_text(), topic, asset_names))


def plan_moves() -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    tracked = set(
        subprocess.check_output(["git", "ls-files", "lessons/pydata"], cwd=ROOT, text=True).splitlines()
    )
    for old, new in MAPPING.items():
        source = LEGACY / old
        target = destination(old)
        primary = source / ("index.ipynb" if (source / "index.ipynb").exists() else "index.md")
        if primary.exists():
            moves.append((primary, target / expected_primary(old)))
        for relative in sorted(tracked):
            if not relative.startswith(f"lessons/pydata/{old}/"):
                continue
            item = ROOT / relative
            if not item.exists():
                continue
            local = str(item.relative_to(source))
            if local in {"index.ipynb", "index.md", "info.yml"}:
                continue
            name = AUXILIARY.get((old, local), item.name)
            if local == ".gitignore":
                target_path = target / ".gitignore"
            elif item.suffix == ".ipynb":
                target_path = target / name
            else:
                target_path = target / "assets" / name
            moves.append((item, target_path))
    return moves


def preflight() -> list[tuple[Path, Path]]:
    tracked = subprocess.check_output(
        ["git", "ls-files", "lessons/pydata"], cwd=ROOT, text=True
    ).splitlines()
    if not LEGACY.is_dir() or not any((ROOT / path).exists() for path in tracked):
        return []
    missing = [old for old in MAPPING if not (LEGACY / old).is_dir()]
    if missing:
        raise SystemExit(f"missing legacy lesson directories: {', '.join(missing)}")
    moves = plan_moves()
    conflicts = [str(dst) for src, dst in moves if dst.exists() and dst != src]
    if conflicts:
        raise SystemExit("destination conflicts:\n" + "\n".join(conflicts))
    return moves


def apply() -> None:
    moves = preflight()
    for source, target in moves:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
    for old, new in MAPPING.items():
        info = LEGACY / old / "info.yml"
        if info.exists():
            info.unlink()
        target = destination(old)
        asset_names = {p.name for p in target.glob("assets/*") if p.is_file()}
        for path in target.rglob("*"):
            if path.is_file() and path.name != ".gitignore":
                rewrite_file(path, old, asset_names)
        source = LEGACY / old
        if source.exists() and not any(source.iterdir()):
            source.rmdir()
    if LEGACY.exists() and not any(LEGACY.iterdir()):
        LEGACY.rmdir()
    if LEGACY.exists():
        for directory in sorted(
            (path for path in LEGACY.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            try:
                directory.rmdir()
            except OSError:
                pass
        try:
            LEGACY.rmdir()
        except OSError:
            pass
    link = ROOT / "book" / "pydata"
    if link.is_symlink():
        link.unlink()
    elif link.is_dir() and not any(link.iterdir()):
        link.rmdir()


def verify() -> None:
    errors: list[str] = []
    tracked_legacy = [
        path for path in subprocess.check_output(
            ["git", "ls-files", "lessons/pydata"], cwd=ROOT, text=True
        ).splitlines() if (ROOT / path).exists()
    ]
    if tracked_legacy:
        errors.append("tracked files remain under lessons/pydata")
    for old, new in MAPPING.items():
        target = destination(old)
        primary_candidates = [target / expected_primary(old)]
        if not target.is_dir():
            errors.append(f"missing topic directory: {target}")
        if not any(primary.is_file() for primary in primary_candidates):
            errors.append(f"missing primary file in {target}")
        if any(target.rglob("info.yml")):
            errors.append(f"info.yml remains in {target}")
        asset_names = {p.name for p in (target / "assets").glob("*") if p.is_file()}
        for path in target.rglob("*"):
            if path.is_file() and path.suffix in {".ipynb", ".md", ".yml", ".txt"}:
                text = path.read_text(errors="replace")
                source_text = text
                if path.suffix == ".ipynb":
                    notebook = json.loads(text)
                    source_text = "".join(
                        part
                        for cell in notebook.get("cells", [])
                        for part in cell.get("source", [])
                    )
                if "static/" in source_text or "lessons/pydata/" in source_text:
                    errors.append(f"legacy reference in {path}")
                for url in re.findall(r"https?://[^\s)\"']*lessons/[^\s)\"']+", source_text):
                    lesson_path = url.split("lessons/", 1)[1]
                    if "_" in lesson_path or "pandas-basics_" in lesson_path:
                        errors.append(f"malformed lesson URL {url} in {path}")
                known_remote_assets = (
                    "https://raw.githubusercontent.com/PyDataCZ/pyladies-kurz/main/lessons/pandas-groupby/assets/serk.csv",
                    "https://github.com/PyDataCZ/pyladies-kurz/raw/main/lessons/databases/assets/movies.sqlite",
                    "https://github.com/PyDataCZ/pyladies-kurz/raw/main/lessons/databases/assets/world.sqlite",
                )
                for remote in known_remote_assets:
                    if remote.replace("/assets/", "/") in source_text:
                        errors.append(f"remote asset URL missing /assets/: {remote}")
                for name in asset_names:
                    ref = f"assets/{name}"
                    if ref in source_text and not (path.parent / ref).is_file():
                        errors.append(f"missing local reference {ref} in {path}")
                for ref in re.findall(r"(?:\.\./)+[\w-]+/[\w.-]+|\./[\w.-]+", source_text):
                    resolved = (path.parent / ref).resolve()
                    if not resolved.is_file():
                        errors.append(f"missing local reference {ref} in {path}")
    if errors:
        raise SystemExit("migration verification failed:\n" + "\n".join(errors))
    print(f"verified {len(MAPPING)} migrated lessons")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        verify()
    elif args.dry_run:
        for source, target in preflight():
            print(f"{source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    else:
        apply()
        verify()


if __name__ == "__main__":
    main()
