from DataTypes import *
from Analysis import *

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


dir_other = "OTHER"
dir_duels = "F25_KW_DUELS"
dir_party = "F25_PARTY"
dir_none = ""

directory_courses = "Data/Courses/"
directory_scores = f"Data/Scorecards/{dir_party}"

# Real golf handicaps use a total number of strokes between players and the hole handicaps set by the course to determine scores
# TODO implement real handicaps next season
is_real_handicap_system = False
is_scaled_to_lowest_handicap = True
handicap_per_hole = { "w": 1, "k": 2, "m": 2.5, }
handicap_per_course = { "w": 0, "k": 9, "m": 14, }
# handicap_per_course = { "w": 5, "k": 14, "m": 21, }

# The below is currently tied to a season
# Games includes from non season games may break this
# TODO seperate general statistics from season statistics
is_season = True


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

# Should have done dataframes probably
# TODO dataframes?

# A non par 3 match will definitely mess some stuff up
# TODO make more robust

def GetScorecardSortingOrderScore(scorecard):
    return sum(scorecard.strokes_per_hole)
def GetScorecardSortingOrderTime(scorecard):
    return scorecard.date, scorecard.course
all_scorecards.sort(key=GetScorecardSortingOrderTime)

# Player statistics
player_strokes = {}
player_h_strokes = {}
player_par = {}
player_h_par = {}
player_skins = {}
player_strokes_cumulative = {}
player_h_strokes_cumulative = {}
player_par_cumulative = {}
player_h_par_cumulative = {}
player_skins_cumulative = {}
player_games = {}

# Course statistics
course_strokes = {}
course_par = {}
course_h_par = {}
hole_strokes = {}
hole_par = {}
hole_h_par = {}

