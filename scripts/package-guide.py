#!/usr/bin/env python3
"""Validate the reviewed public guide and rebuild its manifest and download ZIP."""

import hashlib
import json
import re
import zipfile
from datetime import date
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "guide"
MANIFEST = GUIDE / "package-manifest.json"
ARCHIVE = ROOT / "downloads" / "min-agent-guide.zip"


def build():
    files = sorted(p for p in GUIDE.rglob("*") if p.is_file() and p != MANIFEST)
    if not files or not (GUIDE / "README.md").is_file() or not (GUIDE / "AGENTS.md").is_file():
        raise ValueError("Missing public guide entry files")
    records = []
    for path in files:
        relative = path.relative_to(GUIDE)
        if path.is_symlink() or "원본" in relative.parts or path.name == "원본 목록.json":
            raise ValueError(f"Excluded source or symlink: {relative}")
        data = path.read_bytes()
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^\n)]+)\)", data.decode("utf-8")):
                target = target.strip("<>")
                if re.match(r"(?:https?://|mailto:|#)", target):
                    continue
                destination = (path.parent / unquote(target.split("#")[0])).resolve()
                if not destination.is_relative_to(GUIDE) or not destination.exists():
                    raise ValueError(f"Unresolved package link: {relative}: {target}")
        records.append({"path": relative.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    manifest = {"schemaVersion": 1, "package": "min-agent-guide", "generatedDate": date.today().isoformat(),
                "scope": "Reviewed public construction documents; excludes personal raw sources and filled operational records.",
                "hashAlgorithm": "sha256", "manifestExcludedFromFileHashes": True, "files": records}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ARCHIVE.parent.mkdir(exist_ok=True)
    packaged = sorted(files + [MANIFEST])
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in packaged:
            info = zipfile.ZipInfo("guide/" + path.relative_to(GUIDE).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(packaged)
        for item in records:
            assert hashlib.sha256(archive.read("guide/" + item["path"])).hexdigest() == item["sha256"]
    print(json.dumps({"documents": len(files), "zipEntries": len(packaged), "zipBytes": ARCHIVE.stat().st_size,
                      "zipSha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()}, ensure_ascii=False))


if __name__ == "__main__":
    build()
