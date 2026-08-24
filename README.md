# Materiály pro Datový kurz PyLadies

Zdrojové materiály kurzu jsou uspořádané v adresáři `lessons/`, vždy v
samostatném tematickém adresáři se sémantickým názvem a podsložkou `assets/`.

## Instalace a lokální kontrola

```shell
uv sync --locked --all-packages
uv run python scripts/migrate_lessons.py --verify
uv run python scripts/render_notebooks.py
uv run jupyter-book build --html --strict
```

Výstup Jupyter Booku vzniká v `_build/html`. Je koncipován pro běh na serveru, a tedy
je potřeba spustit jednoduchý HTTP server v daném adresáři - samotné otevření index.html nestačí.
Například takto:

```shell
uv run --directory _build/html python -m http.server
```

Notebooky s uloženými výstupy a ověřené vykonané notebooky jsou v `_build/notebooks/`;
tyto adresáře nejsou zdrojové soubory kurzu.

Interaktivní práci s notebooky spustíš příkazem:

```shell
uv run --directory lessons jupyter lab
```

Kniha používá Binder z větve `main`. Publikování na GitHub Pages probíhá po
změně větve `main` prostřednictvím workflow v `.github/workflows/book.yml`.
