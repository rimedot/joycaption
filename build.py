#!/usr/bin/env python3
"""Build this plugin's .mevax for Meva.

A .mevax is a zip of manifest.json, README.md and LICENSE (deflate), the
layout Meva's plugin SDK writes. The file is named after the repository:
<name>.mevax.

    python3 build.py              # build from the manifest
    python3 build.py --tag v1.2.0 # also check the manifest version is the tag

No dependencies beyond Python 3.8+.
"""

import argparse
import json
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRIES = ["manifest.json", "README.md", "LICENSE"]
# A fixed time, so the same files always give the same .mevax.
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def fail(message: str) -> None:
    print(f"build.py: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tag", help="release tag; the manifest version must equal it without a leading v")
    parser.add_argument("--out", help="output file (default <name>.mevax next to this script)")
    args = parser.parse_args()

    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    source = manifest.get("source", "")
    prefix = "https://github.com/"
    if not source.startswith(prefix) or source[len(prefix):].count("/") != 1:
        fail(f"source must be https://github.com/<owner>/<repo>, not {source!r}")
    expected_id = "github.com/" + source[len(prefix):].lower()
    if manifest.get("id") != expected_id:
        fail(f"id must be {expected_id} (its source), not {manifest.get('id')!r}")
    version = manifest.get("version", "")
    if args.tag is not None:
        tag = args.tag[1:] if args.tag.startswith("v") else args.tag
        if tag != version:
            fail(f"manifest version {version} is not the release tag {args.tag}")

    name = source.rstrip("/").rsplit("/", 1)[1]
    out = Path(args.out) if args.out else HERE / f"{name}.mevax"
    with zipfile.ZipFile(out, "w") as archive:
        for entry in ENTRIES:
            path = HERE / entry
            if not path.is_file():
                fail(f"missing {entry}")
            info = zipfile.ZipInfo(entry, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=6)
    print(f"Built {out.name} ({manifest['id']} {version})")


if __name__ == "__main__":
    main()
