# Kaggle Playground Ops

A reusable Codex Skill for running Kaggle Playground tabular competitions with separate evidence tracks for OOF validation, Public leaderboard exploration, and final submission selection.

这是一套面向 Kaggle Playground 表格赛的 Codex 工作流。它不把 Public 分数、OOF 结果和公开 notebook 混成一种证据，而是分别管理：

- **Stable OOF track**：用嵌套验证、折间稳定性和类别召回选择 Private hedge。
- **Public exploration track**：对公开预测做指纹去重，通过单变量提交验证榜单假设。
- **Final selection track**：在两个最终名额中分别保留 Public attack 和独立 OOF hedge。

## Install

Clone the repository into your Codex skills directory:

```powershell
git clone https://github.com/kenNethhao8/kaggle-playground-ops.git "$HOME\.codex\skills\kaggle-playground-ops"
```

macOS / Linux:

```bash
git clone https://github.com/kenNethhao8/kaggle-playground-ops.git ~/.codex/skills/kaggle-playground-ops
```

Restart Codex after installation if the skill is not discovered immediately.

## Use

Invoke it explicitly:

```text
$kaggle-playground-ops 接管这个 Kaggle 比赛，审计现状并规划最终两个提交。
```

Typical requests:

```text
$kaggle-playground-ops 检查这些公开 notebook 是否只是重复预测，并判断哪些值得提交。

$kaggle-playground-ops 审计我的 OOF、Public/Private 风险和最后两个版本的选择。

$kaggle-playground-ops 根据 HANDOFF.md 继续推进比赛，但不要污染独立模型路线。
```

The skill can also trigger implicitly for Kaggle Playground work involving OOF/CV, public prediction assets, leaderboard diagnostics, submission diffs, or final-selection risk.

## Included tools

| File | Purpose |
|---|---|
| `scripts/submission_diff.py` | Align two hard-label submissions by ID and report changed rows, agreement, and fingerprints |
| `scripts/fingerprint_assets.py` | Hash downloaded assets and deduplicate equivalent label vectors |
| `scripts/oof_audit.py` | Audit probability validity, ID uniqueness, balanced accuracy, class recall, and fold scores |
| `assets/HANDOFF.template.md` | Preserve competition state for takeover and continuation |
| `assets/experiment_ledger.template.csv` | Log hypotheses, lineage, diffs, evidence grades, and leaderboard results |
| `references/playbook.md` | Detailed three-track operating playbook |

The audit script requires Python, pandas, and NumPy. The fingerprint and submission-diff scripts use only the Python standard library.

## Core rules

1. Never tune and report on the same OOF labels.
2. Never trust a notebook title or claimed score without downloading its actual output.
3. Change one factor per diagnostic submission and log the hypothesis first.
4. Treat directly validated Public rows as Public-only evidence.
5. Do not spend both final slots on submissions that differ only on known Public rows.

## Repository structure

```text
kaggle-playground-ops/
├── SKILL.md
├── agents/openai.yaml
├── references/playbook.md
├── scripts/
│   ├── fingerprint_assets.py
│   ├── oof_audit.py
│   └── submission_diff.py
└── assets/
    ├── HANDOFF.template.md
    └── experiment_ledger.template.csv
```

## License

[MIT](LICENSE)
