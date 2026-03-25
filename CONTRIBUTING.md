# Contributing

Thanks for helping improve AbaoZip.

## Local setup

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Tests

Run the built-in test suite before opening a pull request:

```bash
python -m unittest discover -s tests -v
```

## Build

Windows:

```cmd
build.bat
```

Linux / macOS:

```bash
chmod +x build.sh
./build.sh
```

## Release checklist

1. Update `core/version.py` if the release version changes.
2. Review `CHANGELOG.md`.
3. Run `python -m unittest discover -s tests -v`.
4. Trigger `.github/workflows/build.yml` or build locally on the target platform.
5. Tag the release and publish artifacts.

