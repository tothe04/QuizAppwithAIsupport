import tkinter as tk
from tkinter import ttk
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

# Styling constants
FONT_LARGE = ("Arial", 14)
FONT_MEDIUM = ("Arial", 12)
FONT_SMALL = ("Arial", 10)
PAD = 10

def start_quiz():
    """Initializes the quiz with 5 random questions."""
    global selected_questions, current_question, score

    # Reset quiz state
    current_question = 0
    score = 0

    # Select 5 random questions
    selected_questions = random.sample(all_questions, min(5, len(all_questions)))

    # Update the first question
    #label_question.config(text=selected_questions[current_question]["Kérdés"])
    update_question()
    label_result.config(text="")
    entry.delete(0, tk.END)

    # Show input and button
    entry.pack(pady=PAD)
    button_next.pack(pady=PAD)
    button_restart.pack_forget()


def update_question():
    """Updates the question label."""
    question = selected_questions[current_question]["Kérdés"]
    label_question.config(text=f"Kérdés {current_question + 1}/{len(selected_questions)}:\n{question}")



def next_question():
    """Scoring and stepping to the next question."""
    global current_question, score

    # Get user answer
    user_answer = entry.get()

    # Tokenize the user answer using huspacy
    user_doc = nlp(user_answer)

    # Tokenize the correct answer (also using huspacy)
    correct_answer = selected_questions[current_question]["Válasz"]
    correct_doc = nlp(correct_answer)

    # Print the tokens
    user_tokens = [token.text.lower() for token in user_doc]
    correct_tokens = [token.text.lower() for token in correct_doc]
    print("User's Answer Tokenized:", user_tokens)
    print("Correct Answer Tokenized:", correct_tokens)

    # Compare tokenized user answer with the tokenized correct answer
    common_tokens = set(user_tokens).intersection(set(correct_tokens))
    similarity_ratio = len(common_tokens) / len(correct_tokens) if correct_tokens else 0

    print("Similarity Ratio:", similarity_ratio)

    # Define a threshold for correct answer
    if similarity_ratio > 0.5:
        label_result.config(text="Helyes!", style="Success.TLabel")
        score += 1
    else:
        label_result.config(text=f"Helytelen! Helyes válasz: {correct_answer}", style="Error.TLabel")

    # Move to the next question or end the quiz
    current_question += 1
    if current_question < len(selected_questions):
        update_question()
        #label_question.config(text=selected_questions[current_question]["Kérdés"])
        entry.delete(0, tk.END)
    else:
        label_question.config(
            text=f"Kvíz vége! Eredmény: {score}/{len(selected_questions)}"
        )
        entry.pack_forget()
        button_next.pack_forget()
        button_restart.pack(pady=PAD)


if __name__ == "__main__":

    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Kvíz Alkalmazás")
    root.geometry("400x300")

    style = ttk.Style()
    style.configure("ResultLabel.TLabel", font=("Arial", 12))


    frame_main = ttk.Frame(root, padding=PAD)
    frame_main.pack(fill=tk.BOTH, expand=True)

    label_question = ttk.Label(frame_main, text="", font=FONT_LARGE, wraplength=280, anchor="center")
    label_question.pack(pady=PAD)

    entry = ttk.Entry(frame_main, font=FONT_MEDIUM, justify="center")
    entry.pack(pady=PAD)

    button_next = ttk.Button(frame_main, text="Tovább", command=next_question)
    button_next.pack(pady=PAD)

    label_result = ttk.Label(frame_main, text="", font=FONT_MEDIUM, wraplength=280, anchor="center")
    label_result.pack(pady=PAD)

    button_restart = tk.Button(root, text="Újraindítás", command=start_quiz)
    button_restart.pack(pady=PAD)
    button_restart.pack_forget()

    # Start the quiz
    start_quiz()

    root.mainloop()
