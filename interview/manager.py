class InterviewManager:
    """
    Controls adaptive interview flow
    based on candidate performance.
    """

    def __init__(self):

        self.strengths = []

        self.weaknesses = []


    # ---------------------------------------
    # Decide Next Difficulty
    # ---------------------------------------

    def decide_difficulty(
        self,
        current_difficulty,
        score
    ):

        levels = [
            "Easy",
            "Medium",
            "Hard"
        ]

        index = levels.index(
            current_difficulty
        )


        if score >= 8:

            index = min(
                index + 1,
                len(levels) - 1
            )


        elif score <= 5:

            index = max(
                index - 1,
                0
            )


        return levels[index]


    # ---------------------------------------
    # Analyze Performance
    # ---------------------------------------

    def analyze_performance(
        self,
        score,
        question,
        feedback=""
    ):

        record = {

            "question": question,

            "feedback": feedback,

            "score": score

        }


        if score >= 8:

            self.strengths.append(
                record
            )


        elif score <= 5:

            self.weaknesses.append(
                record
            )


    # ---------------------------------------
    # Create Adaptive Context
    # ---------------------------------------

    def get_performance_context(self):

        context = ""


        if self.strengths:

            context += (
                "Candidate performed well in:\n"
            )

            for item in self.strengths[-2:]:

                context += (
                    f"- {item['question']}\n"
                )


        if self.weaknesses:

            context += (
                "\nCandidate struggled with:\n"
            )

            for item in self.weaknesses[-2:]:

                context += (
                    f"- {item['question']}\n"
                    f"Feedback: {item['feedback']}\n"
                )


        if not context:

            context = (
                "No performance history available yet."
            )


        return context


    # ---------------------------------------
    # Summary
    # ---------------------------------------

    def get_summary(self):

        return {

            "strengths": self.strengths,

            "weaknesses": self.weaknesses

        }