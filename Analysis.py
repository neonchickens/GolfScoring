
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


folder_output = "Output/"
colors = ["red", "orange", "green", "blue", "purple"]


def create_strokes_box_plot(keys, data):
    fig, ax1 = plt.subplots(figsize=(6, 4))
    fig.canvas.manager.set_window_title('Par Per Hole')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=False, sym='+', orientation='vertical', whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                alpha=0.5)

    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title='Comparison of par per hole distributions',
        xlabel='Distribution',
        ylabel='Value',
    )

    # Now fill the boxes with desired colors
    num_boxes = len(data)
    medians = np.empty(num_boxes)
    for i in range(num_boxes):
        box = bp['boxes'][i]
        box_x = []
        box_y = []
        for j in range(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = np.column_stack([box_x, box_y])
        
        ax1.add_patch(Polygon(box_coords, facecolor=colors[i % 6]))
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        median_x = []
        median_y = []
        for j in range(2):
            median_x.append(med.get_xdata()[j])
            median_y.append(med.get_ydata()[j])
            ax1.plot(median_x, median_y, 'k')
        medians[i] = median_y[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot(np.average(med.get_xdata()), np.average(data[i]),
                color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.75, num_boxes + 0.25)
    top = 6
    bottom = -2
    ax1.set_ylim(bottom, top)
    ax1.set_xticklabels(keys)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(num_boxes) + 1
    upper_labels = [str(round(s, 2)) for s in medians]
    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        ax1.text(pos[tick], .95, upper_labels[tick],
                transform=ax1.get_xaxis_transform(),
                horizontalalignment='center', color=colors[tick])

    plt.savefig(f'{folder_output}par_per_hole.png')
    plt.show()


def create_games_box_plot(keys, data):
    fig, ax1 = plt.subplots(figsize=(6, 4))
    fig.canvas.manager.set_window_title('Strokes Per Game')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=False, sym='+', orientation='vertical', whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                alpha=0.5)

    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title='Comparison of strokes per game distributions',
        xlabel='Distribution',
        ylabel='Value',
    )

    # Now fill the boxes with desired colors
    num_boxes = len(data)
    medians = np.empty(num_boxes)
    for i in range(num_boxes):
        box = bp['boxes'][i]
        box_x = []
        box_y = []
        for j in range(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = np.column_stack([box_x, box_y])
        
        ax1.add_patch(Polygon(box_coords, facecolor=colors[i % 6]))
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        median_x = []
        median_y = []
        for j in range(2):
            median_x.append(med.get_xdata()[j])
            median_y.append(med.get_ydata()[j])
            ax1.plot(median_x, median_y, 'k')
        medians[i] = median_y[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot(np.average(med.get_xdata()), np.average(data[i]),
                color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.75, num_boxes + 0.25)
    top = 63
    bottom = 18
    ax1.set_ylim(bottom, top)
    ax1.set_xticklabels(keys)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(num_boxes) + 1
    upper_labels = [str(round(s, 2)) for s in medians]
    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        ax1.text(pos[tick], .95, upper_labels[tick],
                transform=ax1.get_xaxis_transform(),
                horizontalalignment='center', color=colors[tick])

    plt.savefig(f'{folder_output}strokes_per_game.png')
    plt.show()


def create_season_strokes(data, data_cumulative):
    index_color = 0
    for key in data:
        count_games = len(data[key]) // 9
        plt.plot(data[key], label=key, color=colors[index_color])
        plt.plot(data_cumulative[key], label=f"{key}_h", linestyle='dashed', color=colors[index_color])
        index_color += 1
    plt.title("Strokes Over Season")
    plt.xlabel("Season Hole #")
    plt.ylabel("Total Strokes")
    plt.legend(loc="upper left")
    plt.xticks(range(0, 9 * count_games + 1, 9), range(0, 9 * count_games + 1, 9))
    plt.grid()
    plt.savefig(f'{folder_output}strokes_over_season.png')
    plt.show()


def create_season_skins(data):
    index_color = 0
    for key in data:
        count_games = len(data[key]) // 9
        plt.plot(data[key], label=key, color=colors[index_color])
        index_color += 1
    plt.title("Skins Over Season")
    plt.xlabel("Season Hole #")
    plt.ylabel("Total Skins")
    plt.legend(loc="upper left")
    plt.yticks(range(0, 9 * count_games // 2, 3), range(0, 9 * count_games // 2, 3))
    plt.xticks(range(0, 9 * count_games + 1, 9), range(0, 9 * count_games + 1, 9))
    plt.grid()
    plt.savefig(f'{folder_output}skins_over_season.png')
    plt.show()


def create_season_par(data, data_cumulative):
    index_color = 0
    for key in data:
        count_games = len(data[key]) // 9
        plt.plot(data[key], label=key, color=colors[index_color])
        plt.plot(data_cumulative[key], label=f"{key}_h", linestyle='dashed', color=colors[index_color])
        index_color += 1
    plt.title("Par Over Season")
    plt.xlabel("Season Hole #")
    plt.ylabel("Total Par +/-")
    plt.legend(loc="upper left")
    plt.xticks(range(0, 9 * count_games + 1, 9), range(0, 9 * count_games + 1, 9))
    plt.grid()
    plt.savefig(f'{folder_output}par_over_season.png')
    plt.show()


def avg(lst):
    return sum(lst)/len(lst)


def create_course_par(data):
    plt.bar(list(data.keys()), list(map(avg, data.values())))
    plt.title('Course par')
    plt.xlabel('Course')
    plt.ylabel('Par')
    plt.xticks(rotation=90)
    plt.show()


def create_hole_par(data):
    plt.bar(list(data.keys()), list(map(avg, data.values())))
    plt.title('Hole par')
    plt.xlabel('Hole')
    plt.ylabel('Par')
    plt.xticks(rotation=90)
    plt.show()



def GetVerbiageForNumber(num):
    if num < 2:
        return ""
    if num == 2:
        return "Double"
    if num == 3:
        return "Triple"
    if num == 4:
        return "Quadrouple"
    if num == 5:
        return "Quintouple"
    
def GetSlangForParDifferential(par, strokes):
    if strokes == 1:
        return "Hole in One"
    diff = strokes - par
    if diff == 0:
        return "Par"
    if diff >= 1:
        return f"{GetVerbiageForNumber(diff)} Bogey"
    if diff == -1:
        return "Birdie"
    if diff == -2:
        return "Eagle"
    if diff == -3:
        return "Albatross"
    
    
def create_pie_par(data):
    all_holes_par = [x for xs in data for x in data[xs]]
    x_data = []
    y_data = []
    x_data.append(len([x for x in all_holes_par if x <= -3]))
    y_data.append(f"<={GetSlangForParDifferential(4, 4 - 3)}")
    for i in range(-2, 5):
        x_data.append(len([x for x in all_holes_par if x == i]))
        y_data.append(f"{GetSlangForParDifferential(4, 4 + i)}")
    x_data.append(len([x for x in all_holes_par if x >= 5]))
    y_data.append(f">={GetSlangForParDifferential(4, 4 + 5)}")

    for i in range(len(x_data)):
        x = x_data[i]
        percent = x / sum(x_data)
        y_data[i] += f" {x} or {100*percent:.1f}%"
    plt.pie(x_data, labels = y_data)
    plt.show() 