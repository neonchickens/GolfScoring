from DataTypes import *
from Analysis import *

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


dir_duels = "F25_KW_DUELS"
dir_party = "F25_PARTY"

directory_courses = "Data/Courses/"
directory_scores = f"Data/Scorecards/{dir_party}"

# Real golf handicaps use a total number of strokes between players and the hole handicaps set by the course to determine scores
# TODO implement real handicaps next season
is_real_handicap_system = False
handicap_per_hole = { "w": 0, "k": 1, "m": 1.5, }
handicap_per_course = { "w": 0, "k": 10, "m": 14, }


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
all_courses = get_all_files(directory_courses, Course.file_from)
all_scorecards = get_all_files(directory_scores, Scorecard.file_from)

# list(map(print, all_courses))
# list(map(print, all_scorecards))




# Process the above inputs for analysis

# The below is currently tied to a season
# Games includes from non season games may break this
# TODO seperate general statistics from season statistics

# Should have done dataframes probably
# TODO dataframes?


def GetScorecardSortingOrder(scorecard):
    return scorecard.date, scorecard.course
all_scorecards.sort(key=GetScorecardSortingOrder)

player_strokes = {}
player_h_strokes = {}
player_skins = {}
player_strokes_cumulative = {}
player_h_strokes_cumulative = {}
player_skins_cumulative = {}

def init_player_lists(player: str) -> None:
    player_strokes[player] = []
    player_h_strokes[player] = []
    player_skins[player] = []
    player_strokes_cumulative[player] = [0]
    player_h_strokes_cumulative[player] = [0]
    player_skins_cumulative[player] = [0]


# get all strokes in order
max_count_strokes = 0
queue_scorecards = list(all_scorecards)
while len(queue_scorecards) > 0:
    date_current = queue_scorecards[0].date
    course_current = queue_scorecards[0].course
    lst_match = []
    while len(queue_scorecards) > 0 and date_current == queue_scorecards[0].date and course_current == queue_scorecards[0].course:
        lst_match.append(queue_scorecards[0])
        queue_scorecards.pop(0)

    # we now have all of the scorecards that played together

    score_running = 0
    course = [x for x in all_courses if course_current in x.name and x.index_tee == 1][0]
    for i in range(len(lst_match[0].score_per_hole)):
        min_score = 9
        player_score = None
        score_running += 1
        for m in lst_match:
            if m.player not in player_strokes:
                init_player_lists(m.player)

            player_strokes[m.player].append(m.score_per_hole[i])
            player_strokes_cumulative[m.player].append(player_strokes_cumulative[m.player][-1] + m.score_per_hole[i])

            handicap = 0
            if is_real_handicap_system:
                handicap = (handicap_per_course[m.player] // 9) + (1 if handicap_per_course[m.player] % 9 >= course.handicap_per_hole[i] else 0)
            else:
                handicap = handicap_per_hole[m.player]
            score_handicap = m.score_per_hole[i] - handicap
            player_h_strokes[m.player].append(score_handicap)
            player_h_strokes_cumulative[m.player].append(player_h_strokes_cumulative[m.player][-1] + score_handicap)
            
            # did player potentially win skin
            if score_handicap < min_score:
                player_score = m.player
                min_score = score_handicap
            elif score_handicap == min_score: # ties carry to the next hole
                player_score = None


        # we now know if a skin was won
        for key in player_strokes:
            player_skins[key].append(score_running if key == player_score else 0)
            player_skins_cumulative[key].append(player_skins_cumulative[key][-1] + player_skins[key][-1])

        # reset skin counter
        if player_score is not None:
            score_running = 0
    


# Show plots
create_season_strokes(player_strokes_cumulative, player_h_strokes_cumulative)
create_season_skins(player_skins_cumulative)
create_box_plot(list(player_strokes.keys()), list(player_strokes.values()))