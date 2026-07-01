#!/usr/bin/env python3
"""Audit row-level OOF probability files using pandas and numpy."""

import argparse
import json

import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("oof_csv")
    parser.add_argument("--id-column", required=True)
    parser.add_argument("--target-column", required=True)
    parser.add_argument("--prob-columns", nargs="+", required=True)
    parser.add_argument("--class-labels", nargs="+", required=True)
    parser.add_argument("--fold-column")
    args = parser.parse_args()
    if len(args.prob_columns) != len(args.class_labels):
        parser.error("probability columns and class labels must have equal length")
    frame = pd.read_csv(args.oof_csv)
    needed = [args.id_column, args.target_column, *args.prob_columns]
    missing = [column for column in needed if column not in frame]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    probs = frame[args.prob_columns].to_numpy(float)
    predicted = np.asarray(args.class_labels)[np.argmax(probs, axis=1)]
    actual = frame[args.target_column].astype(str).to_numpy()
    recalls = {label: float(np.mean(predicted[actual == label] == label)) for label in args.class_labels}
    result = {
        "rows": len(frame),
        "unique_ids": int(frame[args.id_column].nunique()),
        "nan_probability_cells": int(np.isnan(probs).sum()),
        "negative_probability_cells": int((probs < 0).sum()),
        "zero_sum_rows": int(np.isclose(probs.sum(axis=1), 0).sum()),
        "row_sum_max_error": float(np.max(np.abs(probs.sum(axis=1) - 1))),
        "balanced_accuracy": float(np.mean(list(recalls.values()))),
        "per_class_recall": recalls,
    }
    if args.fold_column:
        if args.fold_column not in frame:
            raise ValueError(f"missing fold column: {args.fold_column}")
        result["fold_balanced_accuracy"] = {
            str(fold): float(np.mean([np.mean(predicted[index][actual[index] == label] == label)
                                      for label in args.class_labels]))
            for fold, index in frame.groupby(args.fold_column).groups.items()
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
