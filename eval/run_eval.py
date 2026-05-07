"""
Day 3 — Evaluation harness.

Loops through eval_set.json, runs each question through the agent,
and scores: correct tool called? expected keywords present in answer?

Run with:  python eval/run_eval.py
"""

import json
from pathlib import Path

# TODO Day 3: implement eval loop


def run_eval():
    eval_set = json.loads(Path("eval/eval_set.json").read_text())
    raise NotImplementedError


if __name__ == "__main__":
    run_eval()
