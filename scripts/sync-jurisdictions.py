#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Copy the canonical jurisdiction layer into each in-scope plugin.

Upstream keeps `references/` at the repo root and does not ship it inside plugins
(see the root CLAUDE.md, "Things to leave alone"). Plugins installed from the
marketplace therefore cannot read the root folder, so each in-scope plugin carries
its own copy at `<plugin>/references/jurisdictions/`. This script is the only
thing that writes those copies. Run it after editing anything under
`references/jurisdictions/`; run with `--check` in CI to fail if a copy is stale.

Usage:
  python3 scripts/sync-jurisdictions.py          # copy
  python3 scripts/sync-jurisdictions.py --check  # exit 1 if any copy differs
"""
import filecmp
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "references", "jurisdictions")
PLUGINS = ["commercial-legal", "corporate-legal", "employment-legal"]


def tree(path):
    out = {}
    for d, _, files in os.walk(path):
        for f in files:
            if f.startswith("."):
                continue
            full = os.path.join(d, f)
            out[os.path.relpath(full, path)] = full
    return out


def main():
    check = "--check" in sys.argv
    src = tree(SRC)
    stale = []
    for p in PLUGINS:
        dst_root = os.path.join(ROOT, p, "references", "jurisdictions")
        dst = tree(dst_root) if os.path.isdir(dst_root) else {}
        for rel, full in src.items():
            target = os.path.join(dst_root, rel)
            if rel not in dst or not filecmp.cmp(full, target, shallow=False):
                stale.append(f"{p}/references/jurisdictions/{rel}")
                if not check:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.copy2(full, target)
        for rel in dst:
            if rel not in src:
                stale.append(f"{p}/references/jurisdictions/{rel} (orphan)")
                if not check:
                    os.remove(os.path.join(dst_root, rel))
    if check:
        if stale:
            print("stale jurisdiction copies:\n  " + "\n  ".join(stale))
            return 1
        print("jurisdiction copies are current")
        return 0
    print(f"synced {len(src)} files into {len(PLUGINS)} plugins ({len(stale)} updated)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
