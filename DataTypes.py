from typing import Type
from datetime import datetime, date

class Course:
    def __init__(self):
        self.name = ""
        self.index_tee = 0
        self.par_per_hole = []
        self.handicap_per_hole = []
        self.yards_per_hole = []


    def __str__(self):
        return f"{self.name}, {self.index_tee}, {self.yards_per_hole}"


    def file_from(location: str) -> list['Course']:
        newCourses = []
        with open(location, "r", encoding="utf-8") as f:
            index = 0
            par_per_hole = []
            handicap_per_hole = []
            for line in f:
                if line.endswith("\n"):
                    line = line[:-1]
                if index == 0:
                    entries = line.split(",")
                    handicap_per_hole = list(map(int, entries))
                elif index == 1:
                    entries = line.split(",")
                    par_per_hole = list(map(int, entries))
                else:
                    newCourse = Course()
                    newCourse.name = location
                    newCourse.index_tee = index - 1
                    entries = line.split(",")
                    newCourse.par_per_hole = list(par_per_hole)
                    newCourse.handicap_per_hole = list(handicap_per_hole)
                    newCourse.yards_per_hole = list(map(int, entries))
                    newCourses.append(newCourse)
                index += 1
        return newCourses


def get_date_from_string(string: str) -> date:
    return 

class Scorecard:

    def __init__(self):
        self.player = ""
        self.date = date(2000, 1, 1)
        self.course = ""
        self.index_tee = 0
        self.strokes_per_hole = []

    


    def __str__(self):
        return f"{self.player}, {self.course}, {self.index_tee}, {self.strokes_per_hole}"
    

    def file_from(location: str) -> list['Scorecard']:
        newScorecards = []
        with open(location, "r", encoding="utf-8") as f:
            index = 0
            course = ""
            date = ""
            for line in f:
                if line.endswith("\n"):
                    line = line[:-1]
                if index == 0:
                    course = line
                elif index == 1:
                    date = datetime.fromisoformat(line).date()
                else:
                    newScorecard = Scorecard()
                    newScorecard.course = course
                    newScorecard.date = date
                    entries = line.split(",")
                    newScorecard.index_tee = entries[0]
                    newScorecard.player = entries[1]
                    newScorecard.strokes_per_hole = list(map(int, entries[2:]))
                    newScorecards.append(newScorecard)
                index += 1
        return newScorecards
    