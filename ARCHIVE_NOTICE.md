# AbaoSplitZip Archive Notice

This repository contains the final GPL-licensed open-source release of
AbaoSplitZip.

The project is preserved for users who rely on the original independent ZIP
volume workflow. Future commercial development will happen separately and is
not part of this repository.

## Commercial Successor

This repository preserves the final GPL open-source release of AbaoSplitZip
v1.4.0. Source code, release downloads, and GPL v3 rights remain available.

Future commercial development continues separately under the AbaoZip product
line, with a different license and feature roadmap:

https://www.abaodisk.com/Abaozip

## Final Open-Source Release

- Final version: `v1.4.0`
- License: GPL v3
- Repository: `https://github.com/Xinabao/AbaoSplitZip`

## Maintenance Status

After `v1.4.0`, this repository is intended to be archived. Issues and pull
requests may be closed, and no new feature development is planned here.

## What Changed in the Final Release

The final release focuses on responsible stabilization:

- Fixed password-protected ZIP creation for ZipCrypto and AES-256.
- Added volume manifests so missing trailing volumes are detected.
- Hardened ZIP extraction against unsafe paths and accidental overwrite.
- Added conflict strategies for ZIP extraction: stop, skip, rename, overwrite.
- Improved progress reporting and cancellation for large files.
- Added pack preview confirmation before starting a job.
- Added regression and static quality tests.
