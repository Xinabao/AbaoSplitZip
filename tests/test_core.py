import os
import time
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import pyzipper

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

    def test_empty_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "empty")
            output = os.path.join(tmp, "output")
            os.mkdir(source)

            packer = VolumePacker(
                source_dir=source,
                output_dir=output,
                volume_size_mb=1,
            )

            with self.assertRaises(ValueError):
                packer.pack()

    def test_output_directory_inside_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "source")
            output = os.path.join(source, "output")
            os.mkdir(source)
            with open(os.path.join(source, "a.txt"), "w", encoding="utf-8") as f:
                f.write("hello")

            packer = VolumePacker(
                source_dir=source,
                output_dir=output,
                volume_size_mb=1,
            )

            with self.assertRaises(ValueError):
                packer.pack()

    def test_zipcrypto_password_pack_roundtrips_with_standard_zipfile(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            source.mkdir()
            (source / "a.txt").write_text("secret", encoding="utf-8")

            packer = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=1,
                password="pw",
                encryption_method="zipcrypto",
                compression_key="store",
            )

            result = packer.pack()

            with zipfile.ZipFile(result.output_files[0], "r") as zf:
                with zf.open("source/a.txt", pwd=b"pw") as f:
                    self.assertEqual(f.read().decode("utf-8"), "secret")

    def test_aes256_password_pack_roundtrips_with_unpacker(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            extract_to = Path(tmp) / "extract"
            source.mkdir()
            (source / "a.txt").write_text("secret", encoding="utf-8")

            packer = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=1,
                password="pw",
                encryption_method="aes256",
                compression_key="normal",
            )

            result = packer.pack()
            unpacked = VolumeUnpacker(
                first_zip=result.output_files[0],
                output_dir=str(extract_to),
                password="pw",
            ).unpack()

            self.assertEqual(unpacked.total_files, 1)
            self.assertEqual((extract_to / "source" / "a.txt").read_text(encoding="utf-8"), "secret")

    def test_generated_unpack_script_escapes_batch_and_powershell_metacharacters(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "weird%NAME%&'src"
            output = Path(tmp) / "output"
            source.mkdir()
            (source / "a.txt").write_text("hello", encoding="utf-8")

            result = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=1,
                compression_key="store",
            ).pack()

            bat_path = output / "weird%NAME%&'src_一键全部解压.bat"
            script = bat_path.read_text(encoding="utf-8")

            self.assertIn('echo 正在解压 "weird%%NAME%%&\'src"', script)
            self.assertIn('echo 解压: "weird%%NAME%%&\'src_part001.zip"', script)
            self.assertIn("-LiteralPath '.\\weird%%NAME%%&''src_part001.zip'", script)
            self.assertIn("-DestinationPath $env:OUT_DIR", script)
            self.assertNotIn("Expand-Archive -Path", script)

    def test_single_volume_reports_byte_progress_before_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            source.mkdir()
            (source / "a.txt").write_bytes(b"a" * 2048)
            (source / "b.txt").write_bytes(b"b" * 2048)
            progress_values = []

            packer = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=10,
                compression_key="store",
                progress_callback=progress_values.append,
            )
            packer.file_chunk_size = 512

            packer.pack()

            self.assertTrue(any(0 < value < 100 for value in progress_values))
            self.assertEqual(progress_values[-1], 100)

    def test_cancel_is_checked_during_large_file_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            source.mkdir()
            (source / "large.bin").write_bytes(b"x" * 4096)
            cancelled = {"value": False}

            def on_progress(value):
                if 0 < value < 100:
                    cancelled["value"] = True

            packer = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=10,
                compression_key="store",
                progress_callback=on_progress,
                cancel_check=lambda: cancelled["value"],
            )
            packer.file_chunk_size = 512

            with self.assertRaisesRegex(RuntimeError, "cancelled"):
                packer.pack()

            self.assertFalse((output / "source_part001.zip").exists())

    def test_worker_count_is_capped_for_large_volume_sets(self):
        packer = VolumePacker(
            source_dir="source",
            output_dir="output",
            volume_size_mb=1,
        )

        self.assertLessEqual(packer._max_worker_count(100), 4)

    def test_packing_preserves_file_modified_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            source.mkdir()
            file_path = source / "dated.txt"
            file_path.write_text("dated", encoding="utf-8")
            timestamp = time.mktime((2024, 5, 6, 7, 8, 10, 0, 0, -1))
            os.utime(file_path, (timestamp, timestamp))

            result = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=1,
                compression_key="store",
            ).pack()

            with zipfile.ZipFile(result.output_files[0], "r") as zf:
                info = zf.getinfo("source/dated.txt")

            self.assertEqual(info.date_time, (2024, 5, 6, 7, 8, 10))

    def test_preview_reports_estimated_volumes_and_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            source.mkdir()
            (source / "small.txt").write_bytes(b"a" * 100)
            (source / "large.bin").write_bytes(b"b" * 1500)

            packer = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=0.001,
                compression_key="store",
                mode="directory_priority",
            )

            preview = packer.preview()

            self.assertEqual(preview.total_files, 2)
            self.assertEqual(preview.total_size, 1600)
            self.assertEqual(preview.volumes, 2)
            self.assertEqual(preview.max_file_size, 1500)
            self.assertTrue(preview.has_oversized_file)


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

    def test_unpack_rejects_missing_middle_volume(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("demo_part001.zip", "demo_part003.zip"):
                with zipfile.ZipFile(os.path.join(tmp, name), "w") as zf:
                    zf.writestr(f"demo/{name}.txt", "x")

            unpacker = VolumeUnpacker(
                first_zip=os.path.join(tmp, "demo_part001.zip"),
                output_dir=os.path.join(tmp, "out"),
            )

            with self.assertRaises(RuntimeError):
                unpacker.unpack()

    def test_unpack_uses_manifest_to_reject_missing_final_volume(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            extract_to = Path(tmp) / "extract"
            source.mkdir()
            for i in range(3):
                (source / f"{i}.txt").write_text("x" * 1200, encoding="utf-8")

            result = VolumePacker(
                source_dir=str(source),
                output_dir=str(output),
                volume_size_mb=0.001,
                compression_key="store",
                mode="directory_priority",
            ).pack()
            os.remove(result.output_files[-1])

            with self.assertRaises(RuntimeError):
                VolumeUnpacker(
                    first_zip=result.output_files[0],
                    output_dir=str(extract_to),
                ).unpack()

    def test_unpack_rejects_existing_output_file_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "demo_part001.zip")
            output = Path(tmp) / "out"
            existing = output / "demo" / "a.txt"
            existing.parent.mkdir(parents=True)
            existing.write_text("keep me", encoding="utf-8")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("demo/a.txt", "new data")

            unpacker = VolumeUnpacker(
                first_zip=zip_path,
                output_dir=str(output),
            )

            with self.assertRaises(FileExistsError):
                unpacker.unpack()
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me")

    def test_unpack_skip_conflict_keeps_existing_and_extracts_other_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "demo_part001.zip")
            output = Path(tmp) / "out"
            existing = output / "demo" / "a.txt"
            existing.parent.mkdir(parents=True)
            existing.write_text("keep me", encoding="utf-8")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("demo/a.txt", "new data")
                zf.writestr("demo/b.txt", "second")

            result = VolumeUnpacker(
                first_zip=zip_path,
                output_dir=str(output),
                conflict_strategy="skip",
            ).unpack()

            self.assertEqual(result.total_files, 1)
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me")
            self.assertEqual((output / "demo" / "b.txt").read_text(encoding="utf-8"), "second")

    def test_unpack_rename_conflict_preserves_existing_and_extracts_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "demo_part001.zip")
            output = Path(tmp) / "out"
            existing = output / "demo" / "a.txt"
            existing.parent.mkdir(parents=True)
            existing.write_text("keep me", encoding="utf-8")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("demo/a.txt", "new data")

            result = VolumeUnpacker(
                first_zip=zip_path,
                output_dir=str(output),
                conflict_strategy="rename",
            ).unpack()

            self.assertEqual(result.total_files, 1)
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me")
            self.assertEqual((output / "demo" / "a (1).txt").read_text(encoding="utf-8"), "new data")

    def test_unpack_overwrite_conflict_replaces_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "demo_part001.zip")
            output = Path(tmp) / "out"
            existing = output / "demo" / "a.txt"
            existing.parent.mkdir(parents=True)
            existing.write_text("old", encoding="utf-8")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("demo/a.txt", "new data")

            result = VolumeUnpacker(
                first_zip=zip_path,
                output_dir=str(output),
                conflict_strategy="overwrite",
            ).unpack()

            self.assertEqual(result.total_files, 1)
            self.assertEqual(existing.read_text(encoding="utf-8"), "new data")

    def test_wrong_aes_password_reports_wrong_password(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "secret_part001.zip")
            with pyzipper.AESZipFile(
                zip_path,
                "w",
                compression=zipfile.ZIP_DEFLATED,
                encryption=pyzipper.WZ_AES,
            ) as zf:
                zf.setpassword(b"right")
                zf.setencryption(pyzipper.WZ_AES, nbits=256)
                zf.writestr("secret/a.txt", "secret")

            unpacker = VolumeUnpacker(
                first_zip=zip_path,
                output_dir=os.path.join(tmp, "out"),
                password="wrong",
            )

            with self.assertRaisesRegex(RuntimeError, "wrong password"):
                unpacker.unpack()


class I18nTests(unittest.TestCase):
    def test_detect_system_language_falls_back_to_english(self):
        with mock.patch("core.i18n.locale.getdefaultlocale", side_effect=ValueError):
            self.assertEqual(detect_system_language(), "en")

    def test_detect_system_language_detects_traditional_chinese(self):
        with mock.patch("core.i18n.locale.getdefaultlocale", return_value=("zh_Hant_TW", "UTF-8")):
            self.assertEqual(detect_system_language(), "zh_TW")


if __name__ == "__main__":
    unittest.main()

