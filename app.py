from flask import Flask, render_template, redirect, url_for
import json
import os
import csv
from datetime import datetime
import logging

app = Flask(__name__)


# ============================================================
# APPLICATION LOGGING
# ============================================================

logging.basicConfig(
    filename="snekpy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)



# ============================================================
# USER PROGRESS
# ============================================================

PROGRESS_FILE = "progress.json"


def load_progress():

    if not os.path.exists(PROGRESS_FILE):

        return {
            "xp": 250,
            "streak": 3,
            "completed_lessons": [],
            "completed_practice": []
        }

    try:

        with open(PROGRESS_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {
            "xp": 250,
            "streak": 3,
            "completed_lessons": [],
            "completed_practice": []
        }


def save_progress(progress):

    with open(PROGRESS_FILE, "w") as file:

        json.dump(
            progress,
            file,
            indent=4
        )


progress = load_progress()

# ============================================================
# CSV LEARNING ACTIVITY
# ============================================================

ACTIVITY_FILE = "learning_activity.csv"


def record_activity(lesson_id, activity, xp):

    file_exists = os.path.exists(ACTIVITY_FILE)

    with open(
        ACTIVITY_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Date",
                "Lesson",
                "Activity",
                "XP"
            ])

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            lesson_id,
            activity,
            xp
        ])


# ============================================================
# LESSON DATA
# ============================================================

lessons = {

    1: {
        "number": 1,
        "title": "Introduction to Python",
        "description": "Learn what Python is and write your first Python program.",
        "level": "Beginner",
        "topics": [
            "What is Python?",
            "Easy Syntax",
            "Python Uses",
            "First Program"
        ]
    },

    2: {
        "number": 2,
        "title": "Variables",
        "description": "Learn how Python stores and works with information.",
        "level": "Beginner",
        "topics": [
            "What is a Variable?",
            "Creating Variables",
            "Changing Values",
            "Using Variables"
        ]
    },

    3: {
        "number": 3,
        "title": "Data Types",
        "description": "Understand the most important Python data types.",
        "level": "Beginner",
        "topics": [
            "Strings",
            "Integers",
            "Floats",
            "Booleans"
        ]
    },

    4: {
        "number": 4,
        "title": "Operators",
        "description": "Learn how to perform calculations and comparisons.",
        "level": "Beginner",
        "topics": [
            "Arithmetic",
            "Comparison",
            "Logical Operators",
            "Calculations"
        ]
    },

    5: {
        "number": 5,
        "title": "Conditions",
        "description": "Learn how Python makes decisions using conditions.",
        "level": "Beginner",
        "topics": [
            "if",
            "elif",
            "else",
            "Decision Making"
        ]
    },

    6: {
        "number": 6,
        "title": "Loops",
        "description": "Learn how to repeat actions using Python loops.",
        "level": "Beginner",
        "topics": [
            "for Loop",
            "while Loop",
            "range()",
            "Automation"
        ]
    },

    7: {
        "number": 7,
        "title": "Functions",
        "description": "Learn how to create reusable blocks of Python code.",
        "level": "Intermediate",
        "topics": [
            "Create Functions",
            "Parameters",
            "Return Values",
            "Reusability"
        ]
    },

    8: {
        "number": 8,
        "title": "Lists & Dictionaries",
        "description": "Learn how to store and manage collections of data.",
        "level": "Intermediate",
        "topics": [
            "Lists",
            "Dictionaries",
            "Access Data",
            "Modify Data"
        ]
    }
}


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# LEARN
# ============================================================

@app.route("/learn")
def learn():

    return render_template(
        "learn.html",
        lessons=lessons
    )


# ============================================================
# INDIVIDUAL LESSON
# ============================================================

@app.route("/learn/lesson/<int:lesson_id>")
def lesson(lesson_id):

    if lesson_id not in lessons:

        return render_template(
            "lesson_intro.html",
            lesson_id=lesson_id,
            lesson=None,
            lessons=lessons
        ), 404


    current_lesson = lessons[lesson_id]


    previous_lesson = None
    next_lesson = None


    if lesson_id > 1:

        previous_lesson = lesson_id - 1


    if lesson_id < len(lessons):

        next_lesson = lesson_id + 1


    return render_template(
        "lesson_intro.html",
        lesson_id=lesson_id,
        lesson=current_lesson,
        lessons=lessons,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson
    )


# ============================================================
# INTRODUCTION
# ============================================================

@app.route("/learn/introduction")
def introduction():

    return render_template(
        "lesson_intro.html",
        lesson_id=1,
        lesson=lessons[1],
        lessons=lessons,
        previous_lesson=None,
        next_lesson=2
    )

# ============================================================
# PRACTICE
# ============================================================

