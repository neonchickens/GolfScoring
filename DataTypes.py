class Course:
    def __init__(self):
        self.name = ""
        self.index_tee = 0
        self.handicap_per_hole = []
        self.yards_per_hole = []


    def __str__(self):
        return f"{self.name}, {self.index_tee}, {self.yards_per_hole}"


    def file_from(location):
        newCourses = []
        with open(location, "r", encoding="utf-8") as f:
            index = 0
            handicap_per_hole = []
            for line in f:
                if line.endswith("\n"):
                    line = line[:-1]
                if index == 0:
                    entries = line.split(",")
                    handicap_per_hole = list(map(int, entries))
                else:
                    newCourse = Course()
                    newCourse.name = location
                    newCourse.index_tee = index
                    entries = line.split(",")
                    newCourse.handicap_per_hole = list(handicap_per_hole)
                    newCourse.yards_per_hole = list(map(int, entries))
                    newCourses.append(newCourse)
                index += 1
        return newCourses


class Scorecard:
    def __init__(self):
        self.player = ""
        self.date = ""
        self.course = ""
        self.index_tee = 0
        self.score_per_hole = []


    def __str__(self):
        return f"{self.player}, {self.course}, {self.index_tee}, {self.score_per_hole}"
    

    def file_from(location):
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
                    date = line
                else:
                    newScorecard = Scorecard()
                    newScorecard.course = course
                    newScorecard.date = date
                    entries = line.split(",")
                    newScorecard.index_tee = entries[0]
                    newScorecard.player = entries[1]
                    newScorecard.score_per_hole = list(map(int, entries[2:]))
                    newScorecards.append(newScorecard)
                index += 1
        return newScorecards
    