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
        for filename in os.listdir("../questions"):
            path = f"../questions/{filename}"

            with open(path, encoding="utf-8") as f:
                data = json.load(f)

                if (data["component"] == self.controller.component and
                    data["run"] == self.controller.run):
                    questions.append(data)  
        return questions 
    
    def delete_question(self, index):
        filename = (
            f"../questions/"
            f"{self.controller.component}_"
            f"{self.controller.run}_"
            f"{index}.json"
        )

        if os.path.exists(filename):
            os.remove(filename)
        
    def save_question(self, question_data):
        print("Hoi")
        print(self.controller.run)
        print(self.controller.component)
    
        question_data["component"] = self.controller.component
        question_data["run"] = self.controller.run      

        with open("../questions/" + self.controller.component + "_" + self.controller.run + "_" +  str(question_data["index"]) + ".json", "w", encoding="utf-8") as f:
            json.dump(question_data, f, indent=4, ensure_ascii=False)