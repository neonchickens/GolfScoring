
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np



colors = ["red", "orange", "green", "blue", "purple"]


def create_box_plot(keys, data):
    fig, ax1 = plt.subplots(figsize=(6, 4))
    fig.canvas.manager.set_window_title('Strokes Per Hole')
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
        title='Comparison of strokes per hole distributions',
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
    top = 9
    bottom = 1
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
    plt.xticks(range(0, 9 * count_games + 1, 9), range(0, 9 * count_games + 1, 9))
    plt.grid()
    plt.show()
