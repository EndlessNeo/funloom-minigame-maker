#!/usr/bin/env python3
"""Package a Funloom minigame source directory as an upload ZIP."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

RESULT_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    return slug or "funloom-minigame"


def parse_result_ids(value: str) -> list[str]:
    if not value.strip():
        return ["success", "failure"]

    result_ids: list[str] = []
    for raw_item in value.split(","):
        item = raw_item.strip()
        if not item:
            continue
        if not RESULT_ID_RE.fullmatch(item):
            raise argparse.ArgumentTypeError(
                f"invalid result id: {item!r}; use ASCII letters, numbers, '_' or '-'"
            )
        if item not in result_ids:
            result_ids.append(item)
    return result_ids


def copy_source(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".DS_Store", "Thumbs.db")
    shutil.copytree(source, target, ignore=ignore)


def write_zip(source: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(source.rglob("*")):
            if not file.is_file():
                continue
            if any(part in {".git", "__pycache__"} for part in file.parts):
                continue
            archive.write(file, file.relative_to(source).as_posix())


def write_integration(
    output: Path,
    zip_name: str,
    orientation: str | bool,
    result_ids: list[str],
) -> None:
    project_orientation = (
        "landscape"
        if orientation is True
        else "portrait"
        if str(orientation).strip().lower() == "portrait"
        else "landscape"
    )
    interactive_video_shape = (
        "竖屏影游" if project_orientation == "portrait" else "横屏影游"
    )
    result_text = ", ".join(f"`{result_id}`" for result_id in result_ids)
    is_basic_mode = result_ids == ["success", "failure"]
    mode_text = (
        "Basic mode: keep the default success/failure exits."
        if is_basic_mode
        else (
            "Advanced mode: switch the Funloom minigame node to advanced mode and declare "
            "exactly this complete custom result set first: "
            f"{', '.join(result_ids)}."
        )
    )
    orientation_test_text = (
        "Test the PC stage and mobile horizontal stage for 横屏影游."
        if project_orientation == "landscape"
        else "Test the mobile vertical stage and centered desktop preview for 竖屏影游."
    )
    text = f"""# Funloom Minigame Node Integration

## Upload File

- ZIP: `{zip_name}`
- Entry: ZIP root `index.html`
- 互动影游方向：{interactive_video_shape}

## Declared Results

- Results: {result_text}
- Mode: {mode_text}

## Funloom Test Steps

1. Open the Funloom interactive story creator tool.
2. Upload the ZIP in Resources > Minigames.
3. Create or select a minigame node.
4. Select this uploaded minigame resource.
5. Configure variable mutations for every declared result that needs them.
6. Connect every declared result exit before publishing to Funloom.
7. Enter the minigame from an option node and trigger each declared result.
8. Confirm each result reaches the intended plot or ending node.

## Notes

- The minigame only returns a result string; it does not directly modify story variables.
- Unknown or undeclared results are rejected by the Funloom runtime.
- The minigame follows the Funloom interactive video's 横屏影游/竖屏影游 shape; do not configure a separate minigame override.
- Shape test: {orientation_test_text}
"""
    (output / "INTEGRATION.md").write_text(text, encoding="utf-8")


def run_validator(skill_dir: Path, target: Path, result_ids: list[str]) -> None:
    validator = skill_dir / "scripts" / "validate_minigame.py"
    subprocess.run(
        [
            sys.executable,
            str(validator),
            str(target),
            "--results",
            ",".join(result_ids),
        ],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Package a Funloom minigame source directory.")
    parser.add_argument("source", help="Source directory with root index.html")
    parser.add_argument("--name", default="funloom-minigame", help="Output ZIP base name")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument(
        "--results",
        default="success,failure",
        type=parse_result_ids,
        help=(
            "Comma-separated declared result ids. Omit for basic success,failure; "
            "advanced mode uses exactly the ids provided."
        ),
    )
    parser.add_argument(
        "--forced-landscape",
        action="store_true",
        help="Deprecated compatibility alias for --orientation landscape",
    )
    parser.add_argument(
        "--orientation",
        choices=("landscape", "portrait"),
        default="landscape",
        help="Interactive video project playback orientation inherited by this minigame",
    )
    parser.add_argument(
        "--no-copy-source",
        action="store_true",
        help="Do not copy source into output/source",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()
    skill_dir = Path(__file__).resolve().parents[1]
    name = slugify(args.name)
    zip_path = output / f"{name}.zip"

    if not source.is_dir():
        print(f"[FAIL] source directory not found: {source}")
        return 1

    output.mkdir(parents=True, exist_ok=True)
    run_validator(skill_dir, source, args.results)

    if not args.no_copy_source:
        copy_source(source, output / "source")

    write_zip(source, zip_path)
    orientation = "landscape" if args.forced_landscape else args.orientation
    write_integration(output, zip_path.name, orientation, args.results)
    run_validator(skill_dir, zip_path, args.results)

    print(f"[OK] ZIP written: {zip_path}")
    if args.no_copy_source:
        print("[OK] Source copy skipped")
    else:
        print(f"[OK] Source copied: {output / 'source'}")
    print(f"[OK] Integration guide: {output / 'INTEGRATION.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
