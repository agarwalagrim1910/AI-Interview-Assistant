import sqlite3
import json
from datetime import datetime


DB_NAME = "interview_history.db"


# -----------------------------------------
# Create Database Connection
# -----------------------------------------

def get_connection():

    return sqlite3.connect(
        DB_NAME
    )


# -----------------------------------------
# Create Tables
# -----------------------------------------

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date TEXT,

            skills TEXT,

            questions TEXT,

            answers TEXT,

            scores TEXT,

            feedbacks TEXT,

            average_score REAL,

            verdict TEXT

        )
        """
    )

    conn.commit()

    conn.close()


# -----------------------------------------
# Save Interview
# -----------------------------------------

def save_interview(
    skills,
    questions,
    answers,
    scores,
    feedbacks,
    average_score,
    verdict
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interviews
        (
            date,
            skills,
            questions,
            answers,
            scores,
            feedbacks,
            average_score,
            verdict
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            json.dumps(skills),

            json.dumps(questions),

            json.dumps(answers),

            json.dumps(scores),

            json.dumps(feedbacks),

            average_score,

            verdict

        )

    )

    conn.commit()

    conn.close()


# -----------------------------------------
# Fetch Previous Interviews
# -----------------------------------------

def get_interviews():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM interviews
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data