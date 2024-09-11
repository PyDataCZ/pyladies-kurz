# Materiály pro Datový kurz PyLadies

Tento repozitář slouží jako zdroj pro materiály datového kurzu, který najdeš
(ve vydání roku 2024) na adrese https://naucse.python.cz/2024/pydata-praha-podzim/.

## Instalace a spuštění

Chceš-li server spustit na svém počítači, např. proto, že se chceš zapojit do
vývoje, je potřeba ho nejdřív nainstalovat:

### Instalace `poetry`

Nemáš-li `poetry`, nainstaluj si jej. Na to je několik způsobů:

* podle [návodu](https://python-poetry.org/docs/)
* v aktivovaném [virtuálním prostředí](https://naucse.python.cz/lessons/beginners/install/)
  pomocí `python -m pip install poetry`
* na Fedoře pomocí balíčkovacího systému: `sudo dnf install poetry`

### Instalace závislostí

Přepni se do adresáře s projektem a spusť:

```console
$ poetry install --dev
```

### Lokální server

Chceš-li si kurz prohlédnout, přepni se do adresáře s projektem a spusť:

```console
$ poetry run python -m naucse serve
```

* Program vypíše adresu (např. `http://0.0.0.0:8003/`).
  * Buď adresu navštiv v prohlížeči a doklikej se na kurz, nebo
  * na konec adresy přidej `/course/local/` a navštiv kurz přímo.

## Publikování

Aby se vůbec něco nahrálo na web, kurz musí být definován v repozitáři
https://github.com/pyvec/naucse.python.cz, konkrétně v souboru `courses.yaml`

...

TODO: 🤯

## Větve

TODO: Popiš!
