# ゼロから最初の VEC submission まで — 日本語

**技術情報の最終確認日: 2026-09-30。**  
このガイドと公式サイトが異なる場合は、必ず公式サイトを優先してください。

## 1. 必要なもの

登録・ダウンロード・提出には：
- Virtual Embryo Challenge アカウント
- 提出する場合は登録済み team
- `.h5ad` ファイルを保存できる十分なディスク容量

補助ツールのインストール：

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

pseudo-split でローカル scoring を行う場合：

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. 登録とデータのダウンロード

1. https://virtualembryo.ai/challenge を開く。
2. サインインして team を登録する。
3. https://virtualembryo.ai/challenge/data を開く。
4. 公開済み training data をダウンロードする。
5. 元ファイルは変更せず保存する。

## 3. 現在の5つの validation board

| Board | Target | Genes | 許可 cell 数 | 3D 座標 | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | 不要 | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | 必要 | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | 必要 | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | 必要 | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | 必要 | `wt_identity` |

重要な形式ルール：
- 1 submission = 1つの AnnData `.h5ad`
- `.X` は cells × genes、finite、non-negative、かつ log-normalised 済み
- `var_names` は board の gene list と順序に一致
- T2/T3 では finite な `obsm["spatial_3D"]` が必要
- 提出した `obs["celltype"]` は無視される
- ファイル上限は 1200 MB

Raw counts は構造チェックを通ることがありますが、score は誤ったものになります。

## 4. ツールが想定するデータ配置

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

実際のダウンロード名が違う場合は、その名前をコマンドに使ってください。

## 5. 各 board の baseline を作る

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

これは pipeline の確認用であり、競争用モデルではありません。

## 6. Upload 前に validate

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

board、gene order、cell 数、finite/non-negative 値、`spatial_3D`、log-normalisation を確認します。

## 7. pseudo-split で local score

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

同じ pseudo problem 上で自分の方法同士を比較するために使います。hidden leaderboard の予測ではありません。

## 8. Upload

1. https://virtualembryo.ai/challenge/account/submissions を開く。
2. 正しい board を選ぶ。
3. `.h5ad` を upload。
4. validation error を修正。
5. score と各 metric を確認。

Format validation の失敗は scored attempt を消費しません。現在の P3 ルールでは、phase 全体で各 board **2回の official submission** だけです。

## 9. Agent Team

Human Team はここを飛ばせます。

Agent Team は scoring 前に少なくとも2種類の evidence が必要で、賞の eligibility には trajectory・prompts・harness が必要です。

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

実際の agent run 前に公式 Rules を再確認してください。

## 10. よくあるミス

- T1 に 32,285 genes ではなく 500 genes を入れる。
- embryo T2 に 498 ではなく 500 genes を入れる。
- gene は正しいが順序が違う。
- raw counts または z-score 後の負値。
- T2/T3 に `obsm["spatial_3D"]` がない。
- cell 数が board の範囲外。
- pseudo-split を hidden ranking の予測とみなす。
- 禁止された held-out stage/genotype の外部データを使う。
- Agent evidence が不足。

## 11. Final phase

現在の timeline では P3 は **2026-10-20** 開始予定です。validation answers が training material になり、ranking は hidden test boards に移ります。P3 開始日に Rules と Data を再確認してください。

公式ソース：
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
