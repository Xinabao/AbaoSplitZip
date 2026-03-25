# Changelog

All notable changes to AbaoZip are documented in this file.

## [Unreleased]

## [1.3.1] - 2026-03-25

### Changed

- Unified the main desktop/build naming around `AbaoZip` so local builds, GitHub Actions artifacts, and Windows version metadata use the same product name.
- Moved runtime version metadata into `core/version.py` so the About dialog and build scripts stop hardcoding the same version string in multiple places.
- Reworked compression preset wiring so core packing logic no longer depends on Chinese UI labels.

### Added

- Added a basic `unittest` test suite for volume assignment, ZIP volume discovery, and language detection fallback behavior.
- Added `CONTRIBUTING.md` with a short setup, testing, and release checklist for maintainers.

### Fixed

- Fixed the Windows build script and GitHub Actions workflow to use the actual `AbaoZip` executable name instead of the legacy `AbaoSplitZip` artifact name.
- Tightened language detection fallback handling so locale parsing failures fall back cleanly to English without a broad silent catch.

