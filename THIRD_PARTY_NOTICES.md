# Third-Party Notices

AbaoSplitZip v1.4.0 depends on third-party open-source software. This file is
provided as a release aid and does not replace the upstream license files.
Before redistributing binary builds, review the exact dependency versions bundled
in that build.

## Direct Runtime Dependencies

| Component | Use | License / Notes |
| --- | --- | --- |
| PyQt5 | Desktop GUI | PyQt is dual-licensed under GPL v3 and the Riverbank commercial license. This final open-source release uses the GPL-compatible path. |
| pyzipper | ZIP AES encryption support | MIT. |
| py7zr | Optional 7z extraction | LGPL-2.1-or-later. |
| rarfile | Optional RAR archive reading | ISC. RAR extraction may require a compatible external runtime installed on the user's system. |

## Build-Time Dependency

| Component | Use | License / Notes |
| --- | --- | --- |
| PyInstaller | Standalone executable packaging | GPL with a bootloader exception that allows bundled applications to use their own license. |

## Notes for Maintainers

- Do not bundle proprietary RAR creation or repair code without a clear license.
- If a binary release includes additional transitive dependencies, include their
  notices as well.
- Future proprietary development should re-evaluate the GUI toolkit license.
  PyQt5 GPL builds are not suitable for closed-source proprietary distribution
  unless the appropriate commercial license is obtained.

