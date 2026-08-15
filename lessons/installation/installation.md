# Instalace

Instalace všeho potřebného není složitá a zabere jen chvíli. Pokud se během ní
přeci jen něco pokazí, popros na Slacku nebo někoho zkušenějšího o radu.

Pokud již máš na svém počítači nainstalovaný aktuální Python (3.11 a vyšší)
a rozumíš si s virtuálními prostředími, můžeš samozřejmě používat ten. Nicméně silně
doporučujeme používat nástroj `uv`.

[`uv`](https://docs.astral.sh/uv/) je mocný nástroj, který toho umí víc:
- spravuje instalované verze Pythonu (aniž by zasahoval do systému)
- spravuje virtuální prostředí pro různé projekty (aniž by je bylo třeba explicitně vytvářet)
- umožňuje snadno instalovat a spouštět různé nástroje postavené na Pythonu
- pomáhá s vytvářením balíčků a jejich závislostí

Pojďme ho tedy nainstalovat.

## Instalace uv

Celý proces je popsaný na stránce https://docs.astral.sh/uv/getting-started/installation/ -
liší se podle tvého operačního systému. Každopádně vždy probihá v příkazovém řádku.

### Windows

Kdekoliv v příkazové řádce (či PowerShell okně) spusť následující:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

To by mělo nástroj stáhnout z internetu a nainstalovat - přitom se vypíše cca toto:

```text
Downloading uv 0.8.15 (x86_64-pc-windows-msvc)
Installing to C:\Users\janpi\.local\bin
  uv.exe
  uvx.exe
  uvw.exe
everything's installed!
```

### MacOS či Linux

Tady bude nejlepší v příkazové řádce spustit

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

To by mělo nástroj stáhnout z internetu a nainstalovat.

## Ověření

Zkus v příkazové řádce pustit toto:

```
uv run --python 3.13 python -c "print('Ahoj Pyladies')"
```

Při prvním spuštění nejspíš uvidíš, jak se stahuje a instaluje správná verze Pythonu,
při druhém spuštění vše proběhne jako blesk. V každém případě by tě měl program slušně
pozdravit.

## Pomoc!

Pokud kterýkoliv z kroků selže, nebo si jen nebudeš vědět rady, zeptej se na Slacku v kanále `#poradna`, ideálně ještě před zahájením kurzu.

V následující kapitole se podíváme na to, jak Jupyter spustit a jak s ním pracovat.
