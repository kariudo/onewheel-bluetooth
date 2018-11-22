# onewheel-bluetooth
A python bluetooth data reader for the Onewheel (supporting Gemini firmware).
This is meant to be a quick and dirty example of how to connect and obtain data from the board.

## Usage

Just run it with your board's address as the first paramater:

```
python3 readdata.py XX:XX:XX:XX:XX:XX
```

You should get output like the following:

```
Requesting encryption key...
Waiting for encryption key...
Sending unlock key...
Reading Onewheel status:
Battery Remaining: 100%
Lifetime Odometer: 57 Miles
Trip Odometer: 0 Miles
```
