#!/usr/bin/env python3
"""Fingerprint CSV files by bytes and, optionally, ID-aligned labels."""

import argparse
import csv
import hashlib
from pathlib import Path


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def label_digest(path, id_column, target_column):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    pairs = sorted((row[id_column], row[target_column]) for row in rows)
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError(f"{path}: duplicate IDs")
    payload = "\n".join(f"{key}\t{value}" for key, value in pairs)
    return hashlib.sha256(payload.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--id-column")
    parser.add_argument("--target-column")
    args = parser.parse_args()
    if bool(args.id_column) != bool(args.target_column):
        parser.error("--id-column and --target-column must be used together")
    print("path,bytes,sha256,label_sha256")
    for raw_path in args.paths:
        path = Path(raw_path)
        labels = label_digest(path, args.id_column, args.target_column) if args.id_column else ""
        print(f"{path},{path.stat().st_size},{digest(path)},{labels}")


if __name__ == "__main__":
    main()
