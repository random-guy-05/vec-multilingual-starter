# De zéro à votre première soumission VEC — Français

**Dernière vérification technique : 2026-09-30.**  
En cas de différence avec le site officiel, le site officiel fait foi.

## 1. Prérequis

Pour l'inscription, le téléchargement et l'envoi :
- un compte Virtual Embryo Challenge ;
- une équipe enregistrée pour soumettre ;
- assez d'espace disque pour les fichiers `.h5ad`.

Installer les outils communautaires utilisés ici :

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

Pour le scoring local sur pseudo-split :

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. Inscription et téléchargement

1. Ouvrez https://virtualembryo.ai/challenge
2. Connectez-vous et enregistrez votre équipe.
3. Ouvrez https://virtualembryo.ai/challenge/data
4. Téléchargez les données d'entraînement publiées.
5. Conservez les fichiers originaux inchangés.

## 3. Les cinq boards de validation actuels

| Board | Cible | Gènes | Cellules autorisées | Coordonnées | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | non | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | oui | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | oui | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | oui | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | oui | `wt_identity` |

Règles essentielles :
- une soumission = un fichier AnnData `.h5ad` ;
- `.X` doit être cells × genes, fini, non négatif et déjà log-normalisé ;
- `var_names` doit correspondre exactement au panel et à son ordre ;
- T2/T3 nécessitent `obsm["spatial_3D"]` fini ;
- `obs["celltype"]` soumis est ignoré ;
- taille maximale : 1200 MB.

Des counts bruts peuvent passer les contrôles structurels mais être scorés de façon incorrecte.

## 4. Organisation des données

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

Si vos fichiers portent d'autres noms, utilisez les vrais noms.

## 5. Construire un baseline par board

```bash
mkdir -p out

# T1:val — 1,000–5,118 cellules
python -m vec_community_baselines.make_baseline --method copy_last   --board T1:val --last data/raw/T1/E9.5_RNA.h5ad   --out out/t1_copy_last.h5ad --n-cells 5000

# T2:embryo:val_interp — 583–5,000 cellules
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:embryo:val_interp --last data/raw/T2_embryo/E8.0.h5ad   --out out/embryo_copy_last.h5ad --n-cells 5000

# T2:heart:val_interp — 1,000–17,616 cellules
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_interp --last data/raw/T2_heart/E8.25_late.h5ad   --out out/heart_interp_copy_last.h5ad --n-cells 5000

# T2:heart:val_extrap — 1,000–25,179 cellules
python -m vec_community_baselines.make_baseline --method copy_last   --board T2:heart:val_extrap --last data/raw/T2_heart/E9.5.h5ad   --out out/heart_extrap_copy_last.h5ad --n-cells 5000

# T3:gata4 — 1,000–7,449 cellules
python -m vec_community_baselines.make_baseline --method wt_identity   --board T3:gata4 --wt data/raw/T2_heart/E8.75.h5ad   --out out/t3_wt_identity.h5ad --n-cells 5000
```

Ces baselines testent le pipeline ; ce ne sont pas des méthodes compétitives.

## 6. Valider avant l'envoi

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

Vérifiez le board, le panel/l'ordre des gènes, le nombre de cellules, les valeurs finies/non négatives, `spatial_3D` et la log-normalisation.

## 7. Score local sur pseudo-split

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

Utilisez-le pour comparer vos propres méthodes sur le même pseudo-problème, pas pour prédire le classement caché.

## 8. Envoi

1. Ouvrez https://virtualembryo.ai/challenge/account/submissions
2. Choisissez le bon board.
3. Envoyez le `.h5ad`.
4. Corrigez les erreurs de validation.
5. Consultez score et métriques.

Une validation rejetée ne consomme pas de tentative scorée. En P3, les règles actuelles autorisent seulement **deux soumissions officielles par board pendant toute la phase**.

## 9. Agent Team

Les Human Teams peuvent ignorer cette section.

Pour Agent Team, au moins deux types de preuves sont requis avant scoring ; pour l'éligibilité à un prix, les règles demandent trajectoire, prompts et harness.

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

Relisez les Rules officielles avant un vrai run.

## 10. Erreurs fréquentes

- T1 avec 500 gènes au lieu de 32,285.
- T2 embryo avec 500 gènes au lieu de 498.
- Bons gènes dans le mauvais ordre.
- Counts bruts ou valeurs négatives après z-score.
- `obsm["spatial_3D"]` absent en T2/T3.
- Nombre de cellules hors limites.
- Prendre un pseudo-split pour une prédiction du classement caché.
- Utiliser des données externes interdites de stage/génotype held-out.
- Preuves Agent incomplètes.

## 11. Phase finale

P3 doit actuellement commencer le **2026-10-20**. Les réponses de validation deviennent des données d'entraînement et le classement passe aux tests cachés. Vérifiez à nouveau Rules et Data ce jour-là.

Sources :
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
