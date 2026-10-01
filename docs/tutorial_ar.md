# من الصفر إلى أول مشاركة في VEC — العربية

**آخر تحقق تقني: 2026-09-30.**  
إذا اختلف هذا الدليل عن الموقع الرسمي، فالموقع الرسمي هو المرجع.

## 1. المتطلبات

للتسجيل والتنزيل والرفع:
- حساب في Virtual Embryo Challenge؛
- فريق مسجل إذا كنت ستقدم نتائج؛
- مساحة تخزين كافية لملفات `.h5ad`.

لتثبيت أدوات المجتمع المستخدمة هنا:

```bash
git clone https://github.com/xxx12e/vec-community-kit.git
cd vec-community-kit
git checkout 13ad9baae8f85a8dd121e972c3a87cda8678ec90

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[test]"
```

وللتقييم المحلي على pseudo-split:

```bash
pip install "git+https://github.com/aristoteleo/veckit.git@46d41e63f42a9aab815db20b742feeccd249cb17"
```

## 2. التسجيل وتنزيل البيانات

1. افتح https://virtualembryo.ai/challenge
2. سجل الدخول وأنشئ/سجل فريقك.
3. افتح https://virtualembryo.ai/challenge/data
4. نزّل بيانات التدريب المنشورة.
5. احتفظ بالملفات الأصلية دون تعديل.

## 3. لوحات التحقق الخمس الحالية

| Board | الهدف | الجينات | عدد الخلايا المسموح | إحداثيات 3D | Floor |
|---|---|---:|---:|---|---|
| `T1:val` | E10.5 | 32,285 | 1,000–5,118 | لا | `copy_last` |
| `T2:embryo:val_interp` | E7.5 | 498 | 583–5,000 | نعم | `copy_last` |
| `T2:heart:val_extrap` | E10.5 | 500 | 1,000–25,179 | نعم | `copy_last` |
| `T2:heart:val_interp` | E8.5 | 500 | 1,000–17,616 | نعم | `copy_last` |
| `T3:gata4` | Gata4 KO @ E8.75 | 500 | 1,000–7,449 | نعم | `wt_identity` |

قواعد مهمة:
- كل مشاركة ملف AnnData واحد من نوع `.h5ad`؛
- `.X` يجب أن يكون cells × genes، بقيم finite وغير سالبة ومطبّعة لوغاريتميًا مسبقًا؛
- `var_names` يجب أن يطابق قائمة الجينات وترتيبها للـ board؛
- T2/T3 يتطلبان `obsm["spatial_3D"]` بقيم finite؛
- `obs["celltype"]` في الملف المرسل يتم تجاهله؛
- الحد الأقصى لحجم الملف 1200 MB.

قد تمر raw counts من فحص البنية ولكن تحصل على score خاطئ.

## 4. تنظيم الملفات الذي تستخدمه الأدوات

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

إذا كان اسم الملف الذي نزلته مختلفًا، استخدم اسمه الفعلي في الأوامر.

## 5. إنشاء baseline لكل board

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

هذه baseline لا تهدف للمنافسة؛ هدفها التأكد من أن pipeline يعمل كاملًا.

## 6. التحقق قبل الرفع

```bash
python -m vec_submit_check   --board T2:heart:val_interp   out/heart_interp_copy_last.h5ad
```

تحقق من board، panel وترتيب الجينات، عدد الخلايا، القيم finite/non-negative، `spatial_3D` وlog-normalisation.

## 7. تقييم محلي باستخدام pseudo-split

```bash
python -m vec_local_score   --task T2   --setting heart   --pred out/heart_interp_copy_last.h5ad   --target data/raw/T2_heart/E8.75.h5ad   --reference data/raw/T2_heart/E8.25_late.h5ad
```

استخدمه لمقارنة طرقك على نفس pseudo-problem، وليس للتنبؤ بترتيب hidden leaderboard.

## 8. الرفع

1. افتح https://virtualembryo.ai/challenge/account/submissions
2. اختر الـ board الصحيح.
3. ارفع ملف `.h5ad`.
4. أصلح أي validation error.
5. راجع score وتفاصيل metrics.

فشل format validation لا يستهلك scored attempt. قواعد P3 الحالية تسمح فقط بـ **محاولتين رسميتين لكل board طوال المرحلة**.

## 9. Agent Team

يمكن لـ Human Team تجاوز هذا القسم.

Agent Team يحتاج حاليًا إلى نوعين على الأقل من evidence قبل التقييم؛ ولأهلية الجوائز تطلب القواعد trajectory وprompts وharness.

```bash
python -m pytest tests/test_evidence.py -q

python -m vec_agent_evidence lock   --task T3   --prompt vec_agent_evidence/example_prompt.md   --model <model-id>   --data-root ./data   --hours 8

python -m vec_agent_evidence run   --task T2   --boards T2:heart:val_extrap   --prompt my_prompt.md   --model <model-id>   --data-root ./data   --hours 10   --max-turns 600

python -m vec_agent_evidence package   --run-dir runs/<run_id>   --team-uploaded-mb 0
```

اقرأ Rules الحالية مرة أخرى قبل تشغيل Agent حقيقي.

## 10. أخطاء شائعة

- استخدام 500 genes في T1 بدل 32,285.
- استخدام 500 genes في embryo T2 بدل 498.
- الجينات صحيحة لكن ترتيبها خاطئ.
- raw counts أو قيم سالبة بعد z-score.
- غياب `obsm["spatial_3D"]` في T2/T3.
- عدد الخلايا خارج حدود board.
- اعتبار pseudo-split تنبؤًا بالhidden ranking.
- استخدام بيانات خارجية ممنوعة من held-out stage/genotype.
- نقص evidence في Agent Team.

## 11. المرحلة النهائية

حسب الجدول الحالي يبدأ P3 في **2026-10-20**. تصبح إجابات validation متاحة للتدريب وينتقل الترتيب إلى hidden test boards. راجع Rules وData مرة أخرى عند بدء P3.

المصادر:
- https://virtualembryo.ai/challenge/data
- https://virtualembryo.ai/challenge/evaluation
- https://virtualembryo.ai/challenge/rules
- https://virtualembryo.ai/challenge/tasks
