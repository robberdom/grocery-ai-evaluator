# Rubric v1 — Grocery AI Output Evaluation

Each output is scored independently across 5 dimensions. Scores are integers: 0, 1, or 2.
Total possible score: 10. Dimensions are unweighted in v1.

---

## Dimension 1: Budget Compliance

**What it measures:** Does the output respect the stated budget constraint?

| Score | Definition |
|---|---|
| 2 | Meets budget exactly, or variance ≤5% with no note needed |
| 1 | Exceeds budget (any amount) AND output explicitly acknowledges this AND proposes specific, named corrective adjustments |
| 0 | Exceeds budget with no acknowledgment; OR exceeds budget with only vague guidance ("trim some items") that is not actionable |

**Note:** A score of 1 requires both acknowledgment AND specificity. "This might be over budget" alone is not sufficient for a 1.

---

## Dimension 2: Dietary Adherence

**What it measures:** Are all stated dietary restrictions fully honored?

| Score | Definition |
|---|---|
| 2 | Fully compliant; any ambiguous items (e.g. "hummus" near nut-allergy task) are explicitly flagged with a note |
| 1 | Mostly compliant but includes 1 ambiguous item without flagging, OR minor omission with no safety implication |
| 0 | Contains 1+ prohibited items; restriction is ignored or misunderstood |

**Note:** For allergy-related tasks, a score of 0 is mandatory if any prohibited ingredient appears, regardless of other output quality.

---

## Dimension 3: Realism & Practicality

**What it measures:** Are the items, quantities, and plans plausible for a real shopper at a standard grocery store?

| Score | Definition |
|---|---|
| 2 | All items are standard grocery store products; quantities match realistic consumption for the stated number of people and days |
| 1 | Mostly realistic; 1–2 items are unusual, overpriced, or available only at specialty stores, but don't break the plan |
| 0 | Multiple implausible items, specialty-only ingredients presented as standard, or quantities that make no practical sense |

---

## Dimension 4: Task Completeness

**What it measures:** Does the output address every stated requirement in the task prompt?

| Score | Definition |
|---|---|
| 2 | All requirements addressed clearly (budget, dietary constraint, number of people, number of days, meal type if specified) |
| 1 | One requirement partially addressed or missing; the gap doesn't invalidate the output |
| 0 | Two or more requirements missing; output cannot function as a response to the full task |

---

## Dimension 5: Clarity & Usability

**What it measures:** Is the output easy to act on as an actual shopping and meal guide?

| Score | Definition |
|---|---|
| 2 | Well-structured with logical groupings (by category or day), running totals or final total, and no ambiguity in quantities |
| 1 | Readable but lacks organization (no categories, no total, or inconsistent formatting) |
| 0 | Disorganized, ambiguous quantities, or requires significant effort to interpret before use |

---

## Scoring Notes

- Score each dimension independently before calculating total
- Do not let overall impression bias individual dimension scores (halo effect)
- When in doubt between two scores, default to the lower score and document your reasoning
- All scoring decisions should be defensible by pointing to a specific rubric criterion