practice_data = {

    1: {
        "title": "Print Your Name",
        "challenge": "Write a Python program that prints your name on the screen.",
        "example": 'print("Sahana")',
        "expected": 'print("Sahana")'
    },

    2: {
        "title": "Create a Variable",
        "challenge": "Create a variable called age and store the value 20 in it.",
        "example": "age = 20",
        "expected": "age = 20"
    },

    3: {
        "title": "Create a Boolean",
        "challenge": "Create a variable called is_student and store True in it.",
        "example": "is_student = True",
        "expected": "is_student = True"
    },

    4: {
        "title": "Simple Calculation",
        "challenge": "Create a variable called result and store 10 + 5 in it.",
        "example": "result = 10 + 5",
        "expected": "result = 10 + 5"
    },

    5: {
        "title": "Use a Condition",
        "challenge": "Write a program that prints 'Adult' when age is greater than or equal to 18.",
        "example": "if age >= 18:\n    print('Adult')",
        "expected": "if age >= 18:\n    print('Adult')"
    },

    6: {
        "title": "Use a Loop",
        "challenge": "Write a for loop that prints the numbers from 1 to 5.",
        "example": "for i in range(1, 6):\n    print(i)",
        "expected": "for i in range(1, 6):\n    print(i)"
    },

    7: {
        "title": "Create a Function",
        "challenge": "Create a function called greet that prints 'Hello'.",
        "example": "def greet():\n    print('Hello')",
        "expected": "def greet():\n    print('Hello')"
    },

    8: {
        "title": "Create a List",
        "challenge": "Create a list called fruits containing apple, banana and mango.",
        "example": 'fruits = ["apple", "banana", "mango"]',
        "expected": 'fruits = ["apple", "banana", "mango"]'
    }

}


@app.route("/practice/<int:lesson_id>")
def practice(lesson_id):

    if lesson_id not in practice_data:

        return render_template(
            "lesson_intro.html",
            lesson_id=lesson_id,
            lesson=None,
            lessons=lessons
        ), 404

    return render_template(
        "practice.html",
        lesson_id=lesson_id,
        practice=practice_data[lesson_id]
    )


# ============================================================
# COMPLETE PRACTICE
# ============================================================

@app.route("/practice/<int:lesson_id>/complete", methods=["POST"])
def complete_practice(lesson_id):

    if lesson_id not in practice_data:
        return redirect(url_for("learn"))

    if lesson_id not in progress["completed_practice"]:

        progress["completed_practice"].append(
            lesson_id
        )

        progress["xp"] += 20

        record_activity(
            lesson_id,
            "Practice Completed",
            20
        )

        save_progress(progress)

    return redirect(
        url_for(
            "practice",
            lesson_id=lesson_id
        )
    )


# ============================================================
# CODE LAB
# ============================================================

@app.route("/code")
def code_lab():

    return render_template(
        "code_editor.html"
    )


# ============================================================
# REELS
# ============================================================

@app.route("/reels")
def reels():

    return render_template(
        "reels.html"
    )


# ============================================================
# PROJECTS
# ============================================================

@app.route("/projects")
def projects():

    return render_template(
        "projects.html"
    )


# ============================================================
# PROFILE
# ============================================================

@app.route("/profile")
def profile():

    current_progress = load_progress()

    completed_lessons = len(
        current_progress["completed_lessons"]
    )

    total_lessons = len(lessons)

    progress_percentage = int(
        (completed_lessons / total_lessons) * 100
    )

    return render_template(
        "profile.html",
        xp=current_progress["xp"],
        streak=current_progress["streak"],
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        progress_percentage=progress_percentage
    )


# ============================================================
# CUSTOM 404 PAGE
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return """
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0">

        <title>
            SNEK.PY — Page Not Found
        </title>

        <style>

            body {

                margin: 0;

                min-height: 100vh;

                display: grid;

                place-items: center;

                background: #0b0b0f;

                color: white;

                font-family:
                    Arial,
                    sans-serif;

                text-align: center;
            }


            .error-container {

                padding: 30px;

            }


            h1 {

                font-size: 80px;

                margin: 0;

            }


            h2 {

                margin-top: 10px;

            }


            p {

                color: #aaa;

                font-size: 18px;

            }


            a {

                display: inline-block;

                margin-top: 20px;

                padding: 12px 20px;

                border-radius: 10px;

                background: #8b5cf6;

                color: white;

                text-decoration: none;

                font-weight: bold;

            }


            a:hover {

                opacity: 0.85;

            }

        </style>

    </head>


    <body>

        <div class="error-container">

            <h1>
                404 🐍
            </h1>

            <h2>
                Oops! Page not found.
            </h2>

            <p>
                Don't worry.
                Your Python journey is still safe.
            </p>

            <a href="/">
                ← Back to SNEK.PY
            </a>

        </div>

    </body>

    </html>
    """, 404


# ============================================================
# RUN APPLICATION
# ============================================================

# ============================================================
# ERROR HANDLING
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    logger.warning(
        "Page not found: %s",
        error
    )

    return render_template(
        "index.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    logger.exception(
        "Internal server error"
    )

    return render_template(
        "index.html"
    ), 500


if __name__ == "__main__":

    app.run(
        debug=True
    )