import tkinter as tk
import customtkinter as ctk
import random
import threading
from dotenv import load_dotenv, find_dotenv

from quiz_base import load_questions, is_answer_correct, generate_feedback  # Import AI logic

_ = load_dotenv(find_dotenv())

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# Load questions
file_path = "questions.json"
all_questions = load_questions(file_path)

current_question = 0
score = 0
selected_questions = []
responses = []

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
    label_result.grid_remove()
    tk_textbox.delete("1.0", tk.END)

    # Show input and button
    tk_textbox.grid(row=1, column=0, pady=PAD)
    button_check.grid(row=0, column=0, pady=PAD)
    button_restart.grid_remove()
    frame_feedback.grid_remove()

def update_question():
    """Updates the question label."""
    global current_question, selected_questions
    tk_textbox.delete("1.0", tk.END)
    label_result.grid_remove()
    button_next.grid_remove()

    if current_question < len(selected_questions):
        question = selected_questions[current_question]["Kérdés"]
        label_question.configure(text=f"Kérdés {current_question + 1}/{len(selected_questions)}:\n{question}")
        button_check.grid(row=0, column=0, pady=PAD)
    else:
        threading.Thread(target=end_quiz, daemon=True).start()  # Generate feedback in a separate thread


def check_answer():
    """Runs AI validation in a separate thread to prevent UI freezing."""
    threading.Thread(target=validate_answer, daemon=True).start()

def validate_answer():
    """Validates the user's answer using AI and updates the UI."""
    global current_question, score
    button_check.grid_remove()

    user_answer = tk_textbox.get("1.0", tk.END).strip()
    correct_answer = selected_questions[current_question]["Válasz"]

    label_result.grid(row=3, column=0, pady=PAD, padx=PAD, sticky="ew")
    label_result.configure(text="Ellenőrzés folyamatban...", text_color="black")  # Show loading text

    # AI-based validation
    is_correct = is_answer_correct(user_answer, correct_answer)

    responses.append({
        "question": selected_questions[current_question]["Kérdés"],
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "correct": is_correct
    })

    if is_correct:
        label_result.configure(text="Helyes!", text_color="green")
        score += 1
    else:
        label_result.configure(text=f"Helytelen! Helyes válasz: {correct_answer}", text_color="red")


    # Move to the next question or end quiz
    button_next.grid(row=0, column=1, pady=PAD)
    current_question += 1


def end_quiz():
    """Ends the quiz and generates AI feedback."""
    label_question.configure(text=f"Kvíz vége! Eredmény: {score}/{len(selected_questions)}")
    tk_textbox.grid_remove()
    button_next.grid_remove()
    button_check.grid_remove()
    label_result.grid_remove()

    # Display feedback loading message
    label_feedback_text.configure(text="MI visszajelzés generálása...", text_color="black")
    frame_feedback.grid(row=1, column=0, pady=PAD)

    # Generate AI feedback
    feedback = generate_feedback(responses)

    # Update feedback label
    label_feedback_text.configure(text=f"📢 MI visszajelzés a teljesítmény alapján:\n\n{feedback}",
                                  text_color="black",
                                  width=350)

    # Enable the restart button after feedback loads
    button_restart.configure(state=tk.NORMAL)
    button_restart.grid(row=2, column=0, pady=PAD)

if __name__ == "__main__":
    # Tkinter GUI setup
    root = ctk.CTk()
    root.title("Kvíz Alkalmazás")
    root.geometry("600x400")
    root.configure(padx=PAD, pady=PAD)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.resizable(False, False)

    frame_main = ctk.CTkFrame(root)
    frame_main.grid(row=0, column=0, rowspan=6, columnspan=2, sticky="nsew", ipadx=PAD, ipady=PAD)
    frame_main.grid_columnconfigure(0, weight=1)

    label_question = ctk.CTkLabel(frame_main, text="", font=FONT_LARGE, wraplength=400, anchor="center")
    label_question.grid(row=0, column=0, pady=PAD, padx=PAD, sticky="ew")

    tk_textbox = tk.Text(frame_main, width=60, height=8, font=FONT_MEDIUM)
    tk_textbox.grid(row=1, column=0,pady=PAD)

    frame_buttons = ctk.CTkFrame(frame_main, fg_color="transparent")
    frame_buttons.grid(row=2, column=0, pady=PAD, padx=PAD)

    button_check = ctk.CTkButton(frame_buttons, text="Ellenőrzés", command=check_answer, width=100)
    button_check.grid(row=0, column=0, padx=PAD)

    button_next = ctk.CTkButton(frame_buttons, text="Tovább", command=update_question, width=100)
    button_next.grid_remove()

    label_result = ctk.CTkLabel(frame_main, text="", font=FONT_MEDIUM, wraplength=400, anchor="center")
    label_result.grid(row=3, column=0, pady=PAD, padx=PAD, sticky="ew")

    frame_feedback = ctk.CTkScrollableFrame(frame_main, width=450, height=200)
    frame_feedback.grid_remove()

    label_feedback_text = ctk.CTkLabel(frame_feedback, text="", font=FONT_MEDIUM, wraplength=400, anchor="center")
    label_feedback_text.pack(fill="both", expand=True)

    button_restart = ctk.CTkButton(frame_main, text="Újraindítás", command=start_quiz, width=20)
    button_restart.grid(row=5, column=0, pady=PAD)

    # Start the quiz
    start_quiz()

    root.mainloop()
