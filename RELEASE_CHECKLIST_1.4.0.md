# AbaoSplitZip v1.4.0 Final Release Checklist

Use this checklist for the final GPL open-source release.

## Local Verification

- [ ] Confirm `core/version.py` reports `APP_NAME = "AbaoSplitZip"` and
  `APP_VERSION = "1.4.0"`.
- [ ] Confirm README files describe this as the final GPL open-source release.
- [ ] Confirm public documentation links to the commercial successor only through
  `https://www.abaodisk.com/Abaozip`.
- [ ] Confirm private commercial planning notes are ignored and not committed.
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python -m py_compile core/packer.py core/unpacker.py core/zipcrypto.py core/i18n.py core/version.py gui/main_window.py tests/test_core.py tests/test_static_quality.py`.
- [ ] Run `git diff --check`.
- [ ] Build a local Windows executable with PyInstaller or let GitHub Actions
  build the release artifacts from the tag.

## Commit and Tag

```bash
git add .
git commit -m "Prepare AbaoSplitZip v1.4.0 final GPL release"
git tag -a v1.4.0 -m "AbaoSplitZip v1.4.0 final GPL release"
```

## Push

```bash
git push origin main
git push origin v1.4.0
```

## GitHub Release

- [ ] Wait for GitHub Actions to finish building all platform artifacts.
- [ ] Create or review the GitHub Release generated from tag `v1.4.0`.
- [ ] Use `RELEASE_NOTES_1.4.0.md` as the release body.
- [ ] Confirm assets use `AbaoSplitZip-*` names.

## Archive Repository

Only archive after the release page and binaries are available.

- [ ] Disable or close open Issues and Pull Requests.
- [ ] Confirm repository description says final GPL open-source release.
- [ ] Confirm `ARCHIVE_NOTICE.md` is visible in the repository.
- [ ] GitHub Settings -> General -> Archive repository.
