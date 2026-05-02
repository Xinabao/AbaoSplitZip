import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class StaticQualityTests(unittest.TestCase):
    def test_main_window_handles_close_event_for_running_worker(self):
        source = _source("gui/main_window.py")
        tree = ast.parse(source)
        main_window = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "MainWindow"
        )
        method_names = {
            node.name for node in main_window.body
            if isinstance(node, ast.FunctionDef)
        }

        self.assertIn("closeEvent", method_names)
        self.assertIn("self.worker.isRunning()", source)
        self.assertIn("event.ignore()", source)
        self.assertIn("event.accept()", source)

    def test_main_window_locks_language_switch_while_worker_runs(self):
        source = _source("gui/main_window.py")

        self.assertIn("self.lang_combo.setEnabled(enabled)", source)
        self.assertIn("if self.worker and self.worker.isRunning()", source)

    def test_primary_website_uses_current_brand_and_repository(self):
        source = _source("resources/website/index.html")

        self.assertIn("AbaoSplitZip", source)
        self.assertIn("github.com/Xinabao/AbaoSplitZip", source)
        future_brand = "Abao" + "Zip"
        self.assertNotIn("github.com/Xinabao/" + future_brand, source)
        self.assertIn("Final GPL", source)
        self.assertIn("© 2026", source)

    def test_gui_exposes_pack_preview_and_unpack_conflict_strategy(self):
        source = _source("gui/main_window.py")

        self.assertIn("preview = packer.preview()", source)
        self.assertIn("_choose_conflict_strategy", source)
        self.assertIn("conflict_strategy=conflict_strategy", source)

    def test_gui_only_offers_conflict_strategy_for_zip_archives(self):
        source = _source("gui/main_window.py")

        self.assertIn("archive_path: str", source)
        self.assertIn('os.path.splitext(archive_path)[1].lower() != ".zip"', source)


if __name__ == "__main__":
    unittest.main()
