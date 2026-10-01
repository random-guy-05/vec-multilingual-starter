# शून्य से पहली VEC submission तक — हिन्दी

**तकनीकी जानकारी अंतिम बार जाँची गई: 2026-09-30।**  
यदि इस गाइड और आधिकारिक वेबसाइट में अंतर हो, तो आधिकारिक वेबसाइट को सही मानें।

## 1. क्या चाहिए

Registration, download और upload के लिए:
- Virtual Embryo Challenge account;
- submission के लिए registered team;
- `.h5ad` files के लिए पर्याप्त disk space.

Community helper tools install करें:

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

Local pseudo-split scoring के लिए:

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. Register और data download करें

1. https://virtualembryo.ai/challenge खोलें।
2. Sign in करके team register करें।
3. https://virtualembryo.ai/challenge/data खोलें।
4. Released training data download करें।
5. Original files को unchanged रखें; experiments के लिए copies/derived outputs उपयोग करें।

## 3. पाँच current validation boards

| Board | Target | Genes | Allowed cells | 3D coordinates | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | नहीं | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | हाँ | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | हाँ | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | हाँ | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | हाँ | `wt_identity` |

मुख्य format rules:
- एक submission = एक AnnData `.h5ad`;
- `.X` cells × genes, finite, non-negative और पहले से log-normalised होना चाहिए;
- `var_names` board के gene list और order से match होना चाहिए;
- T2/T3 में finite `obsm["spatial_3D"]` जरूरी है;
- submitted `obs["celltype"]` scorer ignore करता है;
- file size 1200 MB से अधिक नहीं हो सकता।

Raw counts structural validation पास कर सकते हैं लेकिन score गलत होगा।

## 4. Helper toolkit की data layout

Upstream tutorial में paths इस तरह हैं:

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

आपकी downloaded filename अलग हो तो command में वास्तविक filename दें।

## 5. हर board के लिए एक baseline बनाएँ

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

ये competitive models नहीं हैं; इनका उद्देश्य pipeline को end-to-end जाँचना है।

## 6. Upload से पहले validate करें

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

Board, gene order, cell count, finite/non-negative values, spatial key और log-normalisation को जाँचें।

## 7. Pseudo split पर local score

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

यह आपके methods की आपस में तुलना करने के लिए है। Hidden leaderboard score का अनुमान नहीं है।

## 8. Upload

1. https://virtualembryo.ai/challenge/account/submissions पर जाएँ।
2. सही board चुनें।
3. संबंधित `.h5ad` upload करें।
4. Validation error आए तो पहले ठीक करें।
5. Score और metric breakdown देखें।

Rejected format validation scored attempt नहीं खर्च करता। Current P3 rules में पूरे phase के लिए हर board पर केवल **2 official submissions** हैं।

## 9. Agent Team evidence

Human Team इस section को skip कर सकता है।

Agent Team के लिए scoring से पहले कम से कम दो evidence types चाहिए; prize eligibility के लिए rules trajectory, prompts और harness माँगते हैं।

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

Real agent run से पहले current official Rules दोबारा पढ़ें।

## 10. Common mistakes

- T1 में 32,285 के बजाय 500 genes।
- embryo T2 में 498 के बजाय 500 genes।
- सही genes लेकिन गलत order।
- raw counts या negative z-scored values।
- T2/T3 में `obsm["spatial_3D"]` missing।
- board limit से बाहर cell count।
- pseudo-split rank को hidden-test rank समझना।
- prohibited held-out stage/genotype external data का उपयोग।
- Agent evidence अधूरा होना।

## 11. Final phase

Current timeline के अनुसार P3 **2026-10-20** से शुरू होता है। Validation answers training material बनते हैं और ranking hidden test boards पर जाती है। P3 में current rules के अनुसार हर board पर केवल दो official submissions हैं और उन्हें withdraw नहीं किया जा सकता।

P3 शुरू होने के दिन official Rules और Data pages फिर से जाँचें।

Official sources:
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
