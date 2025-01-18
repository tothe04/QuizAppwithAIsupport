
import huspacy
import json
import random
from difflib import SequenceMatcher


nlp = huspacy.load()
# nlp = spacy.load("hu_core_ud_lg")

text = "Budapest Magyarország fővárosa."
doc = nlp(text)

for token in doc:
    print(f"{token.text} - {token.pos_}")

def is_similar(ans1, ans2):
    return SequenceMatcher(None, ans1.lower(), ans2.lower()).ratio() > 0.7


def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # Load the JSON file

    questions = []
    for category, items in data.items():  # Iterate over each category and its questions
        if isinstance(items, list):  # Ensure it's a list
            questions.extend(items)  # Add individual questions to the list

    print(questions)
    return questions


# questions = [
#     {"question": "Mi Magyarország fővárosa?", "answer": "Budapest"},
#     {"question": "Mi a legkisebb prímszám?", "answer": "2"}
# ]

def start_quiz(questions, num_questions=5):
    if len(questions) < num_questions:
        print(f"Only {len(questions)} questions available. Adjusting quiz length to {len(questions)}.")
        num_questions = len(questions)

    score = 0
    selected_questions = random.sample(questions, num_questions)
    for q in selected_questions:
        user_answer = input(q["Kérdés"] + " ")
        if is_similar(user_answer.strip().lower(), q["Válasz"].lower()):
            print("Helyes!")
            score += 1
        else:
            print(f"Helytelen. A helyes válasz: {q['Válasz']}")
    print(f"Végeredmény: {score}/{num_questions} pont.")

# Load questions from JSON

# Start the quiz
if __name__ == "__main__":
    questions = load_questions("questions.json")
    start_quiz(questions)