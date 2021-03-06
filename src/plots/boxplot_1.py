import sys
import matplotlib


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon

show_plot = False
cols = ["dataset", "period", "clf", "magic", "model_params", "k", "bot_thresh",
        "top_thresh", "mode", "trade_frequency", "start_trade", "final_trade",
        "time", "min", "max", "mean", "last"]



def add_legend(fig):

    # Finally, add a basic legend
    fig.text(0.8005, 0.115, '-', color='red', backgroundcolor='silver',
             weight='roman', size='medium')
    fig.text(0.817, 0.115, ' S&P 500 Index returns', color='black',
             weight='roman',
             size='x-small')

    fig.text(0.8005, 0.165, '*', color='white', backgroundcolor='silver',
             weight='roman', size='medium')
    fig.text(0.815, 0.165, ' Average Value', color='black', weight='roman',
             size='x-small')

def plot_by_model(results):
    # plot by model
    models = ['graham', 'SVC', 'RFC', 'MLPC', 'AdaBC']
    data = [results[results.clf == clf]['last'].values / 1000000.0 for clf in models]

    model_names = ['Graham', 'SVM', 'Random Forest', 'Neural Network',
                   'AdaBoost']

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('Revenues per model')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=0, sym='+', vert=1, whis=1.5, meanline=False)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    plt.setp(bp['medians'], color='black')


    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
    # ax1.get_yaxis().set_major_formatter(
    #     # matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title('Comparison of total revenues for different models')
    ax1.set_xlabel('Models')
    ax1.set_ylabel('Total revenue in million U.S. dollars')

    ax1.axhline(y=276480 / 1000000.0, color='red', linestyle='--', alpha=0.4)
    
    # Now fill the boxes with desired colors
    boxColors = ['royalblue', 'royalblue']
    numBoxes = len(data)
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        k = i % 2
        boxCoords = np.column_stack([boxX, boxY])
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            # ax1.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes + 0.5)
    top = max([max(x) for x in data if len(x) > 0]) * 1.1
    bottom = 0
    ax1.set_ylim(bottom, top)
    # ax1.set_xticks([1, 2, 3.5, 3.5, 5.5, 5.5, 7.5, 7.5, 9.5, 9.5])
    ax1.set_xticklabels(model_names, fontsize=10)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
                 horizontalalignment='center', size='x-small',
                 weight=weights[k],
                 color=boxColors[k])

    # Finally, add a basic legend
    # fig.text(0.80, 0.12, 'Classification',
    #          backgroundcolor=boxColors[0], color='black', weight='roman',
    #          size='x-small')
    # fig.text(0.80, 0.09, 'Regression',
    #          backgroundcolor=boxColors[1],
    #          color='white', weight='roman', size='x-small')
    # fig.text(0.8005, 0.135, ' ', color='white', backgroundcolor=boxColors[0],
    #          weight='roman', size='medium')
    # fig.text(0.81, 0.135, ' Classification models', color='black', weight='roman',
    #          size='x-small')
    #
    # fig.text(0.8005, 0.09, ' ', backgroundcolor=boxColors[1],
    #          weight='roman', size='medium')
    # fig.text(0.81, 0.09, ' Regression models', color='black', weight='roman',
    #          size='x-small')

    add_legend(fig)
    plt.savefig('models', bbox_inches='tight')
    if show_plot:
        plt.show()


