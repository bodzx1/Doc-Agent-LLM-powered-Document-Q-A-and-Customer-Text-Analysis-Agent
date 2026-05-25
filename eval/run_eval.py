"""
Day 3 — Evaluation harness.

Loops through eval_set.json, runs each question through the agent,
and scores: correct tool called? expected keywords present in answer?

Run with:  python eval/run_eval.py
"""

import json
from dotenv import load_dotenv
load_dotenv()
import docagent.agent as agent
from pathlib import Path
def run_eval(test_agent: agent):
    eval_set = json.loads(Path("eval/eval_set.json").read_text())
    correct_answer = 0
    for i, item in enumerate(eval_set):
        question = item["question"]
        expected_keywords = item["expected_keywords"]

        print(f"\nQuestion {i+1}: {question}")
        answer = test_agent.invoke({"input": question,"chat_history": []}) ##for evaluation, we can pass an empty chat history since we want to test the agent's ability to answer each question independently without relying on previous conversation context. This allows us to evaluate the agent's performance on each question in isolation.
        print(f"Answer: {answer['output']}")
        # Check if expected keywords are present in the answer
        if all(keyword.lower() in answer['output'].lower() for keyword in expected_keywords):
            correct_answer += 1
            print("Correct answer.")
        else:
            print("Incorrect answer.")
        if i==1:
            break
    total_questions = len(eval_set)
    print(f"\nScore: {correct_answer}/{len(eval_set)}")

    

if __name__ == "__main__":
    test_agent=agent.build_agent()
    run_eval(test_agent)
