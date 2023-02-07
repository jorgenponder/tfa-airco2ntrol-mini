Purpose: See https://github.com/jorgenponder/publish-co2-levels

*This repository is a fork of https://github.com/MathieuSchopfer/tfa-airco2ntrol-mini.

The differences are that this version writes the diagram to file instead of showing it in a window, with a bigger diagram (around 2000px wide), and polls slower, around every 30 seconds.*

Tested so far on an Intel NUC running Ubuntu 20.04 LTS Linux, and on a Raspberry Pi 3+ running Debian 11 Linux.

## Added file
publish.py has been added, for publishing the diagram to a Mastodon server, for example at https://botsin.space

## Example install with virtualenv and running on Debian and Ubuntu

Example install on a Raspberry Pi 3+ running Debian 11 Linux:
    
    sudo apt install python3-virtualenv
    mkdir co2
    cd co2
    git clone git@github.com:jorgenponder/tfa-airco2ntrol-mini.git
    virtualenv .
    ./bin/pip install hidapi
    ./bin/pip install matplotlib
    ./bin/pip install Mastodon.py
    ./bin/python report.py

Example cron job to publish to Mastodon every 4 hours:

    36  */4 * * * cd /path/to/tfa-airco2ntrol-mini && ./bin/python publish.py 2>&1 | logger -t mastodon

Remember to change the settings in publish.py first

# Original text follows

Cross-platform Python logger for [TFA Dostmann Airco2ntrol Mini CO2 monitor](https://www.tfa-dostmann.de/en/product/co2-monitor-airco2ntrol-mini-31-5006/) (31.5006.02) relying on HIDAPI library.

# Prerequisites

This project needs:
 * Python 3
 * [HIDAPI library](https://github.com/libusb/hidapi)
 * [hidapi Python interface](https://pypi.org/project/hidapi/)

## Linux

See what package your distribution provides for the HIDAPI library.

## macOS

The HIDAPI library may be easily installed on macOS with Homebrew:
```shell
brew install hidapi
```

# Getting stared

Just run the logger script with:
```shell
python3 report.py
```

The script will create a log file `airco2ntrol_<date>T<time>.csv` and open a plotting window.

# Troubleshooting

## udev rules on Linux
If the script cannot access the device, update your system's udev rules as follow:

 1. Unplug the device
 2. Copy file `90-airco2ntrol_mini.rules` to `/etc/udev/rules.d`
 3. Reload the rules with `sudo udevadm control --reload-rules`
 4. Plug your device.

## matplotlib on macOS

If the plotting window does not show up, you may need to configure the matplotlib backend. Edit file `~/.matplotlib/matplotlibrc` and add or edit
```
backend: TkAgg
```

Note that you need the Python Tcl/Tk interface. You can install it with
```shell
brew install python-tk
```

# Credits

Henryk Plötz was the first reverse engineer TFA Dotsmann CO2 monitors. Give a look at [his project](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor).
