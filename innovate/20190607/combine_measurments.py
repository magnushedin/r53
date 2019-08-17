import sys
import time

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

signal_name = {'4': 'Calc Load',
               '5': 'ECT',
               'a': 'Fuel Press',
               'b': 'Intk Mani Press',
               'c': 'RPM',
               'd': 'Speed',
               'e': 'Ign Adv',
               'f': 'Intk Air Temp',
               '10': 'MAF',
               '11': 'TPS',
               '14': 'Lambda',
               '2f': 'Fuel Tank Level',
               '33': 'Absolute Barometric Pressure',
               '43': 'Absolute Load Value',
               '46': 'Ambient Air Temperature',
               '5c': 'Engine Oil Temperature',
               '5e': 'Engine Fuel Rate',
               'ee': 'CAC LoadTeDiff',
               'ef': 'CAC Efficiency',
               'fc': 'CAC LoadTeBe',
               'fd': 'CAC LoadTeAf',
               'fe': 'CAC CoolTeBe',
               'ff': 'CAC CoolTeAf'}


def read_data_obd(filename):
    # Dictionary with signal id as key and np.array with data as value
    data = dict()
    try:
        f = open(filename, 'r')

        for lines in f:
            # print("Reading data")
            serial_data = lines.rstrip('\n')
            parsed_data = serial_data.split(',')
            signal_id = parsed_data[0]
            signal_time = parsed_data[1]
            signal_data = parsed_data[2].rstrip('\n')
            # print("Read_data: " + signal_id + "," + signal_time + "," +
            #      signal_data)
            if not(signal_id in data):
                # print("New signal discovered: {}".format(signal_id))
                data[signal_id] = np.array([[float(signal_time),
                                            float(signal_data)]])
            else:
                data[signal_id] = np.vstack((data[signal_id],
                                            np.array([float(signal_time),
                                                     float(signal_data)])))
        return data

    except IOError:
        print('Could not open file: {}'.format(filename))

def read_data_innovate(filename):
    try:
        f = open(filename, 'r')
    except IOError:
        print('Could not open file: {}'.format(filename))
    
    data = dict()
    signals = ['fc', 'fd', 'fe', 'ff']
    for i, lines in enumerate(f):
        if (i > 2):
            # print('{}: {}'.format(i, lines), end='')
            serial_data = lines.rstrip('\n')
            parsed_data = serial_data.split(',')
            signal_time = parsed_data[0]  # time
            for signal_count, signal_id in enumerate(signals):
                if (signal_id not in data):
                    data[signal_id] = np.array([float(signal_time), float(parsed_data[signal_count+1])])
                else:
                    data[signal_id] = np.vstack((data[signal_id], np.array([float(signal_time), float(parsed_data[signal_count+1])])))
    return data


def plot_data_subplot(data):
    temp_signals = ['f', 'ff', 'fe', 'fd', 'fc', 'ef']
    colors = ['-r', '-b', '-k', '-m', '-y', '-g']

    nbr_of_signals = len(data.keys()) - len(temp_signals) + 1
    fig, axarr = plt.subplots(nbr_of_signals, sharex=True)
    
    counter = 1
    temp_signal_count = 0

    for signal_id in data.keys():
        xs = data[signal_id][:, 0]
        ys = data[signal_id][:, 1]
        
        if signal_id in temp_signals:
            axarr[0].plot(xs, ys, colors[temp_signal_count], label=signal_name[signal_id])
            temp_signal_count += 1
        else:
            axarr[counter].clear()
            axarr[counter].plot(xs, ys, '-*')
            axarr[counter].set_ylabel(signal_name[signal_id],
                                    rotation=90)
            axarr[counter].set_title('[0x' + signal_id + '] = ' +
                                    signal_name[signal_id] + ', ' +
                                    str(ys[-1]))
            counter += 1

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.show()


def plot_data_oneplot(data):
    fig, ax = plt.subplots(1, sharex=True)
    colors = ['-r', '-b', '-k', '-m', '-y', '-g']
    for signal_count, signal_id in enumerate(data.keys()):
        xs = data[signal_id][:, 0]
        ys = data[signal_id][:, 1]
        # ax = axarr.twinx()
        ax.plot(xs, ys, colors[signal_count], label=signal_name[signal_id])

    # Format plot
    ax.legend()
    plt.show()


