import json
import os
from pathlib import Path

class QuestionController:
    def __init__(self, controller):
        self.controller = controller
        self.answers = []
        self.overview = []

    def read_questions(self):
        questions = []
        for filename in os.listdir("./questions"):
            path = f"./questions/{filename}"

            with open(path, encoding="utf-8") as f:
                data = json.load(f)

                if (data["component"] == self.controller.component and
                    data["run"] == self.controller.run):
                    questions.append(data)  
        return questions 

    def save_answer(self, question_name, answer, correct):
        self.overview[question_name] = correct
        self.answers[question_name] = answer
        # save overview
        filename = f"./drive/overview_{self.controller.userid}_{self.controller.run}.json"
        path = Path(filename)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.overview, f)
        self.controller.drive.upload_file(filename)

        # save answer
        filename = f"./drive/answers_{self.controller.userid}_{self.controller.run}.json"
        path = Path(filename)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.answers, f)
        
        self.controller.drive.upload_file(filename)

        self.controller.quiz.update_questions()

        


    def set_progress(self):
        overview_map = {}
        filename = f"./drive/overview_{self.controller.userid}_{self.controller.run}.json"
        path = Path(filename)

        exists = True

        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                overview_map = json.load(f)
        else:
            exists = False

        for q in self.controller.questions:
            title = q["title"]
            if title not in overview_map:
                overview_map[title] = "unanswered"
        
        self.overview = overview_map

        if exists == False:
            with path.open("w", encoding="utf-8") as f:
                json.dump(overview_map, f)
                #todo write to drive

        exists = True
        answers_map = {}
        filename = f"./drive/answers_{self.controller.userid}_{self.controller.run}.json"
        path = Path(filename)
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                answers_map = json.load(f)
        else:
            exists = False

        for q in self.controller.questions:
            title = q["title"]
            if title not in answers_map:
                answers_map[title] = "unanswered"
        
        self.answers = answers_map
        if exists == False:
            with path.open("w", encoding="utf-8") as f:
                json.dump(answers_map, f)
                #todo write to drive
                

    # def save_answer(self):
        
         