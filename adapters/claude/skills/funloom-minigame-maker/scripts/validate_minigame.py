#!/usr/bin/env python3
"""Validate a Funloom minigame source directory or ZIP."""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
import tempfile
import zipfile
from pathlib import Path

MAX_BYTES = 50 * 1024 * 1024
TEXT_SUFFIXES = {
    ".html",
    ".htm",
    ".css",
    ".js",
    ".mjs",
    ".json",
    ".txt",
    ".md",
    ".svg",
}
REFERENCE_RE = re.compile(
    r"""(?:src|href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\)|import\s+[^"']*["']([^"']+)["']""",
    re.IGNORECASE,
)
EXTERNAL_RE = re.compile(r"^(?:https?:)?//|^(?:https?|data|blob|mailto|tel):", re.IGNORECASE)
RESULT_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
STRICT_BINARY_GUARD_RE = re.compile(
    r"""result\s*!==\s*["']success["']\s*&&\s*result\s*!==\s*["']failure["']"""
)


def fail(message: str) -> None:
    print(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def warn(message: str) -> None:
    print(f"[WARN] {message}")


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


def has_result_literal(text: str, result_id: str) -> bool:
    return f'"{result_id}"' in text or f"'{result_id}'" in text


def is_safe_zip_member(name: str) -> bool:
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("../"):
        return False
    return "/../" not in normalized


def extract_if_zip(path: Path) -> tuple[Path, tempfile.TemporaryDirectory[str] | None]:
    if path.is_dir():
        return path, None
    temp = tempfile.TemporaryDirectory()
    with zipfile.ZipFile(path) as archive:
        for member in archive.namelist():
            if not is_safe_zip_member(member):
                raise ValueError(f"unsafe ZIP path: {member}")
        archive.extractall(temp.name)
    return Path(temp.name), temp


def iter_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*") if path.is_file()]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def normalize_reference(base_file: Path, ref: str) -> str | None:
    value = ref.strip()
    if not value or value.startswith("#"):
        return None
    if EXTERNAL_RE.search(value):
        return value
    if value.startswith("/"):
        return value
    value = value.split("#", 1)[0].split("?", 1)[0]
    if not value:
        return None
    base = base_file.parent.as_posix()
    return posixpath.normpath(posixpath.join(base, value))


def collect_references(root: Path, files: list[Path]) -> tuple[list[str], list[str]]:
    existing = {path.relative_to(root).as_posix() for path in files}
    missing: list[str] = []
    external: list[str] = []

    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(root)
        text = read_text(path)
        for match in REFERENCE_RE.finditer(text):
            raw = next((group for group in match.groups() if group), "")
            ref = normalize_reference(relative, raw)
            if not ref:
                continue
            if EXTERNAL_RE.search(ref):
                external.append(f"{relative.as_posix()} -> {raw}")
            elif ref not in existing:
                missing.append(f"{relative.as_posix()} -> {raw}")
    return missing, external


def validate(path: Path, result_ids: list[str]) -> int:
    errors = 0
    if not path.exists():
        fail(f"path not found: {path}")
        return 1
    if path.is_file() and path.suffix.lower() != ".zip":
        fail("input must be a directory or .zip file")
        return 1
    if path.is_file() and path.stat().st_size > MAX_BYTES:
        fail("ZIP is larger than 50 MB")
        errors += 1

    root, temp = extract_if_zip(path)
    try:
        files = iter_files(root)
        total_size = sum(file.stat().st_size for file in files)
        if total_size > MAX_BYTES:
            fail("source files are larger than 50 MB")
            errors += 1
        else:
            ok("size is within 50 MB")

        index = root / "index.html"
        if index.exists() and index.is_file():
            ok("root index.html exists")
        else:
            fail("root index.html is missing")
            errors += 1

        all_text = "\n".join(read_text(file) for file in files if file.suffix.lower() in TEXT_SUFFIXES)
        if "funloom:minigame:complete" in all_text:
            ok("Funloom completion message type found")
        else:
            fail("Funloom completion message type is missing")
            errors += 1

        for result_id in result_ids:
            if has_result_literal(all_text, result_id):
                ok(f"{result_id} result found")
            else:
                fail(f"{result_id} result is missing")
                errors += 1

        custom_result_ids = [result_id for result_id in result_ids if result_id not in {"success", "failure"}]
        if custom_result_ids and STRICT_BINARY_GUARD_RE.search(all_text):
            fail("strict success/failure guard found; it would block custom results")
            errors += 1

        missing, external = collect_references(root, files)
        if external:
            for item in external:
                fail(f"external resource: {item}")
            errors += len(external)
        else:
            ok("no external resources found")

        if missing:
            for item in missing:
                fail(f"missing resource: {item}")
            errors += len(missing)
        else:
            ok("referenced local resources exist")

        non_ascii = [file.relative_to(root).as_posix() for file in files if not file.relative_to(root).as_posix().isascii()]
        if non_ascii:
            warn("non-ASCII file names are present; ensure Funloom upload and playback paths are tested")
            for name in non_ascii:
                print(f"       {name}")

        if errors:
            fail(f"validation finished with {errors} issue(s)")
            return 1
        ok("validation passed")
        return 0
    finally:
        if temp:
            temp.cleanup()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Funloom minigame directory or ZIP.")
    parser.add_argument("path", help="Source directory or ZIP path")
    parser.add_argument(
        "--results",
        default="success,failure",
        type=parse_result_ids,
        help=(
            "Comma-separated declared result ids. Omit for basic success,failure; "
            "advanced mode uses exactly the ids provided."
        ),
    )
    args = parser.parse_args()
    return validate(Path(args.path).resolve(), args.results)


if __name__ == "__main__":
    raise SystemExit(main())
