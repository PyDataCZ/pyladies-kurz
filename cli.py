#!/usr/bin/env python

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
                if not file.is_file():
                    continue
                if file.name == "info.yml":
                    continue
                if "checkpoint" in file.stem:
                    continue
                click.echo(f"  {file}")
                if file.suffix == ".ipynb":
                    content = clear_notebook(file)
                    zip.writestr(str(file.relative_to(dir.parent)), content)
                else:
                    zip.write(file, arcname=file.relative_to(dir.parent))
        click.echo("  lessons/pyproject.toml")
        zip.write("lessons/pyproject.toml", arcname="pyproject.toml")


if __name__ == "__main__":
    cli()