def plot_by_dataset(results):
    # plot by dataset
    datasets = ['normal', 'z-score']
    data = [results[results.dataset.str.contains(dataset)]['last'].values /1e6 for
            dataset in datasets]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('Revenues per scaling')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    plt.setp(bp['medians'], color='black')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title('Comparison of total revenues for different scaling methods')
    # ax1.set_xlabel('')
    ax1.set_ylabel('Total revenue in million U.S. dollars')
    ax1.axhline(y=276480 / 1e6, color='red', linestyle='--', alpha=0.4)
    # ax1.get_yaxis().set_major_formatter(
        # matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Now fill the boxes with desired colors
    boxColors = ['royalblue', 'royalblue']
    numBoxes = len(data)
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        k = i % 2
        boxCoords = np.column_stack([boxX, boxY])
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            # ax1.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes + 0.5)
    top = max([max(x) for x in data if len(x) > 0]) * 1.1
    bottom = 0
    ax1.set_ylim(bottom, top)
    # ax1.set_xticks([1, 2, 3.5, 3.5, 5.5, 5.5, 7.5, 7.5, 9.5, 9.5])
    ax1.set_xticklabels(datasets, fontsize=10)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
                 horizontalalignment='center', size='x-small',
                 weight=weights[k],
                 color=boxColors[k])

    # Finally, add a basic legend
    add_legend(fig)
    plt.savefig('datasets', bbox_inches='tight')
    if show_plot:
        plt.show()


def plot_by_frequency(results):
    # plot by dataset
    freqs = [4, 12, 26, 52]
    freqs = [26, 52]
    data = [results[results.trade_frequency == freq]['last'].values /1e6 for
            freq in freqs]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('Revenues per frequency')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    plt.setp(bp['medians'], color='black')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title(
        'Comparison of total revenues for different trade frequencies')
    ax1.set_xlabel('Trade frequency (weeks)')
    ax1.set_ylabel('Total revenue in million U.S. dollars')
    ax1.axhline(y=276480 / 1e6, color='red', linestyle='--', alpha=0.4)
    # ax1.get_yaxis().set_major_formatter(
        # matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Now fill the boxes with desired colors
    boxColors = ['royalblue']
    numBoxes = len(data)
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        k = 0
        boxCoords = np.column_stack([boxX, boxY])
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            # ax1.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes + 0.5)
    top = max([max(x) for x in data if len(x) > 0]) * 1.1
    bottom = 0
    ax1.set_ylim(bottom, top)
    # ax1.set_xticks([1, 2, 3.5, 3.5, 5.5, 5.5, 7.5, 7.5, 9.5, 9.5])
    ax1.set_xticklabels(freqs, fontsize=10)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = 0
        ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
                 horizontalalignment='center', size='x-small',
                 weight=weights[k],
                 color=boxColors[k])

    # Finally, add a basic legend
    add_legend(fig)
    plt.savefig('frequency', bbox_inches='tight')
    if show_plot:
        plt.show()


def plot_by_training(results):
    # plot by dataset
    freqs = [53, 105]
    data = [results[results.magic == mn]['last'].values /1e6 for
            mn in freqs]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('Revenues per training size')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    plt.setp(bp['medians'], color='black')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title(
        'Comparison of total revenues for different training data periods')
    ax1.set_xlabel('Length of data used for training')
    ax1.set_ylabel('Total revenue in million U.S. dollars')
    ax1.axhline(y=276480 / 1e6, color='red', linestyle='--', alpha=0.4)
    # ax1.get_yaxis().set_major_formatter(
        # matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Now fill the boxes with desired colors
    boxColors = ['royalblue']
    numBoxes = len(data)
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        k = 0
        boxCoords = np.column_stack([boxX, boxY])
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            # ax1.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes + 0.5)
    top = max([max(x) for x in data if len(x) > 0]) * 1.1
    bottom = 0
    ax1.set_ylim(bottom, top)
    # ax1.set_xticks([1, 2, 3.5, 3.5, 5.5, 5.5, 7.5, 7.5, 9.5, 9.5])
    ax1.set_xticklabels(['1 year', '2 years'], fontsize=10)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = 0
        ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
                 horizontalalignment='center', size='x-small',
                 weight=weights[k],
                 color=boxColors[k])

    # Finally, add a basic legend
    add_legend(fig)
    plt.savefig('training', bbox_inches='tight')
    if show_plot:
        plt.show()


