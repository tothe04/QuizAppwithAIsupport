import tkinter as tk
from tkinter import ttk
import random
import threading
from quiz_base import load_questions, is_answer_correct, generate_feedback  # Import AI logic

# Load questions
file_path = "questions.json"
all_questions = load_questions(file_path)

current_question = 0
score = 0
selected_questions = []
responses = []  # Store user responses for AI feedback

# Styling constants
FONT_LARGE = ("Arial", 14)
FONT_MEDIUM = ("Arial", 12)
PAD = 10

def start_quiz():
    """Initializes the quiz with random questions."""
    global selected_questions, current_question, score, responses

    # Reset quiz state
    current_question = 0
    score = 0
    responses = []
    selected_questions = random.sample(all_questions, min(5, len(all_questions)))

    # Display first question
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

def check_answer():
    """Runs AI validation in a separate thread to prevent UI freezing."""
    threading.Thread(target=validate_answer, daemon=True).start()

def validate_answer():
    """Validates the user's answer using AI and updates the UI."""
    global current_question, score

    user_answer = entry.get().strip()
    correct_answer = selected_questions[current_question]["Válasz"]

    label_result.config(text="Ellenőrzés folyamatban...", foreground="black")  # Show loading text

    # AI-based validation
    is_correct = is_answer_correct(user_answer, correct_answer)

    responses.append({
        "question": selected_questions[current_question]["Kérdés"],
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "correct": is_correct
    })

    if is_correct:
        label_result.config(text="Helyes!", foreground="green")
        score += 1
    else:
        label_result.config(text=f"Helytelen! Helyes válasz: {correct_answer}", foreground="red")

    # Move to the next question or end quiz
    current_question += 1
    if current_question < len(selected_questions):
        root.after(1000, update_question)  # Show next question after 1 sec
        root.after(1000, lambda: entry.delete(0, tk.END))  # Clear input
    else:
        threading.Thread(target=end_quiz, daemon=True).start()  # Generate feedback in a separate thread

def end_quiz():
    """Ends the quiz and generates AI feedback."""
    label_question.config(text=f"Kvíz vége! Eredmény: {score}/{len(selected_questions)}")
    entry.pack_forget()
    button_next.pack_forget()

    # Display feedback loading message
    label_feedback.config(text="AI visszajelzés generálása...", foreground="black")

    # Generate AI feedback
    feedback = generate_feedback(responses)

    # Update feedback label
    label_feedback.config(text=f"📢 AI visszajelzés:\n{feedback}", foreground="blue")

    # Enable the restart button after feedback loads
    button_restart.config(state=tk.NORMAL)
    button_restart.pack(pady=PAD)

if __name__ == "__main__":
    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Kvíz Alkalmazás")
    root.geometry("500x400")

    frame_main = ttk.Frame(root, padding=PAD)
    frame_main.pack(fill=tk.BOTH, expand=True)

    label_question = ttk.Label(frame_main, text="", font=FONT_LARGE, wraplength=400, anchor="center")
    label_question.pack(pady=PAD)

    entry = ttk.Entry(frame_main, font=FONT_MEDIUM, justify="center")
    entry.pack(pady=PAD)

    button_next = ttk.Button(frame_main, text="Tovább", command=check_answer)  # Now runs AI check
    button_next.pack(pady=PAD)

    label_result = ttk.Label(frame_main, text="", font=FONT_MEDIUM, wraplength=400, anchor="center")
    label_result.pack(pady=PAD)

    label_feedback = ttk.Label(frame_main, text="", font=FONT_MEDIUM, wraplength=400, anchor="center")
    label_feedback.pack(pady=PAD)

    button_restart = tk.Button(root, text="Újraindítás", command=start_quiz)
    button_restart.pack(pady=PAD)
    button_restart.pack_forget()

    # Start the quiz
    start_quiz()

    root.mainloop()
