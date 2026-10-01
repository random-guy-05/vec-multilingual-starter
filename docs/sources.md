# Technical source of truth

Last verified: **2026-10-01**

The official Challenge website is authoritative. Translations in this repository should be updated when these sources change.

## Core official sources

- Challenge home / timeline: https://virtualembryo.ai/challenge
- Data and board contracts: https://virtualembryo.ai/challenge/data
- Tasks: https://virtualembryo.ai/challenge/tasks
- Evaluation and submission format: https://virtualembryo.ai/challenge/evaluation
- Rules: https://virtualembryo.ai/challenge/rules
- Reference baselines: https://virtualembryo.ai/challenge/baselines
- Community Contribution Award: https://virtualembryo.ai/challenge/community

## Five current validation boards

| Board | Genes | Allowed cells | Required spatial coordinates |
|---|---:|---:|---|
| `T1:val` | 32,285 | 1,000–5,118 | No |
| `T2:embryo:val_interp` | 498 | 583–5,000 | Yes |
| `T2:heart:val_extrap` | 500 | 1,000–25,179 | Yes |
| `T2:heart:val_interp` | 500 | 1,000–17,616 | Yes |
| `T3:gata4` | 500 | 1,000–7,449 | Yes |

Source: Challenge Data page, read 2026-09-30.

## Submission facts used throughout the translations

- Format: AnnData `.h5ad`.
- `.X` must be a 2D cells × genes matrix, finite and non-negative.
- Expression must already be log-normalised. Raw counts can pass structural checks and still be scored incorrectly.
- `var_names` must match the board's gene list and order.
- Task 1 has no spatial coordinates.
- Tasks 2 and 3 require `obsm["spatial_3D"]`; only the first three columns are read.
- Cell ordering is not matched against target cells.
- Submitted `obs["celltype"]` is optional and ignored by the scorer.
- Cell count must be inside the board's published minimum/maximum.
- A file may not exceed 1200 MB.
- Rejected format validation does not consume a scored attempt.
- In P3, there are two official submissions per board for the whole phase and they cannot be withdrawn.
- Agent Team submissions require evidence; prize eligibility specifically requires trajectory, prompts and harness.

## Released training data

The official atlas currently lists 9 training datasets, including:
- whole-embryo spatial stages E6.75, E7.25, E8.0;
- heart spatial stages E8.25, E8.75, E9.5;
- Mab21l2 KO at E9.5;
- Task-1 single-cell RNA at E8.5 and E9.5.

See: https://virtualembryo.ai/atlas/challenge-data

## Upstream community tutorial/tooling

- Repository: https://github.com/xxx12e/vec-community-kit
- English guide: https://github.com/xxx12e/vec-community-kit/blob/main/docs/tutorial_en.md
- Chinese guide: https://github.com/xxx12e/vec-community-kit/blob/main/docs/tutorial_zh.md
- Metrics overview: https://github.com/xxx12e/vec-community-kit/blob/main/docs/metrics_overview.md

Pinned revision consulted: `13ad9baae8f85a8dd121e972c3a87cda8678ec90`.

This multilingual repo is an original adaptation/expansion. For executable helper code, validators, baseline writers and evidence tooling, use the upstream repository directly.
