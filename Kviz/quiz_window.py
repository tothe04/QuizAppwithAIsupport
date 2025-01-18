import tkinter as tk
import random
import huspacy
from quiz_base import load_questions

# Load questions from JSON file
file_path = "questions.json"
all_questions = load_questions(file_path)

current_question = 0
score = 0
selected_questions = []

# Initialize huspacy for Hungarian tokenization
nlp = huspacy.load()

def start_quiz():
    """Initializes the quiz with 5 random questions."""
    global selected_questions, current_question, score

    # Reset quiz state
    current_question = 0
    score = 0

    # Select 5 random questions
    selected_questions = random.sample(all_questions, min(5, len(all_questions)))

    # Update the first question
    label_question.config(text=selected_questions[current_question]["Kérdés"])
    label_result.config(text="")
    entry.delete(0, tk.END)


def next_question():
    """Handles the next question logic in the quiz."""
    global current_question, score

    # Get user answer
    user_answer = entry.get()

    # Tokenize the user answer using huspacy
    user_doc = nlp(user_answer)

    # Tokenize the correct answer (also using huspacy)
    correct_answer = selected_questions[current_question]["Válasz"]
    correct_doc = nlp(correct_answer)

    # Print the tokens (for debugging or processing purposes)
    user_tokens = [token.text.lower() for token in user_doc]
    correct_tokens = [token.text.lower() for token in correct_doc]
    print("User's Answer Tokenized:", user_tokens)
    print("Correct Answer Tokenized:", correct_tokens)

    # Compare tokenized user answer with the tokenized correct answer
    common_tokens = set(user_tokens).intersection(set(correct_tokens))
    similarity_ratio = len(common_tokens) / len(correct_tokens) if correct_tokens else 0

    # Print the similarity ratio (for debugging)
    print("Similarity Ratio:", similarity_ratio)

    # Define a threshold for correct answer (e.g., 0.7 similarity)
    if similarity_ratio > 0.5:
        label_result.config(text="Helyes!", fg="green")
        score += 1
    else:
        label_result.config(text=f"Helytelen! Helyes válasz: {correct_answer}", fg="red")

    # Move to the next question or end the quiz
    current_question += 1
    if current_question < len(selected_questions):
        label_question.config(text=selected_questions[current_question]["Kérdés"])
        entry.delete(0, tk.END)
    else:
        label_question.config(text=f"Kvíz vége! Eredmény: {score}/{len(selected_questions)}")
        entry.pack_forget()
        button.pack_forget()
        restart_button.pack(pady=10)


# Tkinter GUI setup
root = tk.Tk()
root.title("Kvíz Alkalmazás")

label_question = tk.Label(root, text="", font=("Arial", 14))
label_question.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

button = tk.Button(root, text="Tovább", command=next_question)
button.pack(pady=10)

label_result = tk.Label(root, text="")
label_result.pack(pady=10)

restart_button = tk.Button(root, text="Újraindítás", command=start_quiz)
restart_button.pack(pady=10)
restart_button.pack_forget()

# Start the quiz
start_quiz()

root.mainloop()
