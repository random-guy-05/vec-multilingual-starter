# Translation and update policy

## Canonical source

The English guide is the canonical prose source for this repository. Technical facts should first be checked against [sources.md](sources.md), then propagated to every translation.

## What must never be translated

Keep these literal:

- board IDs such as `T2:heart:val_interp`
- command names
- file paths
- `.X`
- `var_names`
- `obsm["spatial_3D"]`
- `obs["celltype"]`
- URLs
- gene counts
- cell-count bounds

## Update rule

When an official rule changes:

1. Update [sources.md](sources.md) with the new verification date.
2. Update [tutorial_en.md](tutorial_en.md).
3. Make the same factual change in every translation.
4. Do not silently preserve old commands or limits for readability.

## Translation quality

Initial translations may be machine-assisted, but native-speaker corrections are explicitly welcome. The goal is technically faithful, clear language for first-time entrants rather than literary translation.

## Attribution

The multilingual project is inspired by and links to the MIT-licensed `vec-community-kit` English/Chinese tutorial. It does not claim authorship of that upstream tooling.
