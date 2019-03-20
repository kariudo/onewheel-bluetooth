# Onewheel Blue
A python bluetooth data reader/writer for the Onewheel (supporting Gemini firmware).
This is a prototype for reading stats and modifying characteristics of the OneWheel.

Ensure that you have pygatt and it's dependacies are properly installed.

## Usage

Just run it with your board's MAC address as the last paramater:

```
python3 alpha.py [some command line options] XX:XX:XX:XX:XX:XX
```

## Help
```
python3 alpha.py -h
or
python3 alpha.py --help
--------------------------------------------------------------------------
usage: alpha_1.py [-h] [-ww | -p | -s] [-lo | -ld | -cl] [-bi] [-cs] [-ls]
                  [-v]
                  device

positional arguments:
  device                bluetooth address of the Onewheel to connect to

optional arguments:
  -h, --help            show this help message and exit
  -ww, --weewoo         Activate ambulance mode
  -p, --phase           Phase between red and white
  -s, --speed           Constantly output speed in mph
  -lo, --lights-off     Turns both lights off
  -ld, --lights-default Turns lights to default mode
  -cl, --customlight    Custom light prompt
  -bi, --board-info     Read out board information
  -cs, --custom-shape   Custom shape prompt
  -ls, --live-statistics Read out of board statistics
  -v, --verbose         increase output verbosity

```
## Tips

-This tool will not work if you are currently connected to your board with the phone app
-Make sure you have the dependencies install and are using python 3

## Goals

-Make all of the characteristics subscription based that can be so reduce board reads
-Log to a file
-gyro output
-maybe gps logging

### Credits
Thanks to [@beeradmoore](https://github.com/beeradmoore) for figuring out the md5 chunks for the serial stream reasponse via the ponewheel issue: https://github.com/ponewheel/android-ponewheel/issues/86#issuecomment-440809066
