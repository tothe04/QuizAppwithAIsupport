# QuizAppwithAIsupport

***This is a simple quiz application built using Python with the Tkinter and CustomTkinter libraries for the graphical 
user interface. The quiz selects random questions from a JSON file and allows users to answer them. After completing 
the quiz, an AI-based feedback system provides an analysis of the user's performance.***

## Table of contents

- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)

---

## Installation

### Clone the repository

- `git clone https://github.com/tothe04/QuizAppwithAIsupport.git`
- `cd QuizAppwithAIsupport`

---

## Setup

1. Create a virtual environment: <br>
    - In the project root run `python -m venv venv`
2. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On Unix or macOS, run: `source tutorial-env/bin/activate`
3. Install the required dependencies: <br>
   `pip install -r requirements.txt`
4. Set up the environment variables
   - A Google Gemini API key is needed for this project to run properly, you can get one here:
        - [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) (note: this does have a free tier
        limit)
        - You will need to set this key as "GOOGLE_API_KEY" in an env variable
    - Either create a `.env` file in the root directory or set up in system environment variables.

---

### Running the Application

1. Ensure all dependencies are installed.

2. Run the script:
    - `python main.py`
