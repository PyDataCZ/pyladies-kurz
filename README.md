# Materiály pro Datový kurz PyLadies

Tento repozitář slouží jako zdroj pro materiály datového kurzu, který najdeš
(ve vydání roku 2024) na adrese https://naucse.python.cz/2024/pydata-praha-podzim/.

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

## Publikování na web

1. Aby se vůbec něco nahrálo na web, kurz musí být definován v repozitáři
https://github.com/pyvec/naucse.python.cz, konkrétně v souboru `courses.yaml`

2. Soubor `.github/workflows/main.yml` v tomto repozitáři musí definovat odpovídající
jméno větve, do které se mají materiály kompilovat.

3. Potom by mělo stačit mergovat cokoliv do větve `main`, aby se vše automaticky propsalo na web.

4. ⚠️ Nicméně ono se sice vyplodí, co se vyplodit má, ale na web nenahraje. Je potřeba to 
prošťouchnout pomocí akce v hlavním repozitáři: https://github.com/pyvec/naucse.python.cz/actions/workflows/main.yml . 
Ta se spustí tlačítkem "Run workflow" vpravo nahoře. Pokud by chyběla práva, @janpipek či @coobas by právo
mít měli.
