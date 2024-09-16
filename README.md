# Materiály pro Datový kurz PyLadies

TODO: Link na aktuální kurz

## Instalace a spuštění

Chceš-li server spustit na svém počítači, např. proto, že se chceš zapojit do
vývoje, je potřeba ho nejdřív nainstalovat:

### Instalace `uv`

Nemáš-li `uv`, nainstaluj si jej. Na to je několik způsobů:

* podle [návodu](https://github.com/astral-sh/uv)

### Instalace závislostí

Přepni se do adresáře s projektem a spusť:

```shell
uv sync
```

### Lokální server

Chceš-li si kurz prohlédnout, přepni se do adresáře s projektem a spusť:

```shell
uv run python -m naucse serve
```

* Program vypíše adresu (např. `http://0.0.0.0:8003/`).
  * Buď adresu navštiv v prohlížeči a doklikej se na kurz, nebo
  * na konec adresy přidej `/course/local/` a navštiv kurz přímo.

Poznámka: ve windows mi to nefunguje :-(

## Publikování jedné hodiny

Balíček ZIP se všemi materiály lze vytvořit použitím skriptu:

```shell
uv run cli.py export <id-hodiny>
```

## Publikování

TODO: 🤯

## Větve 

TODO: Popiš!