def init_player_lists(player: str) -> None:
    player_strokes[player] = []
    player_h_strokes[player] = []
    player_par[player] = []
    player_h_par[player] = []
    player_skins[player] = []
    player_strokes_cumulative[player] = [0]
    player_h_strokes_cumulative[player] = [0]
    player_par_cumulative[player] = [0]
    player_h_par_cumulative[player] = [0]
    player_skins_cumulative[player] = [0]
    
    player_games[player] = []


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

    # get the minimum handicap of all players in the match
    # the player with the lowest handicap receives no strokes
    min_handicap = 0
    if is_scaled_to_lowest_handicap:
        min_handicap = 1000
        for m in lst_match:
            p = m.player
            if is_real_handicap_system:
                if handicap_per_course[p] < min_handicap:
                    min_handicap = handicap_per_course[p]
            else:
                if handicap_per_hole[p] < min_handicap:
                    min_handicap = handicap_per_hole[p]

    # go through holes in order
    score_running = 0
    course = [x for x in all_courses if course_current in x.name and x.index_tee == 1][0]
    for i in range(len(lst_match[0].strokes_per_hole)):
        min_score = 9
        player_score = None
        score_running += 1
        for m in lst_match:
            if m.player not in player_strokes:
                init_player_lists(m.player)

            # stat keeping
            player_strokes[m.player].append(m.strokes_per_hole[i])
            player_strokes_cumulative[m.player].append(player_strokes_cumulative[m.player][-1] + m.strokes_per_hole[i])

            player_par[m.player].append(m.strokes_per_hole[i] - course.par_per_hole[i])
            player_par_cumulative[m.player].append(player_par_cumulative[m.player][-1] + player_par[m.player][-1])

            handicap_hole_match = 0
            handicap_hole_course = 0
            if is_real_handicap_system:
                handicap_match = handicap_per_course[m.player] - min_handicap
                handicap_hole_match = (handicap_match // 9) + (1 if handicap_match % 9 >= course.handicap_per_hole[i] else 0)
                handicap_hole_course = (handicap_per_course[m.player] // 9) + (1 if handicap_per_course[m.player] % 9 >= course.handicap_per_hole[i] else 0)
            else:
                handicap_hole_match = handicap_per_hole[m.player] - min_handicap
                handicap_hole_course = handicap_per_hole[m.player]
            score_handicap = m.strokes_per_hole[i] - handicap_hole_match
            player_h_strokes[m.player].append(score_handicap)
            player_h_strokes_cumulative[m.player].append(player_h_strokes_cumulative[m.player][-1] + score_handicap)

            player_h_par[m.player].append(m.strokes_per_hole[i] - course.par_per_hole[i] - handicap_hole_match)
            player_h_par_cumulative[m.player].append(player_h_par_cumulative[m.player][-1] + player_h_par[m.player][-1])
            
            # did player potentially win skin
            if score_handicap < min_score:
                player_score = m.player
                min_score = score_handicap
            elif score_handicap == min_score: # ties carry to the next hole
                player_score = None

            # stat keeping
            key_hole = f"{course.name}_{i+1}"
            if key_hole not in hole_strokes:
                hole_strokes[key_hole] = []
                hole_par[key_hole] = []
                hole_h_par[key_hole] = []
            hole_strokes[key_hole].append(player_strokes[m.player][-1])
            hole_par[key_hole].append(player_strokes[m.player][-1] - course.par_per_hole[i])
            hole_h_par[key_hole].append(player_strokes[m.player][-1] - course.par_per_hole[i] - handicap_hole_course)

        # we now know if a skin was won
        for key in player_strokes:
            player_skins[key].append(score_running if key == player_score else 0)
            player_skins_cumulative[key].append(player_skins_cumulative[key][-1] + player_skins[key][-1])

        # reset skin counter
        if player_score is not None:
            score_running = 0
    
    # stat keeping
    for m in lst_match:
        player_games[m.player].append(sum(m.strokes_per_hole))

        if course.name not in course_strokes:
            course_strokes[course.name] = []
            course_par[course.name] = []
            course_h_par[course.name] = []
        course_strokes[course.name].append(sum(m.strokes_per_hole))
        course_par[course.name].append(sum(m.strokes_per_hole) - sum(course.par_per_hole))

        if is_real_handicap_system:
            course_h_par[course.name].append(sum(m.strokes_per_hole) - sum(course.par_per_hole) - handicap_per_course[m.player])
        else:
            course_h_par[course.name].append(sum(m.strokes_per_hole) - sum(course.par_per_hole) - len(m.strokes_per_hole) * handicap_per_hole[m.player])
    

# Golf GHIN handicap calculator
# average of best 8 games of last 20
# scale par 27 up to par 72
for p in handicap_per_course: # iterate list of players
    # TODO should scale games to 72 before sorting?
    recent_games = [x for x in all_scorecards if p == x.player]
    if len(recent_games) >= 20:
        recent_games = recent_games[:20]
    recent_games.sort(key=GetScorecardSortingOrderScore)
    if len(recent_games) >= 8:
        recent_games = recent_games[:8]
    total = 0
    for s in recent_games:
        total += sum(s.strokes_per_hole)
    hdcp27 = total / len(recent_games) - 27
    hdcp32 = hdcp27 * (32/27)
    hdcp36 = hdcp27 * (36/27)
    hdcp72 = hdcp27 * (72/27)
    print(f"{p}: {int(hdcp27)} through par 27 / {int(hdcp32)} through par 32 / {int(hdcp36)} through par 36 / {int(hdcp72)} through par 72")


# Season & player stats
if is_season:
    create_season_strokes(player_strokes_cumulative, player_h_strokes_cumulative)
    create_season_par(player_par_cumulative, player_h_par_cumulative)
    create_season_skins(player_skins_cumulative)
create_strokes_box_plot(list(player_par.keys()), list(player_par.values()))
create_games_box_plot(list(player_games.keys()), list(player_games.values()))

create_pie_par(hole_par)

# Course stats
if is_scaled_to_lowest_handicap:
    create_course_par(course_h_par)
    create_hole_par(hole_h_par)
else:
    create_course_par(course_par)
    create_hole_par(hole_par)