# From zero to a first VEC submission — English

**Last technical verification: 2026-09-30.**  
Official rules and board contracts always win if this guide and the website disagree.

## 1. What you need

For registration/download/upload:
- a Virtual Embryo Challenge account;
- a registered team if you want to submit;
- enough disk space for the released `.h5ad` files.

For the helper commands below:
- Python 3.10+;
- Git;
- the community toolkit:

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

For local pseudo-split scoring, also install the tested scorer revision:

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. Register and download

1. Open https://virtualembryo.ai/challenge
2. Sign in and register your team.
3. Open https://virtualembryo.ai/challenge/data
4. Download the released training files.
5. Keep the original files unchanged. Work on copies or derived outputs.

The official Data page is the source of truth for filenames, stages, gene panels and board limits.

## 3. Know the five current validation boards

| Board | Target | Genes | Allowed cells | Coordinates | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | no | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | yes | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | yes | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | yes | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | yes | `wt_identity` |

Important format rules:

- one AnnData `.h5ad` file per submission;
- `.X` must be cells × genes, finite, non-negative and already log-normalised;
- `var_names` must equal the board gene list in the expected order;
- Tasks 2/3 require finite `obsm["spatial_3D"]`; only the first 3 columns are read;
- submitted `obs["celltype"]` is optional and ignored;
- the file must be at most 1200 MB.

A raw-count matrix can pass structural validation and still be scored incorrectly. Check the scale yourself.

## 4. Put the data in the layout used by the helper toolkit

The upstream tutorial uses paths like:

```text
data/raw/T1/E8.5_RNA.h5ad
data/raw/T1/E9.5_RNA.h5ad

data/raw/T2_embryo/E6.75.h5ad
data/raw/T2_embryo/E7.25.h5ad
data/raw/T2_embryo/E8.0.h5ad

data/raw/T2_heart/E8.25_late.h5ad
data/raw/T2_heart/E8.75.h5ad
data/raw/T2_heart/E9.5.h5ad
```

If your downloaded filename differs, use your actual filename in the commands.

## 5. Build one known baseline for every board

These are plumbing checks, not competitive methods. Each command states the board's current cell bound next to it.

```bash
mkdir -p out

# T1:val — allowed 1,000–5,118 cells
python -m vec_community_baselines.make_baseline   --method copy_last   --board T1:val   --last data/raw/T1/E9.5_RNA.h5ad   --out out/t1_copy_last.h5ad   --n-cells 5000

# T2:embryo:val_interp — allowed 583–5,000 cells
python -m vec_community_baselines.make_baseline   --method copy_last   --board T2:embryo:val_interp   --last data/raw/T2_embryo/E8.0.h5ad   --out out/embryo_copy_last.h5ad   --n-cells 5000

# T2:heart:val_interp — allowed 1,000–17,616 cells
python -m vec_community_baselines.make_baseline   --method copy_last   --board T2:heart:val_interp   --last data/raw/T2_heart/E8.25_late.h5ad   --out out/heart_interp_copy_last.h5ad   --n-cells 5000

# T2:heart:val_extrap — allowed 1,000–25,179 cells
python -m vec_community_baselines.make_baseline   --method copy_last   --board T2:heart:val_extrap   --last data/raw/T2_heart/E9.5.h5ad   --out out/heart_extrap_copy_last.h5ad   --n-cells 5000

# T3:gata4 — allowed 1,000–7,449 cells
python -m vec_community_baselines.make_baseline   --method wt_identity   --board T3:gata4   --wt data/raw/T2_heart/E8.75.h5ad   --out out/t3_wt_identity.h5ad   --n-cells 5000
```

## 6. Validate before uploading

Example:

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

A local pass is useful, but the portal remains authoritative.

Check every file for:
- correct board;
- correct gene panel/order;
- allowed cell count;
- finite/non-negative expression;
- correct spatial key on T2/T3;
- log-normalised expression, which structural validation cannot prove.

## 7. Score on a pseudo split

A pseudo split uses released stages to compare **your own methods** before spending leaderboard attempts. It does not reveal the hidden target.

Example for T2 heart interpolation:

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

Use the score to compare candidate methods on the same pseudo problem, not to predict your leaderboard score.

## 8. Upload

1. Go to https://virtualembryo.ai/challenge/account/submissions
2. Choose the exact board.
3. Upload the corresponding `.h5ad`.
4. Fix any validation error before scoring.
5. Read the resulting score and per-metric breakdown.

A rejected validation does not consume a scored attempt. Current P3 rules allow only **two official submissions per board for the whole final phase**, so be conservative once P3 begins.

## 9. Agent Team evidence

Human Team entrants can skip this section.

The Agent Team follows the same benchmark but must show that the submitted result came from the autonomous agent run. Current rules require at least two evidence types before an Agent submission is scored, and prize eligibility requires **trajectory, prompts and harness**.

The upstream toolkit provides an evidence skeleton. Example:

```bash
# Verify the evidence package on a synthetic stand-in run
python -m pytest tests/test_evidence.py -q

# Lock a run without launching it
python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

# Real Claude Code run: lock -> run -> postrun
python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

# Build upload evidence
python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

Read the current Agent rules before a real run. Do not assume an evidence helper itself proves compliance.

## 10. Common first-submission mistakes

- T1 file has 500 genes instead of 32,285.
- Embryo T2 file has 500 genes even though the current validation board has 498.
- Correct genes, wrong order.
- Raw counts instead of log-normalised expression.
- Negative values caused by z-scoring/centering.
- Missing `obsm["spatial_3D"]` on T2/T3.
- Too many or too few cells for the selected board.
- Treating local pseudo-split rank as a prediction of hidden-test rank.
- Using external held-out-stage/genotype data prohibited by the rules.
- Agent run is missing trajectory/prompts/harness evidence.

## 11. Final phase

The Challenge timeline currently says P3 begins **2026-10-20**. Validation answers then become training material and ranking moves to hidden test boards. Current rules permit two official submissions per board for the entire P3 phase, and they cannot be withdrawn.

Check the official Rules and Data pages again on the day you enter P3.

## Official sources

- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
- https://virtualembryo.ai/challenge/baselines

For deeper executable tooling and the original bilingual tutorial:
https://github.com/xxx12e/vec-community-kit
