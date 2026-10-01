# 从零到第一次 VEC 提交 — 简体中文

**技术信息最后核对：2026-09-30。**  
如果本教程与官网不一致，请以 Virtual Embryo Challenge 官网为准。

## 1. 需要准备什么

注册、下载和提交需要：
- Virtual Embryo Challenge 账号；
- 如果要提交结果，需要注册 team；
- 足够存放 `.h5ad` 数据的磁盘空间。

安装本教程使用的社区工具：

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

如果要做本地 pseudo-split 评分，再安装测试过的 scorer：

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. 注册并下载数据

1. 打开 https://virtualembryo.ai/challenge
2. 登录并注册 team。
3. 打开 https://virtualembryo.ai/challenge/data
4. 下载已经发布的训练数据。
5. 原始文件尽量保持不变，用副本或生成的新文件做实验。

## 3. 当前五个 validation board

| Board | 目标 | 基因数 | 允许细胞数 | 3D 坐标 | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | 不需要 | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | 需要 | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | 需要 | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | 需要 | `copy_last` |
| `T3:gata4` | E8.75 Gata4 KO | 500 | 1,000–7,449 | 需要 | `wt_identity` |

关键格式规则：
- 每次提交一个 AnnData `.h5ad`；
- `.X` 必须是 cells × genes，有限、非负，并且已经做 log normalization；
- `var_names` 必须和该 board 的 gene list 及顺序完全一致；
- T2/T3 需要有限的 `obsm["spatial_3D"]`，只读取前三列；
- 提交里的 `obs["celltype"]` 可以没有，而且 scorer 会忽略它；
- 单文件最大 1200 MB。

特别注意：raw counts 可能通过结构检查，但依然会被按 log-normalized 数据错误评分。

## 4. 社区工具使用的数据目录

上游教程使用类似路径：

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

如果你下载到的文件名不同，请在命令中改成真实文件名。

## 5. 给每个 board 先做一个 baseline

```bash
mkdir -p out

# T1:val — 允许 1,000–5,118 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T1:val --last data/raw/T1/E9.5_RNA.h5ad   --out out/t1_copy_last.h5ad --n-cells 5000

# T2:embryo:val_interp — 允许 583–5,000 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:embryo:val_interp --last data/raw/T2_embryo/E8.0.h5ad   --out out/embryo_copy_last.h5ad --n-cells 5000

# T2:heart:val_interp — 允许 1,000–17,616 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_interp --last data/raw/T2_heart/E8.25_late.h5ad   --out out/heart_interp_copy_last.h5ad --n-cells 5000

# T2:heart:val_extrap — 允许 1,000–25,179 cells
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_extrap --last data/raw/T2_heart/E9.5.h5ad   --out out/heart_extrap_copy_last.h5ad --n-cells 5000

# T3:gata4 — 允许 1,000–7,449 cells
python -m vec_community_baselines.make_baseline --method wt_identity   --board T3:gata4 --wt data/raw/T2_heart/E8.75.h5ad   --out out/t3_wt_identity.h5ad --n-cells 5000
```

这些 baseline 用来确认整个提交流程能跑通，不是竞争性方法。

## 6. 上传前验证

例如：

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

请检查：board、gene panel/顺序、cell 数量、有限且非负的表达值、T2/T3 的 `spatial_3D`，以及工具无法完全判断的 log normalization。

## 7. 用 pseudo split 做本地评分

T2 heart 示例：

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

它适合比较你自己的多个方法，但**不能**当成隐藏 leaderboard 分数预测器。

## 8. 上传

1. 打开 https://virtualembryo.ai/challenge/account/submissions
2. 选对 board。
3. 上传对应的 `.h5ad`。
4. 如果 validation 报错，先修复。
5. 查看总分和各 metric。

格式 validation 被拒绝不会消耗 scored attempt。当前 P3 规则是整个 final phase 每个 board 只有 **2 次 official submission**。

## 9. Agent Team 证据

Human Team 可以跳过本节。

Agent Team 在评分前目前至少要附上两类证据；要获得奖项资格，规则要求 **trajectory、prompts 和 harness**。

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

真正跑 Agent 前请重新阅读官网 Rules。证据打包工具并不等于官方认证。

## 10. 常见第一次提交错误

- T1 只放了 500 genes，而不是 32,285。
- embryo T2 放了 500 genes，但当前 validation board 实际是 498。
- genes 对，但顺序错。
- 提交 raw counts 或中心化/z-score 后出现负值。
- T2/T3 缺少 `obsm["spatial_3D"]`。
- cell 数超出 board 范围。
- 把 pseudo split 排名当成隐藏测试排名。
- 使用规则禁止的 held-out stage / genotype 外部数据。
- Agent Team 证据不完整。

## 11. Final phase

当前时间表中 P3 从 **2026-10-20** 开始。validation 答案会变成训练数据，排名切到 hidden test board；当前规则规定每个 board 整个 P3 只有两次 official submission，并且不能撤回。

进入 P3 当天请重新检查 Rules 和 Data。

官方来源：
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
