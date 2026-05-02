# Changelog

All notable changes to AbaoSplitZip are documented in this file.

## [1.4.0] - 2026-05-02

Final GPL open-source release before the AbaoSplitZip repository is archived.

### Added

- Added volume manifest generation so the extractor can detect deleted trailing volumes instead of silently extracting a partial set.
- Added regression tests for encrypted packing, missing volumes, overwrite protection, unsafe output paths, and generated script escaping.
- Added a preflight packing preview with file count, total size, estimated volume count, and oversized-file warning before starting a job.
- Added ZIP extraction conflict strategies for existing output files: stop, skip, auto-rename, or overwrite.
- Added GUI prompts for pack previews and ZIP output conflict handling in non-empty destination folders.

### Changed

- Hardened ZIP extraction to preflight target paths and reject existing output files by default.
- Improved one-click batch script generation by using PowerShell `-LiteralPath` and escaping batch/PowerShell metacharacters in generated commands.
- Locked the language selector while a background job is running so the UI cannot be rebuilt mid-operation.
- Updated bundled website pages to use the current `AbaoSplitZip` branding and repository links consistently.
- Changed packing progress to byte-level updates so even a single large volume shows visible progress before completion.
- Capped default packing concurrency and reduced per-writer buffering to lower memory and disk contention on large volume sets.

### Fixed

- Fixed password-protected packing for both ZipCrypto-compatible ZIPs and AES-256 ZIPs.
- Fixed empty-source and invalid output-folder cases so they fail explicitly instead of reporting a misleading successful result.
- Fixed worker output-folder tracking so the "Open Output Folder" button opens the last successful operation's destination.
- Added close-window handling for running jobs, prompting before cancelling and exiting.
- Made packing cancellation interrupt long file copies instead of waiting for the whole file or volume to finish.
- Preserved archived file modified times after switching to chunked ZIP writes.

## [1.3.1] - 2026-03-25

### Changed

- Unified the main desktop/build naming around `AbaoSplitZip` so local builds, GitHub Actions artifacts, and Windows version metadata use the same product name.
- Moved runtime version metadata into `core/version.py` so the About dialog and build scripts stop hardcoding the same version string in multiple places.
- Reworked compression preset wiring so core packing logic no longer depends on Chinese UI labels.

### Added

- Added a basic `unittest` test suite for volume assignment, ZIP volume discovery, and language detection fallback behavior.
- Added `CONTRIBUTING.md` with a short setup, testing, and release checklist for maintainers.

### Fixed

- Fixed the Windows build script and GitHub Actions workflow to use the actual `AbaoSplitZip` executable name instead of the legacy `AbaoSplitZip` artifact name.
- Tightened language detection fallback handling so locale parsing failures fall back cleanly to English without a broad silent catch.

