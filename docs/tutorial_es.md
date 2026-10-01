# De cero a tu primera entrega de VEC — Español

**Última verificación técnica: 2026-09-30.**  
Si esta guía y la web oficial difieren, manda siempre la web oficial.

## 1. Qué necesitas

Para registrarte, descargar y subir:
- una cuenta de Virtual Embryo Challenge;
- un equipo registrado para enviar resultados;
- espacio suficiente para los archivos `.h5ad`.

Para los comandos auxiliares:

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

Para puntuar localmente con pseudo-splits:

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. Registro y descarga

1. Abre https://virtualembryo.ai/challenge
2. Inicia sesión y registra tu equipo.
3. Abre https://virtualembryo.ai/challenge/data
4. Descarga los datos de entrenamiento publicados.
5. Conserva los archivos originales sin modificar.

## 3. Los cinco boards de validación actuales

| Board | Objetivo | Genes | Células permitidas | Coordenadas | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | no | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | sí | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | sí | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | sí | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | sí | `wt_identity` |

Reglas clave:
- una entrega = un archivo AnnData `.h5ad`;
- `.X` debe ser células × genes, finito, no negativo y ya log-normalizado;
- `var_names` debe coincidir con el panel y el orden del board;
- T2/T3 requieren `obsm["spatial_3D"]` finito;
- `obs["celltype"]` enviado se ignora;
- máximo 1200 MB por archivo.

Los counts crudos pueden pasar validación estructural y aun así puntuarse mal.

## 4. Estructura de datos usada por las herramientas

El tutorial upstream usa rutas como:

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

Si tus nombres son distintos, usa los nombres reales.

## 5. Construye un baseline por board

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

Son pruebas del pipeline, no métodos competitivos.

## 6. Valida antes de subir

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

Comprueba panel/orden de genes, número de células, valores finitos/no negativos, `spatial_3D` y log-normalización.

## 7. Puntuación local con pseudo-split

Ejemplo T2 heart:

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

Úsalo para comparar tus propios métodos en el mismo pseudo-problema. No es una predicción del leaderboard oculto.

## 8. Subida

1. Ve a https://virtualembryo.ai/challenge/account/submissions
2. Selecciona el board exacto.
3. Sube el `.h5ad`.
4. Corrige cualquier error de validación.
5. Revisa score y métricas.

Una validación rechazada no consume un intento puntuado. En P3 las reglas actuales permiten solo **dos entregas oficiales por board en toda la fase**.

## 9. Agent Team

Human Team puede saltar esta sección.

Para Agent Team, las reglas actuales exigen al menos dos tipos de evidencia antes de puntuar; para optar a premio se requieren trayectoria, prompts y harness.

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

Lee las reglas oficiales antes de una ejecución real.

## 10. Errores frecuentes

- T1 con 500 genes en vez de 32,285.
- T2 embryo con 500 genes cuando este board usa 498.
- Genes correctos en orden incorrecto.
- Counts crudos o datos z-scoreados.
- Falta `obsm["spatial_3D"]` en T2/T3.
- Número de células fuera del rango.
- Confundir pseudo-split con predicción del score oculto.
- Usar datos externos de etapas/genotipos prohibidos.
- Evidencia incompleta en Agent Team.

## 11. Fase final

P3 está programada actualmente para **2026-10-20**. Las respuestas de validación pasan a entrenamiento y el ranking cambia a test oculto. Comprueba de nuevo Rules y Data ese día.

Fuentes oficiales:
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