def plot_data(data, signals, sameaxis=True):
    fig, ax = plt.subplots(1, sharex=True)
    axarr = [ax]
    colors = ['-r', '-b', '-k', '-m', '-y', '-g']
    signal_count = 0
    axis_count = 0
    for signal_id in data.keys():
        if signal_id in signals:
            xs = data[signal_id][:, 0]
            ys = data[signal_id][:, 1]
            axarr[axis_count].plot(xs, ys, colors[signal_count], label=signal_name[signal_id])
            axarr[axis_count].legend()
            signal_count += 1
            if not sameaxis:
                axis_count += 1
                axarr.append(ax.twinx())

    # Format plot
    plt.show()


def plot_data_sfa(data, xsignal, signals, sameaxis=True):

    # TODO: Signals need to have the same x-axis for this to work.

    '''
    Take one axis to have as base. Interpolate the second signal to this axis. Need to take the longest x-axis?
    '''

    fig, ax = plt.subplots(1, sharex=True)
    axarr = [ax]
    colors = ['-r', '-b', '-k', '-m', '-y', '-g']
    signal_count = 0
    axis_count = 0
    for signal_id in data.keys():
        if signal_id in signals:
            xs = data[xsignal][:, 0]
            ys = data[signal_id][:, 1]
            axarr[axis_count].plot(
                xs, ys, colors[signal_count], label=signal_name[signal_id])
            axarr[axis_count].legend()
            signal_count += 1
            if not sameaxis:
                axis_count += 1
                axarr.append(ax.twinx())

    # Format plot
    plt.show()


def data2datazap_csv(data):
    # csv_data = np.empty(shape=[len(data['c']), len(signal_plot.keys())])
    print_string = ""
    for signal_id in data.keys():
        print_string += "{};".format(signal_name[signal_id])
    print(print_string.rstrip(';'))

    for ii in range(len(data['c'])):
        print_string = ""
        for signal_id in data.keys():
            try:
                print_string += "{};".format(data[signal_id][ii, 1])
            except:
                print_string += "0;"
        print(print_string.rstrip(';'))


def combine_data(data_obd, data_innovate):
    for key in data_obd.keys():
        for i, t in enumerate(data_obd[key][:, 0]):
            data_obd[key][i, 0] = (t/1000) - 106
    data = {**data_obd, **data_innovate}
    
    return data


def calc_diff(data1, data2):
    diff = data1[:, 1] - data2[:, 1]
    # print(diff)
    data = np.array([data1[:, 0], data1[:, 1]])
    print(data)
    return data1


def plot_measurments():
    # Load data
    filename_obd = '20190607_0120.log'
    filename_innovate = 'session2.csv'
    data_obd = read_data_obd(filename_obd)
    data_innovate = read_data_innovate(filename_innovate)
    data = combine_data(data_obd, data_innovate)

    # Calculate signals
    data['ee'] = np.column_stack((data['fc'][:, 0], data['fc'][:, 1] - data['fd'][:, 1]))  # Temperature diff over CAC
    data['ef'] = np.column_stack((data['fc'][:, 0], data['ee'][:, 1] / (data['fc'][:, 1] - data['fe'][:, 1])))  # CAC efficiency
    # Gear ratio
    # Filter for WOT

    # Plot data
    plot_data_subplot(data)  # all data

    signals = ['f', 'ff', 'fe', 'fd', 'fc', 'ee']
    plot_data(data, signals)

    signals = ['ef', 'c']
    plot_data(data, signals, sameaxis=False)

    # int mani press, eng speed, temperature
    signals = ['c', 'fc', 'b']
    plot_data(data, signals, sameaxis=False)

    # intk mani press sfa eng speed
    signals = ['d']
    # plot_data_sfa(data, 'c', signals)

    # intk mani press sfa eng speed and tempterature (3D)

    # temperature sfa veh speed
    # temperature sfa eng speed
    # temperature sfa eng speed and veh speed (3D)
    # CAC efficiency sfa engine speed (and intake manifold pressure)

    # data2datazap_csv(data)


def calculate_stint_times():
    pass
    # Calculate acceleration times for various stint ranges
    # Use filters for gears used


if __name__ == '__main__':
    plot_measurments()
    calculate_stint_times()
