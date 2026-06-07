QUESTION_BANK = {
    "Java": [
        "What is JVM?",
        "Explain OOP concepts.",
        "Difference between ArrayList and LinkedList?"
    ],

    "Python": [
        "Difference between list and tuple?",
        "What is a dictionary?",
        "Explain Python decorators."
    ],

    "Data Structures": [
        "What is a stack?",
        "Difference between stack and queue?",
        "Explain hashing."
    ],

    "Algorithms": [
        "What is binary search?",
        "Explain time complexity.",
        "What is dynamic programming?"
    ],

    "Git": [
        "What is Git?",
        "Difference between merge and rebase?",
        "Explain git stash."
    ]
}


def generate_questions(skills):

    questions = []

    for skill in skills:

        if skill in QUESTION_BANK:
            questions.extend(QUESTION_BANK[skill])

    return questions