from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "funloom-minigame-maker" / "skills" / "funloom-minigame-maker"


def load_script(name: str):
    path = SKILL_DIR / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_minigame = load_script("validate_minigame")
package_minigame = load_script("package_minigame")


class ResultModeTests(unittest.TestCase):
    def test_skill_uses_creator_facing_orientation_prompt(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "您所需要设计的互动影游是横屏影游还是竖屏影游？这会涉及到后边小游戏的呈现方式。",
            skill_text,
        )
        self.assertNotIn("landscape 横屏", skill_text)
        self.assertNotIn("portrait 竖屏", skill_text)

    def test_integration_guide_uses_creator_facing_orientation_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            package_minigame.write_integration(
                output,
                "demo.zip",
                "portrait",
                ["success", "failure"],
            )

            text = (output / "INTEGRATION.md").read_text(encoding="utf-8")
            self.assertIn("互动影游方向：竖屏影游", text)
            self.assertNotIn("Project playback orientation", text)
            self.assertNotIn("portrait", text)

    def test_custom_results_are_not_forced_to_include_basic_results(self) -> None:
        self.assertEqual(
            validate_minigame.parse_result_ids("perfect,timeout"),
            ["perfect", "timeout"],
        )
        self.assertEqual(
            package_minigame.parse_result_ids("perfect"),
            ["perfect"],
        )

    def test_default_results_stay_basic_success_failure(self) -> None:
        self.assertEqual(
            validate_minigame.parse_result_ids(""),
            ["success", "failure"],
        )
        self.assertEqual(
            package_minigame.parse_result_ids(""),
            ["success", "failure"],
        )

    def test_advanced_validation_accepts_custom_only_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir)
            (source / "index.html").write_text(
                """
<!doctype html>
<script>
const FUNLOOM_ALLOWED_RESULTS = ["perfect"];
parent.postMessage({ type: "funloom:minigame:complete", result: "perfect" }, "*");
</script>
""".strip(),
                encoding="utf-8",
            )

            self.assertEqual(validate_minigame.validate(source, ["perfect"]), 0)

    def test_integration_guide_describes_advanced_without_basic_results(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            package_minigame.write_integration(
                output,
                "demo.zip",
                False,
                ["perfect", "timeout"],
            )

            text = (output / "INTEGRATION.md").read_text(encoding="utf-8")
            self.assertIn("Advanced mode", text)
            self.assertIn("`perfect`, `timeout`", text)
            self.assertIn("declare exactly this complete custom result set", text)
            self.assertNotIn("add these exact custom result ids", text)
            self.assertNotIn("success/failure", text)


if __name__ == "__main__":
    unittest.main()
