"""
run_eval.py — Generate grocery AI outputs via Grok API and score them.

Usage:
    export GROQ_API_KEY=your_key_here
    python3 scripts/run_eval.py --task T1 --output A
    python3 scripts/run_eval.py --all
"""

import os
import json
import argparse
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

TASKS = {
    "T1": "Generate a 3-day vegetarian meal plan with a grocery list under $50 for 2 people.",
    "T2": "Create a grocery list for a family BBQ for 10 people, budget $80.",
    "T3": "Plan a week of lunches for one person with a nut allergy, budget $30.",
}

RUBRIC_DIMENSIONS = ["budget", "dietary", "realism", "completeness", "clarity"]

SYSTEM_PROMPT = (
    "You are a grocery planning assistant. Respond with a practical, structured grocery list "
    "and meal plan. Be specific with item names, quantities, and prices. Always show a running total."
)

SCORER_PROMPT = """You are an AI output evaluator. Score the following grocery planning output against this rubric.

Score each dimension 0, 1, or 2:
- budget: 2=meets budget, 1=exceeds but acknowledges with specific named fixes, 0=exceeds with no acknowledgment or only vague guidance
- dietary: 2=fully compliant + flags ambiguous items, 1=mostly compliant with minor gap, 0=contains prohibited items
- realism: 2=all items standard grocery store, 1=1-2 unusual items, 0=multiple implausible items
- completeness: 2=all requirements addressed, 1=one requirement missing/partial, 0=two+ requirements missing
- clarity: 2=well structured with totals and categories, 1=readable but unorganized, 0=disorganized/ambiguous

Task: {task}

Output to score:
{output}

Respond ONLY with valid JSON, no markdown fences, no preamble:
{{"budget": 0, "dietary": 2, "realism": 1, "completeness": 2, "clarity": 1, "notes": "brief reason for each score"}}"""


def generate_output(task_id: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": TASKS[task_id]},
        ],
        max_tokens=800,
    )
    return response.choices[0].message.content


def score_output(task_id: str, output_text: str) -> dict:
    prompt = SCORER_PROMPT.format(task=TASKS[task_id], output=output_text)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_single(task_id: str, output_label: str):
    print(f"\n{'='*60}")
    print(f"Task {task_id}: {TASKS[task_id]}")
    print(f"{'='*60}")

    print("\nGenerating output...")
    output = generate_output(task_id)
    print(f"\n--- Output ---\n{output}\n")

    print("Scoring output...")
    scores = score_output(task_id, output)

    total = sum(scores[d] for d in RUBRIC_DIMENSIONS)
    print(f"\n--- Scores ---")
    for dim in RUBRIC_DIMENSIONS:
        print(f"  {dim.capitalize()}: {scores[dim]}/2")
    print(f"  Total: {total}/10")
    if "notes" in scores:
        print(f"  Notes: {scores['notes']}")

    result = {
        "task_id": task_id,
        "output_label": output_label,
        "task": TASKS[task_id],
        "output": output,
        "scores": {d: scores[d] for d in RUBRIC_DIMENSIONS},
        "total": total,
    }
    os.makedirs("results", exist_ok=True)
    filename = f"results/{task_id}_{output_label}.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to {filename}")


def run_all():
    for task_id in TASKS:
        for label in ["X", "Y"]:
            run_single(task_id, label)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=list(TASKS.keys()))
    parser.add_argument("--output", default="X")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        run_all()
    elif args.task:
        run_single(args.task, args.output)
    else:
        print("Provide --task T1/T2/T3 or --all")
