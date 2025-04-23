import os
import huspacy
import json
import random
import hu_core_news_lg
import google.generativeai as genai

nlp = huspacy.load()
npl = hu_core_news_lg.load()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def validate_with_huspacy(ans1, ans2, threshold=0.6):
    """Check if two answers are similar using HuSpaCy NLP embeddings."""
    doc1 = nlp(ans1)
    doc2 = nlp(ans2)

    similarity = doc1.similarity(doc2)
    return similarity >= threshold

def validate_with_gemini(user_answer, correct_answer, model_name="gemini-2.0-flash-lite"):
    """Use a specified Google Gemini model to validate the answer."""

    prompt = f"""The following is a Hungarian quiz question. Determine if the user's answer is correct or close to 
    the correct answer.
    
    Correct answer: {correct_answer}
    User's answer: {user_answer}
    
    Respond with only "true" if the answer is correct or close enough, otherwise respond with "false". 
    """

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return "true" in response.text.lower()

def is_answer_correct(user_answer, correct_answer):
    """Use multiple validation methods and apply majority voting."""

    if user_answer is None or user_answer == "":
        return False

    validations = [
        validate_with_huspacy(user_answer, correct_answer),
        validate_with_gemini(user_answer, correct_answer, "gemini-2.0-flash"),
        validate_with_gemini(user_answer, correct_answer, "gemini-1.5-flash")
    ]

    return sum(validations) >= 2 # Accept if at least 2 say it's correct


def generate_feedback(responses):
    """Send the user's responses to Gemini to generate feedback."""

    prompt = "Analyze the following quiz answers and provide feedback on mistakes:\n\n"

    for item in responses:
        prompt += f"Question: {item["question"]}\n"
        prompt += f"User's Answer: {item["user_answer"]}\n"
        prompt += f"Correct Answer in database: {item["correct_answer"]}\n"
        prompt += (f"Considered the answer: {"correct" if item["correct"] else "false"} "
                   f"based on the db answer and two ai models.\n\n")

    prompt += ("Give a short (one paragraph), brief explanation of common mistakes and suggestions for improvement. "
               "Please answer in Hungarian. And format the text with new lines, logically split into paragraphs, and "
               "justify the lines too, please.")

    model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")
    response = model.generate_content(prompt)
    return response.text

def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # Load the JSON file

    questions = []
    for category, items in data.items():  # Iterate over each category and its questions
        if isinstance(items, list):  # Ensure it's a list
            questions.extend(items)  # Add individual questions to the list

    return questions

def start_quiz(questions, num_questions=5):
    """Starts the quiz logic."""

    if len(questions) < num_questions:
        print(f"Only {len(questions)} questions available. Adjusting quiz length to {len(questions)}.")
        num_questions = len(questions)

    score = 0
    selected_questions = random.sample(questions, num_questions)

    responses = []

    for q in selected_questions:
        user_answer = input(q["Kérdés"] + " ").strip().lower()
        correct_answer = q["Válasz"].lower()


        is_correct = is_answer_correct(user_answer, correct_answer)
        responses.append({
            "question": q["Kérdés"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "correct": is_correct
        })

        if is_correct:
            print("Helyes!")
            score += 1
        else:
            print(f"Helytelen. A helyes válasz: {correct_answer}")

    print(f"Végeredmény: {score}/{num_questions} pont.")

    feedback = generate_feedback(responses)
    print("\n📢 AI Feedback on your performance:\n")
    print(feedback)

# Load questions and start the quiz
if __name__ == "__main__":
    quiz_questions = load_questions("questions.json")
    start_quiz(quiz_questions)
