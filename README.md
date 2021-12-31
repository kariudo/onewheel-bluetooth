# onewheel-bluetooth

A python bluetooth data reader for the Onewheel (supporting Gemini firmware, and later).
This is meant to be a quick example of how to connect and obtain data from the board.

The backend library for bluetooth/gatt interaction is rewritten now with `bleak` due to a deprecation/lack of ownership of `pygatt`.

## Requirements

Python 3+ is required, and the dependencies are included in the `requirements.txt`.

### Setup the environment

I suggest using a venv, espeically for development purposes:

```shell
> python3 -m venv venv
```

Then activate your venv before installing dependencies:

```shell
> source ./venv/bin/activate
```

> Note: Some of the commands vary, including the above, on Windows. For example, I think the path to the venv script in windows is `.\venv\Scripts\activate`.

Then install the required packages with `pip`:

```shell
> pip install -r requirements.txt
```

## Usage

Just run it with your board's address as the first paramater:

```shell
> python3 readdata.py XX:XX:XX:XX:XX:XX
```

You can include `-v` to get all of the verbose debug output as well.

You should get output like the following:

```shell
INFO:root:Battery Remaining: 79%
INFO:root:Lifetime Odometer: 258 Miles
INFO:root:Trip Odometer: 0 Miles
```

### Credits

Thanks to [@beeradmoore](https://github.com/beeradmoore) for the help figuring out the md5 chunks for the serial stream reasponse via the ponewheel issue: https://github.com/ponewheel/android-ponewheel/issues/86#issuecomment-440809066
