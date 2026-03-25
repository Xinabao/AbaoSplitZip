import os
import tempfile
import unittest
from unittest import mock

from core.i18n import detect_system_language
from core.packer import VolumePacker
from core.unpacker import VolumeUnpacker


class VolumePackerTests(unittest.TestCase):
    def test_size_balanced_assigns_files_across_volumes(self):
        packer = VolumePacker(
            source_dir="source",
            output_dir="output",
            volume_size_mb=1,
            compression_key="normal",
            mode="size_balanced",
        )
        packer.volume_size_bytes = 100
        file_list = [("a.bin", 70), ("b.bin", 60), ("c.bin", 40), ("d.bin", 30)]

        volumes = packer.assign_volumes(file_list)

        self.assertEqual(volumes, [["a.bin", "d.bin"], ["b.bin", "c.bin"]])

    def test_directory_priority_keeps_large_file_in_own_volume(self):
        packer = VolumePacker(
            source_dir="source",
            output_dir="output",
            volume_size_mb=1,
            compression_key="normal",
            mode="directory_priority",
        )
        packer.volume_size_bytes = 100
        file_list = [("big.iso", 150), ("small.txt", 20), ("tiny.txt", 10)]

        volumes = packer.assign_volumes(file_list)

        self.assertEqual(volumes, [["big.iso"], ["small.txt", "tiny.txt"]])

    def test_invalid_volume_size_is_rejected(self):
        with self.assertRaises(ValueError):
            VolumePacker(source_dir="source", output_dir="output", volume_size_mb=0)


class VolumeUnpackerTests(unittest.TestCase):
    def test_find_volumes_returns_sorted_related_parts(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in (
                "demo_part003.zip",
                "demo_part001.zip",
                "demo_part002.zip",
                "other_part001.zip",
            ):
                open(os.path.join(tmp, name), "wb").close()

            unpacker = VolumeUnpacker(
                first_zip=os.path.join(tmp, "demo_part002.zip"),
                output_dir=tmp,
            )

            volumes = unpacker.find_volumes()

            self.assertEqual(
                [os.path.basename(path) for path in volumes],
                ["demo_part001.zip", "demo_part002.zip", "demo_part003.zip"],
            )


class I18nTests(unittest.TestCase):
    def test_detect_system_language_falls_back_to_english(self):
        with mock.patch("core.i18n.locale.getdefaultlocale", side_effect=ValueError):
            self.assertEqual(detect_system_language(), "en")

    def test_detect_system_language_detects_traditional_chinese(self):
        with mock.patch("core.i18n.locale.getdefaultlocale", return_value=("zh_Hant_TW", "UTF-8")):
            self.assertEqual(detect_system_language(), "zh_TW")


if __name__ == "__main__":
    unittest.main()

