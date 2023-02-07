Purpose: To capture CO2 readings from a Dostmann mini or coach CO2 meter,and publish, currently to Mastodon

Note! This is alpha code. And alpha instructions. Tested on Ubuntu Linux.

![Example diagram](https://raw.githubusercontent.com/jorgenponder/tfa-airco2ntrol-mini/master/diagram.png)

This is how you can publish the carbon dioxide levels of your premises in order to build some trust with the people who visit them. Four steps need to be done once, no running costs. The vision is to give out a USB or memory card and it just works, but right now you have to be comfortable installing python code on a computer.

Another use case is to monitor an empty apartment or house, verifying that nothing CO2-producing and hence potentially virus producing, has been on the premises. Or monitor if CO2 is leaking into the space from e.g. neighbours.

This will be the result: https://mas.to/@koldio/109808222410697067

1. Get a TFA Dostmann CO2 meter, they cost around EUR 80 each. This meter is better than almost anything else in the price range, as it does not need to be adjusted (calibrated) once a day. Which means that it also works well in premises that are not fully ventilated every 24 hours. https://www.tfa-dostmann.de/en/product/co2-monitor-airco2ntrol-mini-31-5006/

2. Get an account on a Mastodon server, and register an application there and save the keys for the application. Some Mastodon servers are supposed to be extra bot friendly, such as this one: https://botsin.space . But that server has a delay before getting approved. However you might still be waiting for a CO2 meter. Read the rules for the server you choose before opening an account there.

3. Install the code in this repository. https://github.com/jorgenponder/tfa-airco2ntrol-mini It is a modified version of https://github.com/MathieuSchopfer/tfa-airco2ntrol-mini to provide 24 hour charts, as well as saving the diagram to disk instead of displaying it in a window. It also contains a file publish.py, that publishes to a Mastodon server very 4 hours, if you put it in a cron job that runs it every four hours.

4. Plug the meter into a computer with a USB cable.

After this, your CO2 data should be published on a Mastodon account every four hours.


**This repository is a fork of https://github.com/MathieuSchopfer/tfa-airco2ntrol-mini.

The differences are that this version writes the diagram to file instead of showing it in a window, with a bigger diagram (around 2000px wide), and polls slower, around every 30 seconds.**

Tested so far on an Intel NUC running Ubuntu 20.04 LTS Linux, and on a Raspberry Pi 3+ running Debian 11 Linux.

## Added file
publish.py has been added, for publishing the diagram to a Mastodon server, for example at https://botsin.space

## Example install with virtualenv and running on Debian and Ubuntu

Example install on a Raspberry Pi 3+ running Debian 11 Linux:
    
    sudo apt install python3-virtualenv
    mkdir co2
    cd co2
    git clone git@github.com:jorgenponder/tfa-airco2ntrol-mini.git
    cd tfa-airco2ntrol-mini
    virtualenv .
    ./bin/pip install hidapi
    ./bin/pip install matplotlib
    ./bin/pip install Mastodon.py
    # run the program to create the Co2 diagram
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
