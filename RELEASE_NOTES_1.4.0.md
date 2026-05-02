# AbaoSplitZip v1.4.0

This is the final GPL open-source release of AbaoSplitZip before the
repository is archived.

## Highlights

- Fixed password-protected packing for both ZipCrypto-compatible ZIP files and
  AES-256 ZIP files.
- Added a volume manifest so deleted trailing volumes are detected instead of
  silently producing partial extraction.
- Hardened ZIP extraction against unsafe archive paths and accidental
  overwrites.
- Added ZIP output conflict strategies: stop, skip existing files, auto-rename,
  or overwrite.
- Added a preflight packing preview showing file count, total size, estimated
  volume count, and oversized-file warnings.
- Improved large-file progress reporting and cancellation responsiveness.
- Capped default packing concurrency and reduced write buffering to lower memory
  and disk contention on large volume sets.
- Fixed generated one-click extraction scripts to handle metacharacters more
  safely.
- Updated documentation, release assets, website links, and executable naming
  back to `AbaoSplitZip` for the final open-source archive.
- Added archive, release checklist, and third-party notices for responsible
  project closure.

## Verification

The release was prepared with:

```bash
python -m unittest discover -s tests -v
python -m py_compile core/packer.py core/unpacker.py core/zipcrypto.py core/i18n.py gui/main_window.py tests/test_core.py tests/test_static_quality.py
git diff --check
```

## Notes

- License: GPL v3.
- AES-256 encrypted ZIP files require a compatible extractor such as 7-Zip or
  WinRAR; Windows Explorer does not support AES ZIP encryption.
- RAR extraction depends on a compatible runtime available on the user's system.
