from DataTypes import *
import os

directory_courses = "Data/Courses/"
directory_scores = "Data/Scorecards/"

# Retrieves all files from directory, recursively
# method is what consumes the file and returns a list of objects
def get_all_files(directory, method):
    lst = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            newEntry = method(filepath)
            lst.extend(newEntry)
        else:
            lst.extend(get_all_files(filepath, method))
    return lst

# Read all data from files
allCourses = get_all_files(directory_courses, Course.file_from)
allScorecards = get_all_files(directory_scores, Scorecard.file_from)

list(map(print, allCourses))
# list(map(print, allScorecards))



# Process the above inputs into a dataframe for analysis