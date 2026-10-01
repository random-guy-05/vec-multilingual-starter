# Do zero à primeira submissão no VEC — Português

**Última verificação técnica: 2026-09-30.**  
Se houver diferença entre este guia e o site oficial, siga sempre o site oficial.

## 1. Pré-requisitos

Para registro, download e upload:
- conta no Virtual Embryo Challenge;
- equipe registrada para enviar resultados;
- espaço em disco para os arquivos `.h5ad`.

Instale as ferramentas comunitárias usadas nos exemplos:

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

Para pontuação local em pseudo-splits:

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. Registrar e baixar os dados

1. Abra https://virtualembryo.ai/challenge
2. Faça login e registre sua equipe.
3. Abra https://virtualembryo.ai/challenge/data
4. Baixe os dados de treinamento liberados.
5. Mantenha os arquivos originais sem alterações.

## 3. Os cinco boards de validação atuais

| Board | Alvo | Genes | Células permitidas | Coordenadas | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | não | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | sim | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | sim | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | sim | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | sim | `wt_identity` |

Regras principais:
- uma submissão é um arquivo AnnData `.h5ad`;
- `.X` deve ser cells × genes, finito, não negativo e já log-normalizado;
- `var_names` precisa corresponder ao painel e à ordem do board;
- T2/T3 exigem `obsm["spatial_3D"]` finito;
- `obs["celltype"]` enviado é ignorado;
- tamanho máximo: 1200 MB.

Counts brutos podem passar na validação estrutural e ainda assim receber uma pontuação incorreta.

## 4. Layout de dados usado pelas ferramentas

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

Se o seu download tiver outro nome, use o nome real no comando.

## 5. Criar um baseline para cada board

```bash
mkdir -p out

# T1:val — 1,000–5,118 células
python -m vec_community_baselines.make_baseline --method copy_last   --board T1:val --last data/raw/T1/E9.5_RNA.h5ad   --out out/t1_copy_last.h5ad --n-cells 5000

# T2:embryo:val_interp — 583–5,000 células
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:embryo:val_interp --last data/raw/T2_embryo/E8.0.h5ad   --out out/embryo_copy_last.h5ad --n-cells 5000

# T2:heart:val_interp — 1,000–17,616 células
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_interp --last data/raw/T2_heart/E8.25_late.h5ad   --out out/heart_interp_copy_last.h5ad --n-cells 5000

# T2:heart:val_extrap — 1,000–25,179 células
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_extrap --last data/raw/T2_heart/E9.5.h5ad   --out out/heart_extrap_copy_last.h5ad --n-cells 5000

# T3:gata4 — 1,000–7,449 células
python -m vec_community_baselines.make_baseline --method wt_identity   --board T3:gata4 --wt data/raw/T2_heart/E8.75.h5ad   --out out/t3_wt_identity.h5ad --n-cells 5000
```

Esses baselines servem para testar o fluxo inteiro, não como métodos competitivos.

## 6. Validar antes do upload

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

Confira board, painel e ordem dos genes, contagem de células, valores finitos/não negativos, `spatial_3D` e log-normalização.

## 7. Pontuar em um pseudo-split

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

Use para comparar seus próprios métodos no mesmo pseudo-problema. Não use como previsão do ranking oculto.

## 8. Upload

1. Abra https://virtualembryo.ai/challenge/account/submissions
2. Escolha o board correto.
3. Envie o `.h5ad`.
4. Corrija qualquer erro de validação.
5. Examine a pontuação e as métricas.

Falhar na validação de formato não consome tentativa pontuada. Nas regras atuais de P3 existem apenas **duas submissões oficiais por board em toda a fase**.

## 9. Agent Team

Human Team pode pular esta seção.

Agent Team precisa anexar pelo menos dois tipos de evidência antes da pontuação; para elegibilidade a prêmio, as regras pedem trajetória, prompts e harness.

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

Releia as Rules antes de uma execução real.

## 10. Erros comuns

- T1 com 500 genes em vez de 32,285.
- T2 embryo com 500 em vez de 498 genes.
- Genes corretos na ordem errada.
- Counts brutos ou valores negativos após z-score.
- Falta de `obsm["spatial_3D"]` em T2/T3.
- Contagem de células fora do limite.
- Tratar pseudo-split como previsão do ranking oculto.
- Usar dados externos de estágio/genótipo proibidos.
- Evidência incompleta no Agent Team.

## 11. Fase final

P3 está programada para começar em **2026-10-20**. As respostas de validação passam a poder ser usadas no treinamento e o ranking muda para testes ocultos. Verifique novamente Rules e Data ao entrar em P3.

Fontes:
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
