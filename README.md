# VEC Multilingual Starter

**A multilingual zero-to-first-submission guide for the Virtual Embryo Challenge (NeurIPS 2026).**

This repository lowers the language barrier for first-time entrants by providing the same practical onboarding path in multiple languages, kept against one shared source-of-truth document.

> Independent community resource. Not an official Virtual Embryo Challenge repository and not affiliated with the organisers.

## Languages

| Language | Guide |
|---|---|
| English | [docs/tutorial_en.md](docs/tutorial_en.md) |
| Español | [docs/tutorial_es.md](docs/tutorial_es.md) |
| 简体中文 | [docs/tutorial_zh-CN.md](docs/tutorial_zh-CN.md) |
| हिन्दी | [docs/tutorial_hi.md](docs/tutorial_hi.md) |
| Português | [docs/tutorial_pt-BR.md](docs/tutorial_pt-BR.md) |
| Français | [docs/tutorial_fr.md](docs/tutorial_fr.md) |
| العربية | [docs/tutorial_ar.md](docs/tutorial_ar.md) |
| 日本語 | [docs/tutorial_ja.md](docs/tutorial_ja.md) |
| 한국어 | [docs/tutorial_ko.md](docs/tutorial_ko.md) |

## What every guide covers

1. Registering and downloading the released data.
2. What each of the five current validation boards asks for.
3. The exact current gene-count and cell-count bounds.
4. Installing the official/community tooling used by the walkthrough.
5. Building a simple baseline submission file.
6. Validating the file before upload.
7. Scoring locally on a pseudo split.
8. Uploading to the Challenge portal.
9. What changes in the final phase.
10. Agent Team evidence requirements.
11. Common first-submission mistakes.

The guides are intentionally synchronized: the technical facts live in [docs/sources.md](docs/sources.md), while the translated guides explain the same workflow in each language.

## Current board contract

Verified **2026-09-30** against the official Challenge Data page.

| Board | Genes | Allowed cells | Output |
|---|---:|---:|---|
| `T1:val` | 32,285 | 1,000–5,118 | expression |
| `T2:embryo:val_interp` | 498 | 583–5,000 | expression + 3D coordinates |
| `T2:heart:val_extrap` | 500 | 1,000–25,179 | expression + 3D coordinates |
| `T2:heart:val_interp` | 500 | 1,000–17,616 | expression + 3D coordinates |
| `T3:gata4` | 500 | 1,000–7,449 | mutant expression + 3D coordinates |

Official source: https://virtualembryo.ai/challenge/data

## Upstream tutorial and tooling

This project was inspired by the excellent bilingual tutorial in:

- https://github.com/xxx12e/vec-community-kit
- Chinese tutorial: https://github.com/xxx12e/vec-community-kit/blob/main/docs/tutorial_zh.md
- English tutorial: https://github.com/xxx12e/vec-community-kit/blob/main/docs/tutorial_en.md

Pinned upstream revision used while preparing this multilingual expansion:

`13ad9baae8f85a8dd121e972c3a87cda8678ec90`

The upstream repository is MIT licensed. This repository does **not** reproduce its tutorial line-for-line; it provides an original, shorter multilingual onboarding guide while retaining attribution and linking users to the upstream tooling for executable helpers.

## Why a separate multilingual repo?

The Challenge explicitly says that translations count as community contributions and gives a Chinese tutorial as an example of useful reach. A single synchronized multilingual landing page makes it easier for students and first-time entrants to discover the same instructions in their preferred language.

Official Community Contribution Award page:
https://virtualembryo.ai/challenge/community

## Supporting docs

- [Technical sources and verification date](docs/sources.md)
- [Metrics overview](docs/metrics_overview.md)
- [Translation and update policy](docs/translation_policy.md)
- [Community Contribution submission text](COMMUNITY_SUBMISSION.md)

## Important caveats

- The official Challenge website, rules, board contracts and scorer are always authoritative.
- Validation targets remain hidden until the final phase.
- A local pseudo split helps compare your own methods; it is **not** a preview of the hidden-target ranking.
- Raw counts can pass structural validation while still being wrong for scoring. Submission expression must already be log-normalised.
- External-data restrictions are task- and stage-specific. Check the current rules before using external data.
- Agent Team prize eligibility requires evidence. The rules page is authoritative.

## Contributing translations

Native-speaker corrections are welcome. Please preserve commands, board IDs, file keys and official URLs exactly; translate the explanation around them rather than translating code tokens.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. Upstream inspiration is separately credited above.
