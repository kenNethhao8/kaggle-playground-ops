# Kaggle Playground operating playbook

Use this playbook for tabular competitions with separate Public and Private leaderboards. The operating objective is expected final rank, not maximum visible Public score.

## 1. Initialize the evidence system

Create `data/`, `scripts/`, `outputs/`, `HANDOFF.md`, and `experiment_ledger.csv`. Record the metric, class order, split rules, external-data policy, submission quota, final-selection count, deadline, and timezone. Hash every submitted file.

Maintain three independent tracks:

1. **Stable OOF:** estimates generalization and supplies the Private hedge.
2. **Public exploration:** analyzes public notebooks, prediction assets, and controlled leaderboard feedback.
3. **Final selection:** assigns distinct roles to the available final slots.

## 2. Build the stable OOF track

Use stratified folds where appropriate. Save row-level OOF probabilities, fold IDs, test probabilities, ID order, and class order. Check row alignment, missing values, negative probabilities, zero-sum rows, fold scores, per-class recall, and leakage.

Any parameter learned from OOF labels—including blend weights, class biases, thresholds, and candidate filters—requires **nested validation**: tune on all but one fold and score on the held-out fold, rotating across folds.

Retain a candidate when most folds agree, no class is sacrificed materially, and its predictions add useful diversity. Prefer uncertainty intervals over tiny point-estimate gains.

## 3. Build the Public exploration track

Download actual notebook or dataset outputs. Normalize by ID, compute a fingerprint, deduplicate exact label vectors, and measure disagreement against current anchors. Different names with identical outputs are one evidence source.

Grade evidence:

| Grade | Evidence | Permitted use |
|---|---|---|
| A-grade | A controlled one-row or paired experiment directly changes leaderboard score in the expected direction | Validated Public-only patch |
| B-grade | Several genuinely independent probability assets agree, with supporting model or regression evidence | Candidate for a single-row diagnostic |
| C-grade | One notebook, title, claimed score, or regression signal alone | Research only; do not submit directly |

Each diagnostic submission changes one factor only: one row, one small patch group, one blend weight, or one class bias. Log the hypothesis, expected result, failure information, lineage, and diff rows before submission.

Under a disjoint Public/Private split, a row proven to affect Public contributes no Private score. Keep such rows in `validated_public_patches.csv`. They may be transferred to another anchor only after confirming the anchor still has the old labels and the resulting diff is exactly the expected patch set.

## 4. Use public anchors without contaminating the hedge

Treat a high-scoring public hard-label file as a candidate generator, not ground truth. To support an independently trained model:

1. Inspect only disagreement rows.
2. Ignore the anchor when the stable model has high confidence.
3. Consider support only where the stable model has low margin or high entropy and several fingerprint-distinct sources agree.
4. Apply a small logit bonus rather than a hard overwrite.
5. Select bonus strength and row cap using nested OOF.

## 5. Allocate submission budget

A reasonable starting allocation is 30% model/OOF validation, 30% public-asset reproduction, 20% controlled diagnostics, and 20% deadline reserve. Before every submission answer: What hypothesis does it test? What will failure teach? Is it redundant? Can it change final selection?

## 6. Select final submissions

With two final slots:

- **Public attack:** strongest Public candidate, including only A-grade validated Public patches.
- **Private hedge:** independently trained candidate selected by nested OOF, fold stability, per-class recall, and diversity, without row-wise leaderboard feedback.

Do not choose two candidates that differ only on known Public rows. Measure their overall agreement and disagreement counts before selection.

## 7. Deadline checklist

- Refresh rules, deadline, and leaderboard state.
- Download and fingerprint late public assets.
- Verify row count, schema, IDs, hashes, and exact Kaggle submission IDs.
- Confirm the two slots have distinct roles and lineages.
- Preserve the handoff, ledger, OOF artifacts, validated patches, and final files.
- Stop low-evidence guessing early enough to recover from upload mistakes.

## 8. Postmortem

Build this table after Private reveal:

`submission | public | private | gap | role | lineage | diff_rows | fingerprint`

Determine which Public gains came from confirmed Public rows, which public anchors failed collectively on Private, which OOF candidate generalized best, and whether the chosen hedge maximized expected Private performance given evidence available at selection time.

Classify misses as **method error** (leakage, alignment, reused evaluation labels), **risk choice** (reasonable aggressive/conservative decision), or **outcome variance** (sound process, unfavorable split). Do not rewrite history from the final rank alone.
