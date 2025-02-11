#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Based on https://github.com/MathieuSchopfer/tfa-airco2ntrol-mini by Mathieu Schopfer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
from datetime import datetime
import os
import os.path
from matplotlib import pyplot as plt
import numpy as np
import airco2ntrol_mini as aco2m
plt.tight_layout(pad=1)
_co2_line = None
_last_point = None
#_plot_range = 1800  # Plot range in seconds
_plot_range = 86400  # Plot range in seconds
_warning_threshold = 600
_danger_threshold = 800

parser = argparse.ArgumentParser(description='Measure and log a CO2')
parser.add_argument('--prefix', type=str, help='file name prefix, default `airco2ntrol`', default='airco2ntrol')
parser.add_argument('--dir', type=str, help='log file output directory', default='logs')
args = parser.parse_args()


def _format_axis_time(t, pos=None):
    return datetime.fromtimestamp(t).time().isoformat(timespec='minutes')


def update_plot(t, co2, _):
    timestamps = np.append(_co2_line.get_xdata(), t)
    co2s = np.append(_co2_line.get_ydata(), co2)

    # Remove data out of plot time range
    k = np.flatnonzero(timestamps[-1]-timestamps < _plot_range)
    timestamps = timestamps[k]
    co2s = co2s[k]

    xsup = timestamps[0]+_plot_range if timestamps[-1]-timestamps[0] < _plot_range else timestamps[-1]
    plt.xlim(timestamps[0], xsup)

    ymax_default = 1000
    co2max = np.max(co2s)
    ysup = ymax_default if co2max < ymax_default-150 else co2max+150
    plt.ylim(300, ysup)

    _co2_line.set_xdata(timestamps)
    _co2_line.set_ydata(co2s)

    _last_point.set_xdata([t])
    _last_point.set_ydata([co2])

    fig = plt.gcf()
    fig.set_size_inches(20, 6)
    fig.canvas.draw()
    fig.savefig('co2.png')
    fig.canvas.flush_events()


if __name__ == '__main__':

    try:
        aco2m.open_device()
    except OSError as e:
        print('Could not open the device, check that it is correctly plugged:', e)
    else:
        # Create output directory
        odir = os.path.expanduser(args.dir)
        if not os.path.exists(odir):
            os.mkdir(odir)

        # Create log file
        timestamp = datetime.now().isoformat(timespec='seconds')
        filePath = os.path.join(odir, f'{args.prefix}_{timestamp}.csv')
        with open(filePath, 'at', encoding='UTF-8', errors='replace', buffering = 1) as logFile:

            # CSV logging
            def logger(t, co2, temperature):

                _t = datetime.fromtimestamp(t)

                # Log to file
                timestamp = _t.isoformat(timespec='seconds')
                logFile.write(f'{timestamp:s},{co2:.0f},{temperature:.1f}\n')

                # Console output
                timestamp = _t.time().isoformat(timespec='seconds')
                print(f'{timestamp:s}\t{co2:.0f} ppm\t\t{temperature:.1f} °C', end='\r')

            aco2m.register_watcher(logger)

            logFile.write('Time,CO2[ppm],Temperature[°C]\n')
            print('Time\t\tCO2\t\tTemperature')

            # Plotting
            aco2m.register_watcher(update_plot)
#            plt.ion()  # Activate interactive plotting
            _co2_line, = plt.plot([], [], linewidth=2, color='black')  # Init line
            _last_point, = plt.plot([], [], marker='o', color='black')  # Init line

            # Add background colours
            plt.axhspan(0, _warning_threshold, color='tab:green', alpha=0.5)
            plt.axhspan(_warning_threshold, _danger_threshold, color='tab:orange', alpha=0.5)
            plt.axhspan(_danger_threshold, 3000, color='tab:red', alpha=0.5)  # 3000 ppm is the device measurement limit

            # Customize look
            ax = plt.gca()
            ax.get_xaxis().set_major_formatter(_format_axis_time)
            plt.grid(color='whitesmoke', linestyle=':', linewidth=1)
            plt.xlabel('Time')
            plt.ylabel('CO2 [ppm]')
#            plt.title(f'CO2 concentration over {_plot_range/60:.0f} min')
            plt.title(f'CO2 concentration over the last {_plot_range/3600:.0f} hours')

            aco2m.watch(delay=30)
