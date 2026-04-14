# grocery-ai-evaluator

A rubric design and calibration simulation project for evaluating AI-generated grocery planning outputs.

Built to demonstrate: rubric development, scoring methodology, calibration sessions, inter-rater reliability analysis, and assessment validation as applied to a real AI training domain.

---

## Project Structure

```
grocery-ai-evaluator/
│
├── rubric/
│   └── rubric_v1.md              # 5-dimension scoring rubric with level definitions
│
├── tasks/
│   └── tasks.md                  # 3 evaluation tasks with prompts and constraints
│
├── outputs/
│   ├── T1_outputs.md             # 3 outputs for Task 1 (vegetarian meal plan, $50)
│   ├── T2_outputs.md             # 2 outputs for Task 2 (BBQ for 10, $80)
│   └── T3_outputs.md             # 2 outputs for Task 3 (nut-free lunches, $30)
│
├── scores/
│   └── scoring_sheet.md          # All outputs scored across all dimensions
│
├── calibration/
│   └── calibration_session.md    # Evaluator disagreement, root cause, and resolution
│
├── scripts/
│   └── run_eval.py               # Script to generate new outputs via Grok API
│
└── README.md
```

---

## Rubric Summary

Each output is scored across 5 dimensions (0–2 each). Maximum score: 10.

| Dimension | What It Measures |
|---|---|
| Budget Compliance | Does the output respect the stated budget? |
| Dietary Adherence | Are all dietary restrictions honored? |
| Realism & Practicality | Are items and quantities plausible for a real shopper? |
| Task Completeness | Are all stated requirements addressed? |
| Clarity & Usability | Is the output well-structured and easy to act on? |

---

## Score Summary

| Output | Task | Total /10 | Quality |
|---|---|---|---|
| T1-A | Vegetarian meal plan, $50 | 10/10 | Strong |
| T1-B | Vegetarian meal plan, $50 | 6/10 | Acceptable |
| T1-C | Vegetarian meal plan, $50 | 3/10 | Poor |
| T2-A | BBQ for 10, $80 | 10/10 | Strong |
| T2-B | BBQ for 10, $80 | 7/10 | Acceptable — calibration example |
| T3-A | Nut-free lunches, $30 | 10/10 | Strong |
| T3-B | Nut-free lunches, $30 | 6/10 | Poor (dietary fail) |

---

## Calibration Highlight
Trigger: Budget exceeded by >20% but output acknowledged the violation and suggested fixes.

Output T2-B triggered a scoring disagreement on the Budget dimension:

- Evaluator 1: Score 0 — exceeded budget by 44%
- Evaluator 2: Score 1 — output acknowledged the violation and named specific items to remove

Both evaluators applied the rubric correctly. The rubric was ambiguous. The session resolved this by updating the Budget dimension's level 1 definition to cover acknowledged violations with named corrective guidance — regardless of violation magnitude. 

Full writeup: `calibration/calibration_session.md`

---

## Running the Eval Script

```bash
pip install groq

export GROQ_API_KEY=your_key_here

python scripts/run_eval.py --task T1 --output A
python scripts/run_eval.py --all
```

Results saved as JSON to `/results/`.

---

## Stack

- **Model:** llama-3.3-70b-versatile via Groq API
- **Language:** Python (eval runner), Markdown (rubric + results)
- **Eval approach:** Manual scoring against rubric + simulated calibration session

---

## Open Questions

- Should Dietary Adherence be weighted 2x given safety implications of allergy violations?
- Should mandatory-0 dietary failures be automatic rejections regardless of total score?
- Can rubric scores be validated against real user satisfaction data?
- How does output quality degrade on more complex tasks (5-day plans, multiple dietary restrictions combined)?
- Would a v2 rubric with a dedicated "Safety Flagging" dimension improve detection of allergy failures?
