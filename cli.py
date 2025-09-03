#!/usr/bin/env python

import json
import pathlib
import zipfile

import click
import yaml
from nbconvert.exporters import NotebookExporter
from nbconvert.preprocessors import ClearOutputPreprocessor


def get_materials() -> dict:
    with open("course.yml", "r", encoding="utf8") as f:
        course = yaml.safe_load(f)
        materials = {
            lesson["slug"]: lesson.get("materials", []) for lesson in course["plan"]
        }
        return materials


def get_chapter_info() -> dict:
    """Extract chapter information from book myst.yml for download mapping."""
    book_config_path = pathlib.Path("book/myst.yml")
    if not book_config_path.exists():
        return {}

    with open(book_config_path, "r", encoding="utf8") as f:
        config = yaml.safe_load(f)

    chapters = {}
    toc = config.get("project", {}).get("toc", [])

    def extract_files(items, parent_title=None):
        for item in items:
            if isinstance(item, dict):
                title = item.get("title", parent_title)
                if "file" in item:
                    # Extract chapter name from file path (e.g., 'pydata/pandas_core/index.ipynb' -> 'pandas_core')
                    file_path = item["file"]
                    if file_path.startswith("pydata/") and "/" in file_path:
                        chapter_name = file_path.split("/")[1]
                        chapters[chapter_name] = {
                            "title": title or chapter_name,
                            "file": file_path,
                            "source_path": f"book/{file_path}",
                        }
                if "children" in item:
                    extract_files(item["children"], title)

    extract_files(toc)
    return chapters


def clear_notebook(path: pathlib.Path) -> bytes:
    exporter = NotebookExporter()
    exporter.register_preprocessor(ClearOutputPreprocessor(), enabled=True)
    output = exporter.from_filename(str(path))
    return output[0]


@click.group()
def cli():
    pass


@cli.command()
@click.argument("slug")
def export(slug: str) -> None:
    """Export all material folders for a lesson as a single zip file.
    Clears the output of ipynb jupyter notebook files.
    """
    materials = get_materials()
    dirs = [
        "lessons" / pathlib.Path(material["lesson"]) for material in materials[slug]
    ]
    with zipfile.ZipFile(f"{slug}.zip", "w") as zip:
        for dir in dirs:
            for file in dir.glob("**/*"):
                click.echo(f"  {file}")
                if not file.is_file():
                    continue
                if file.suffix == ".ipynb":
                    content = clear_notebook(file)
                    zip.writestr(str(file.relative_to(dir.parent)), content)
                else:
                    zip.write(file, arcname=file.relative_to(dir.parent))


@cli.command()
@click.argument("chapter_name")
@click.option(
    "--output-dir", default="downloads", help="Output directory for zip files"
)
def export_chapter(chapter_name: str, output_dir: str) -> None:
    """Export a single chapter with its notebook and static files.

    Creates a zip file containing the notebook (with cleared outputs) and all
    associated static files needed to run the chapter locally.
    """
    # Use the book structure directly
    chapter_source = pathlib.Path("book/pydata") / chapter_name

    if not chapter_source.exists():
        click.echo(f"Error: Chapter '{chapter_name}' not found at {chapter_source}")
        return

    # Create output directory if it doesn't exist
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(exist_ok=True)

    zip_filename = output_path / f"{chapter_name}.zip"

    click.echo(f"Creating {zip_filename}...")

    with zipfile.ZipFile(zip_filename, "w") as zip_file:
        # Add all files from the chapter directory
        for file_path in chapter_source.rglob("*"):
            if file_path.is_file():
                click.echo(f"  Adding {file_path}")

                # Get relative path for archive
                arcname = file_path.relative_to(chapter_source)

                if file_path.suffix == ".ipynb":
                    # Clear notebook outputs
                    content = clear_notebook(file_path)
                    zip_file.writestr(str(arcname), content)
                else:
                    # Add other files as-is
                    zip_file.write(file_path, arcname)

        # Add README with instructions
        readme_content = create_chapter_readme(chapter_name, chapter_source)
        zip_file.writestr("README.md", readme_content)

    click.echo(f"✓ Chapter '{chapter_name}' exported to {zip_filename}")


@cli.command()
@click.option(
    "--output-dir", default="downloads", help="Output directory for zip files"
)
def export_all_chapters(output_dir: str) -> None:
    """Export all chapters as individual zip files for download."""
    chapters = get_chapter_info()

    if not chapters:
        click.echo("No chapters found in book configuration")
        return

    output_path = pathlib.Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Create downloads index
    downloads_index = {"chapters": {}, "generated_at": None}

    for chapter_name, chapter_info in chapters.items():
        click.echo(f"\nExporting chapter: {chapter_name}")

        # Use the export_chapter functionality
        ctx = click.get_current_context()
        ctx.invoke(export_chapter, chapter_name=chapter_name, output_dir=output_dir)

        # Add to downloads index
        downloads_index["chapters"][chapter_name] = {
            "title": chapter_info["title"],
            "filename": f"{chapter_name}.zip",
            "url": f"_downloads/{chapter_name}.zip",
        }

    # Write downloads index for the website
    import datetime

    downloads_index["generated_at"] = datetime.datetime.now().isoformat()

    with open(output_path / "index.json", "w", encoding="utf8") as f:
        json.dump(downloads_index, f, indent=2, ensure_ascii=False)

    click.echo(f"\n✓ All chapters exported to {output_dir}/")
    click.echo(f"✓ Downloads index created at {output_dir}/index.json")


def create_chapter_readme(chapter_name: str, chapter_path: pathlib.Path) -> str:
    """Create a README file for the exported chapter."""
    readme_content = f"""# {chapter_name.replace("_", " ").title()} - Jupyter Notebook Exercise

This package contains the Jupyter notebook and all necessary data files for the "{chapter_name}" chapter from the PyLadies Data Course.

## Contents

- `index.ipynb` - Main Jupyter notebook
- `static/` - Data files and images required by the notebook

## Getting Started

1. **Install Required Packages**
   Make sure you have Python 3.8+ and the following packages installed:
   ```bash
   pip install jupyter pandas matplotlib seaborn numpy
   ```

2. **Open the Notebook**
   ```bash
   jupyter notebook index.ipynb
   ```

3. **Follow Along**
   The notebook contains both explanations and exercises. Run the cells step by step.

## Data Files

All required data files are included in the `static/` folder. The notebook will automatically find these files using relative paths.

## Need Help?

- Check out the full course at: https://pydatacz.github.io/pyladies-kurz/
- Visit PyLadies Czech Republic: http://pyladies.cz/
- PyData Prague: http://pydata.cz/

Happy learning! 🐍📊
"""
    return readme_content


if __name__ == "__main__":
    cli()
