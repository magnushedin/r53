import sys
import time

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

signal_name = {'4': 'Calc_Load',
               '5': 'ECT',
               'a': 'Fuel_Press',
               'b': 'Intk_Mani_Press',
               'c': 'RPM',
               'd': 'Speed',
               'e': 'Ign_Adv',
               'f': 'Intk_Air_Temp',
               '10': 'MAF',
               '11': 'TPS',
               '14': 'Lambda',
               '2f': 'Fuel_Tank_Level',
               '33': 'Absolute_Barometric_Pressure',
               '43': 'Absolute_Load_Value',
               '46': 'Ambient_Air_Temperature',
               '5c': 'Engine_Oil_Temperature',
               '5e': 'Engine_Fuel_Rate',
               'ee': 'CAC_LoadTeDiff',
               'ef': 'CAC_Efficiency',
               'fc': 'CAC_LoadTeBe',
               'fd': 'CAC_LoadTeAf',
               'fe': 'CAC_CoolTeBe',
               'ff': 'CAC_CoolTeAf'}


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


def plot_measurments(data):

    print(data.keys())

    # Calculate signals
    #data['ee'] = np.column_stack((data['fc'][:, 0], data['fc'][:, 1] - data['fd'][:, 1]))  # Temperature diff over CAC
    #data['ef'] = np.column_stack((data['fc'][:, 0], data['ee'][:, 1] / (data['fc'][:, 1] - data['fe'][:, 1])))  # CAC efficiency
    # Gear ratio
    # Filter for WOT

    # Plot data
    #plot_data_subplot(data)  # all data

    signals = ['f', '11', 'b', 'c', 'd', 'e']
    plot_data(data, signals)

    signals = ['ef', 'c']
    #plot_data(data, signals, sameaxis=False)

    # int mani press, eng speed, temperature
    signals = ['c', 'fc', 'b']
    #plot_data(data, signals, sameaxis=False)

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

def save_as_octave(data, filename):
    f = open(filename, 'w')
    f.write('''
# name: data
# type: scalar struct
# ndims: 2
 1 1
# length: {signal_count}'''.format(signal_count=len(data.keys())))

    for signal in data:
        data_string = ""
        data_length = 0
        signal_id = signal
        for d in data[signal_id][:,1]:
            data_string = data_string + " " + str(d)
            data_length += 1
        f.write(
'''
# name: {signal_name}
# type: matrix
# rows: 1
# columns: {data_length}
'''.format(signal_name = signal_name[signal_id], data_length = data_length)
        )
        f.write("{}\n\n".format(data_string))
    f.close()



if __name__ == '__main__':
    filename_obd = '20190806_1409_m.log'
    data = read_data_obd(filename_obd)
    #plot_measurments(data)
    save_as_octave(data, '../octave/oem_ignition_mapping')