def plot_by_threshold(results):
    # plot by dataset

    thresholds_list = [(-np.inf, 0), (-np.inf, 0.005), (-np.inf, 0.01),
                       (-np.inf, 0.015),
                       (-np.inf, 0.02), (-np.inf, 0.025), (-np.inf, 0.03)]
    thresholds_names = [0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]

    data = [results[(results.top_thresh == t) & (results.bot_thresh == b)][
                'last'].values /1e6 for
            b, t in thresholds_list]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('Revenues per threshold')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    plt.setp(bp['medians'], color='black')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title('Comparison of total revenues for thresholds')
    ax1.set_xlabel('Top threshold')
    ax1.set_ylabel('Total revenue in million U.S. dollars')
    ax1.axhline(y=276480 / 1e6, color='red', linestyle='--', alpha=0.4)
    # ax1.get_yaxis().set_major_formatter(
        # matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Now fill the boxes with desired colors
    boxColors = ['royalblue']
    numBoxes = len(data)
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        k = 0
        boxCoords = np.column_stack([boxX, boxY])
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            # ax1.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes + 0.5)
    top = max([max(x) for x in data if len(x) > 0]) * 1.1
    bottom = 0
    ax1.set_ylim(bottom, top)
    # ax1.set_xticks([1, 2, 3.5, 3.5, 5.5, 5.5, 7.5, 7.5, 9.5, 9.5])
    ax1.set_xticklabels(thresholds_names, fontsize=10)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = 0
        ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
                 horizontalalignment='center', size='x-small',
                 weight=weights[k],
                 color=boxColors[k])

    # Finally, add a basic legend
    add_legend(fig)
    plt.savefig('thresholds', bbox_inches='tight')
    if show_plot:
        plt.show()


def plot_by_mode(results):
    # plot by dataset
    modes = ['sell_all', 'avoid_fees']
    # import ipdb
    # ipdb.set_trace()
    data = [results[results['mode'] == m]['last'].values /1e6 for m in modes]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('Revenues for different trading strategies')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    plt.setp(bp['medians'], color='black')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title('Comparison of total revenues for different strategies')
    ax1.set_xlabel('Strategy')
    ax1.set_ylabel('Total revenue in million U.S. dollars')
    ax1.axhline(y=276480 / 1e6, color='red', linestyle='--', alpha=0.4)
    # ax1.get_yaxis().set_major_formatter(
        # matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Now fill the boxes with desired colors
    boxColors = ['royalblue']
    numBoxes = len(data)
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        k = 0
        boxCoords = np.column_stack([boxX, boxY])
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            # ax1.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        ax1.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes + 0.5)
    top = max([max(x) for x in data if len(x) > 0]) * 1.1
    bottom = 0
    ax1.set_ylim(bottom, top)
    # ax1.set_xticks([1, 2, 3.5, 3.5, 5.5, 5.5, 7.5, 7.5, 9.5, 9.5])
    ax1.set_xticklabels(['sell/buy all', 'avoid fees'], fontsize=10)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = 0
        ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
                 horizontalalignment='center', size='x-small',
                 weight=weights[k],
                 color=boxColors[k])

    # Finally, add a basic legend
    add_legend(fig)
    plt.savefig('modes', bbox_inches='tight')
    if show_plot:
        plt.show()



if __name__ == '__main__':
    print("Loading ../../results/res1.csv" )

    results = pd.read_csv('../../results/res1.csv', names=cols).sort_values(
        'last').drop(
        'time', 1).drop_duplicates()

    # r = r[(r.clf == 'AdaBC') | (r.clf == 'MLPC') | (r.clf == 'RFC') | (r.clf == 'SVC') | (r.clf == 'graham')]

    # results = r[(r.trade_frequency == 52) | (r.trade_frequency == 26)]

    plot_by_model(results)
    plot_by_dataset(results)
    plot_by_frequency(results)
    plot_by_training(results)
    plot_by_threshold(results)
    plot_by_mode(results)
    plot_by_trade(results)
