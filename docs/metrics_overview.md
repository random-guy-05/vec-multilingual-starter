# Metrics overview

This is a short orientation, not a replacement for the official scoring page.

Official source: https://virtualembryo.ai/challenge/evaluation

## Task 1

Task 1 predicts a distribution of single-cell RNA expression.

Current score groups:
- Differential-expression gene recovery: 25%
- Change direction: 25%
- Cell-state distribution: 30%
- Gene-gene co-variation: 20%

The important beginner lesson: do not submit one average cell repeated many times. Mean-level metrics may look reasonable, but population/distribution metrics will expose the collapse.

## Task 2

Task 2 predicts expression **and** 3D spatial structure.

Current score groups:
- Expression change: 25%
- Cell-state distribution: 25%
- Tissue shape and growth scale: 25%
- Local spatial organisation: 25%

Coordinates are allowed in any global translation/rotation frame. The scorer focuses on relational structure rather than absolute atlas registration.

## Task 3

Task 3 predicts the knockout embryo itself, using a matched wild-type reference.

Current score groups:
- Response gene recovery: 30%
- Response direction: 25%
- Response magnitude: 25%
- Cell-state distribution: 20%

Do not submit only a delta matrix. The prediction file represents the mutant embryo.

## Floor and ceiling

Every board is calibrated between:
- a **floor**: the task's do-nothing baseline (score 50 by construction), and
- an attainable **ceiling**: a split-half estimate from the real held-out target.

A model can score below 50 if it is worse than doing nothing, and can reach or exceed the published ceiling before clipping.

For formulas and current calibration anchors, use the official Evaluation page.
