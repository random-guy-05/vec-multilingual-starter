# Verification log

## 2026-09-30

Purpose: establish the technical facts shared by every translated guide.

Checked official pages:
- https://virtualembryo.ai/challenge
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
- https://virtualembryo.ai/challenge/baselines
- https://virtualembryo.ai/challenge/community

Confirmed:
- five current validation board IDs;
- board gene counts;
- board minimum/maximum cell counts;
- T1 expression-only vs T2/T3 expression + `spatial_3D`;
- non-negative, finite, log-normalised submission expression requirement;
- 1200 MB file cap;
- P3 two-official-submissions-per-board rule;
- Agent evidence requirement;
- P3 start date shown by the Challenge timeline.

Upstream tutorial/tooling consulted:
- https://github.com/xxx12e/vec-community-kit
- revision `13ad9baae8f85a8dd121e972c3a87cda8678ec90`
- English and Chinese tutorials
- baseline/validator/local-score/Agent evidence documentation

Important scope note:
This repository does not claim to have independently re-run the upstream toolkit's full data dry run. The executable helper commands are intentionally delegated to and attributed to the upstream repository, whose own tests and run logs document that tooling. This repository's contribution is multilingual onboarding, synchronized technical facts, and maintenance infrastructure.

Automated repository check:
`python scripts/check_sync.py`

The check verifies that every language guide contains all five current board IDs, their key numeric bounds, required AnnData terminology, the baseline/validation/local-score/Agent workflow commands, and the official Data/Rules URLs.
