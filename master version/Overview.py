from pathlib import Path
import json

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import ipywidgets as widgets
from IPython.display import clear_output


class Overview:

    CORRECT = "correct"
    INCORRECT = "incorrect"
    UNANSWERED = "unanswered"

    def __init__(self, controller):
        self.controller = controller

        self.answers_output = widgets.Output()
        self.results_output = widgets.Output()
        self.heatmap_output = widgets.Output()

        self.refresh_button = widgets.Button(
            description="Refresh"
        )
        self.refresh_button.on_click(self.refresh)

        self.vbox = widgets.VBox([
            self.refresh_button,
            self.answers_output,
            self.results_output,
            self.heatmap_output,
        ])


    def get_ui(self):
        return self.vbox

    def refresh(self, _=None):
        self.controller.drive.download_questions_for_selection(self.controller)
        data = self.load_data()

        with self.answers_output:
            clear_output(wait=True)
            self.plot_answers_per_question(data)

        with self.results_output:
            clear_output(wait=True)
            self.plot_results_overview(data)

        with self.heatmap_output:
            clear_output(wait=True)
            self.plot_progress_heatmap(data)


    def load_data(self):
        data = {}

        drive_path = Path("./drive")

        selected_component = self.controller.component
        selected_run = self.controller.run

        for file in drive_path.glob("overview_*.json"):
            try:
                parts = file.stem.split("_")
                if len(parts) < 4:
                    continue
                userid = parts[-1]
                run = parts[-2]
                component = "_".join(parts[1:-2])

                if component != selected_component or run != selected_run:
                    continue

                key = f"{component}_{run}"
                with open(file, encoding="utf-8") as f:
                    data[key] = json.load(f)
            except Exception as e:
                print(f"Failed reading {file}: {e}")
        return data

    def get_questions(self, data):
        questions = set()

        for student_results in data.values():
            questions.update(student_results.keys())

        return sorted(questions)


    def plot_answers_per_question(self, data):

        questions = self.get_questions(data)

        counts = []

        for question in questions:

            submitted = 0

            for student_results in data.values():

                result = student_results.get(
                    question,
                    self.UNANSWERED
                )

                if result != self.UNANSWERED:
                    submitted += 1

            counts.append(submitted)

        plt.figure(figsize=(10, 4))

        plt.bar(questions, counts)

        plt.title("Answers per Question")
        plt.ylabel("Students")

        plt.xticks(rotation=90)

        plt.tight_layout()
        plt.show()


    def plot_results_overview(self, data):

        questions = self.get_questions(data)
        total_students = len(data)

        rows = []

        for question in questions:

            correct = 0
            incorrect = 0
            unanswered = 0

            for student_results in data.values():

                result = student_results.get(question, self.UNANSWERED)

                if result == self.CORRECT:
                    correct += 1

                elif result == self.INCORRECT:
                    incorrect += 1

                else:
                    unanswered += 1

            rows.append({
                "question": question,
                "correct": 100 * correct / total_students,
                "incorrect": 100 * incorrect / total_students,
                "unanswered": 100 * unanswered / total_students,
            })

        df = pd.DataFrame(rows)

        plt.figure(figsize=(10, 4))
        
        plt.bar(
            df["question"],
            df["incorrect"],
            label="Incorrect",
            color="red"
        )

        plt.bar(
            df["question"],
            df["unanswered"],
            bottom=df["incorrect"],
            label="Unanswered",
            color="lightgray"
        )

        plt.bar(
            df["question"],
            df["correct"],
            bottom=df["incorrect"] + df["unanswered"],
            label="Correct",
            color="green"
        )

        plt.title("Question Results")
        plt.ylabel("Percentage")
        plt.ylim(0, 100)

        plt.xticks(rotation=90)

        plt.legend()
        plt.tight_layout()
        plt.show()


    def plot_progress_heatmap(self, data):
        questions = self.get_questions(data)
        df = pd.DataFrame(
            float("nan"),
            index=data.keys(),
            columns=questions
        )

        for student, results in data.items():
            for question, result in results.items():
                if result == self.CORRECT:
                    df.loc[student, question] = 1

                elif result == self.INCORRECT:
                    df.loc[student, question] = 0

        annotations = df.copy()

        annotations = annotations.replace({
            1: "✓",
            0: "✗"
        }).fillna("")

        plt.figure(figsize=(12, 8))

        sns.heatmap(
            df,
            annot=annotations,
            fmt="",
            cmap="RdYlGn",
            vmin=0,
            vmax=1,
            cbar=False,
            linewidths=0.5
        )

        plt.title("Student Progress")
        plt.xlabel("Questions")
        plt.ylabel("Students")

        plt.tight_layout()
        plt.show()