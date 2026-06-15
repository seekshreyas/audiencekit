from __future__ import annotations

from pathlib import Path


BLOCKED_REFERENCES = [
    "synthetic" + "_gss2",
    "synthetic" + "-gss",
    "MADS " + "W4",
    "workshop " + "demo",
]

SKIP_DIRS = {
    ".agents",
    ".claude",
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "results",
}


def test_no_old_project_references_in_source_tree() -> None:
    root = Path(__file__).resolve().parents[1]
    offenders: list[str] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS or part.endswith(".egg-info") for part in path.parts):
            continue
        if path.suffix in {".pyc", ".jpg", ".whl", ".gz"}:
            continue
        text = path.read_text(errors="ignore")
        for needle in BLOCKED_REFERENCES:
            if needle.lower() in text.lower():
                offenders.append(f"{path.relative_to(root)} contains {needle}")

    assert offenders == []
