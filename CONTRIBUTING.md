# Contributing

Thanks for helping improve AbaoSplitZip.

This repository is being prepared as the final GPL open-source release. After
`v1.4.0`, the repository is intended to be archived and new feature development
will happen separately.

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

