# 처음부터 첫 VEC submission까지 — 한국어

**기술 정보 최종 확인: 2026-09-30.**  
이 문서와 공식 사이트가 다르면 공식 사이트를 따르세요.

## 1. 준비물

등록, 다운로드, 업로드에 필요한 것:
- Virtual Embryo Challenge 계정
- 제출하려면 등록된 team
- `.h5ad` 파일을 저장할 충분한 디스크 공간

보조 커뮤니티 도구 설치:

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

pseudo-split local scoring을 하려면:

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. 등록과 데이터 다운로드

1. https://virtualembryo.ai/challenge 를 엽니다.
2. 로그인하고 team을 등록합니다.
3. https://virtualembryo.ai/challenge/data 를 엽니다.
4. 공개된 training data를 다운로드합니다.
5. 원본 파일은 수정하지 않고 보관합니다.

## 3. 현재 5개 validation board

| Board | Target | Genes | 허용 cell 수 | 3D 좌표 | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | 없음 | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | 필요 | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | 필요 | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | 필요 | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | 필요 | `wt_identity` |

핵심 형식 규칙:
- submission 하나당 AnnData `.h5ad` 하나;
- `.X`는 cells × genes, finite, non-negative, 이미 log-normalised 상태;
- `var_names`는 해당 board의 gene list와 순서를 정확히 일치;
- T2/T3는 finite한 `obsm["spatial_3D"]` 필요;
- 제출된 `obs["celltype"]`는 scorer가 무시;
- 파일 최대 크기 1200 MB.

Raw counts는 구조 검사를 통과할 수 있지만 scoring은 잘못될 수 있습니다.

## 4. 도구가 사용하는 데이터 경로

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

다운로드된 실제 파일명이 다르면 명령에서도 실제 이름을 사용하세요.

## 5. 각 board baseline 만들기

```bash
mkdir -p out

# T1:val — 1,000–5,118 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T1:val --last data/raw/T1/E9.5_RNA.h5ad   --out out/t1_copy_last.h5ad --n-cells 5000

# T2:embryo:val_interp — 583–5,000 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:embryo:val_interp --last data/raw/T2_embryo/E8.0.h5ad   --out out/embryo_copy_last.h5ad --n-cells 5000

# T2:heart:val_interp — 1,000–17,616 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_interp --last data/raw/T2_heart/E8.25_late.h5ad   --out out/heart_interp_copy_last.h5ad --n-cells 5000

# T2:heart:val_extrap — 1,000–25,179 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_extrap --last data/raw/T2_heart/E9.5.h5ad   --out out/heart_extrap_copy_last.h5ad --n-cells 5000

# T3:gata4 — 1,000–7,449 cells
python -m vec_community_baselines.make_baseline --method wt_identity   --board T3:gata4 --wt data/raw/T2_heart/E8.75.h5ad   --out out/t3_wt_identity.h5ad --n-cells 5000
```

이 baseline들은 경쟁용 모델이 아니라 end-to-end pipeline 확인용입니다.

## 6. 업로드 전 validation

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

board, gene panel/order, cell count, finite/non-negative 값, `spatial_3D`, log-normalisation을 확인하세요.

## 7. pseudo-split local score

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

같은 pseudo problem에서 본인의 여러 방법을 비교할 때 사용합니다. hidden leaderboard score 예측이 아닙니다.

## 8. 업로드

1. https://virtualembryo.ai/challenge/account/submissions 로 이동.
2. 정확한 board 선택.
3. 해당 `.h5ad` 업로드.
4. validation error 수정.
5. score와 metric breakdown 확인.

Format validation 실패는 scored attempt를 소모하지 않습니다. 현재 P3 규칙은 전체 phase 동안 board마다 **official submission 2회**만 허용합니다.

## 9. Agent Team

Human Team은 이 부분을 건너뛸 수 있습니다.

Agent Team은 scoring 전에 최소 두 종류의 evidence가 필요하며, prize eligibility에는 trajectory, prompts, harness가 필요합니다.

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

실제 Agent run 전에 최신 공식 Rules를 다시 읽으세요.

## 10. 자주 하는 실수

- T1에 32,285가 아니라 500 genes를 넣음.
- embryo T2에 498이 아니라 500 genes를 넣음.
- gene set은 맞지만 순서가 다름.
- raw counts 또는 z-score 후 음수 값.
- T2/T3에 `obsm["spatial_3D"]`가 없음.
- cell 수가 board 범위를 벗어남.
- pseudo-split을 hidden ranking 예측으로 해석.
- 금지된 held-out stage/genotype 외부 데이터를 사용.
- Agent evidence가 불완전함.

## 11. Final phase

현재 일정상 P3는 **2026-10-20** 시작 예정입니다. validation answer가 training material이 되고 ranking은 hidden test board로 이동합니다. P3 시작일에 Rules와 Data를 다시 확인하세요.

공식 소스:
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
