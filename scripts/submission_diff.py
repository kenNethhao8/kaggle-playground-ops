#!/usr/bin/env python3
"""Compare two hard-label Kaggle submissions after aligning by ID."""

import argparse
import csv
import hashlib
from pathlib import Path


def read_labels(path, id_column, target_column):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or id_column not in reader.fieldnames or target_column not in reader.fieldnames:
            raise ValueError(f"{path}: missing {id_column!r} or {target_column!r}")
        rows = list(reader)
    labels = {row[id_column]: row[target_column] for row in rows}
    if len(labels) != len(rows):
        raise ValueError(f"{path}: duplicate IDs")
    return labels


def fingerprint(labels):
    payload = "\n".join(f"{key}\t{labels[key]}" for key in sorted(labels))
    return hashlib.sha256(payload.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("left")
    parser.add_argument("right")
    parser.add_argument("--id-column", required=True)
    parser.add_argument("--target-column", required=True)
    args = parser.parse_args()
    left = read_labels(args.left, args.id_column, args.target_column)
    right = read_labels(args.right, args.id_column, args.target_column)
    if left.keys() != right.keys():
        raise ValueError("submission ID sets differ")
    changed = [key for key in sorted(left) if left[key] != right[key]]
    print(f"rows,{len(left)}")
    print(f"diff_rows,{len(changed)}")
    print(f"agreement,{1 - len(changed) / len(left):.9f}")
    print(f"left_sha256,{fingerprint(left)}")
    print(f"right_sha256,{fingerprint(right)}")
    for key in changed[:20]:
        print(f"diff,{key},{left[key]},{right[key]}")


if __name__ == "__main__":
    main()
