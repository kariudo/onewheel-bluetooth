import logging
import asyncio
from argparse import ArgumentParser
from onewheel import Onewheel, scan_for_onewheel
from time import sleep

loop_delay = 1  # seconds between refreshed data
max_failures = 5  # number of times in a row to retry when bad data is received


async def load_cli_configuration():
    """configure CLI arguments and return the device address."""

    # Parse out the commandline arguments.
    parser = ArgumentParser()
    parser.add_argument("device", type=str, nargs='?',
                        help="bluetooth address of the Onewheel to connect to")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="display debug level logging")
    parser.add_argument("-s", "--scan", action="store_true",
                        help="attempt to detect the identifier of a visible onewheel")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG if args.verbose else logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    ow_mac: str

    if args.scan:
        # If scan, then find the first onewheel in range.
        try:
            ow_mac = await scan_for_onewheel()
        except Exception as e:
            logging.error(e)
            quit(4)
    else:
        # Otherwise, use the onewheel MAC address the user provides.
        ow_mac = args.device
    if not ow_mac:
        # If nothing was provided, complain to the user.
        logging.error(
            "You must provide a device MAC address, or use --scan mode. See --help for options.")
        quit(3)
    return ow_mac


async def main():
    address = await load_cli_configuration()
    onewheel = Onewheel(address)
    if await onewheel.connect():
        try:
            logging.info(f"Connected to board: {onewheel.name}")
            retry = max_failures
            while True:
                if not onewheel.client.is_connected:
                    logging.warning("Not connected, exiting loop")
                    break
                batt = await onewheel.batt_percentage()
                # exit if we aren't getting valid data.
                if batt == 0:
                    if retry > 0:
                        retry -= 1
                        logging.warning(
                            "Unable to read valid data, retrying in 3 sec...")
                        sleep(3)
                        continue
                    else:
                        raise Exception(
                            "Unable able to read valid data, after 5 failed attempts. Exiting.")

                logging.info("Battery : [%-20s] %d%%" %
                             ('='*int(batt/5), batt))
                logging.info(f"Trip    : {await onewheel.tripmeter()} mi")
                logging.info(f"Odometer: {await onewheel.odometer()} mi")

                retry = max_failures  # reset retry count on success
                sleep(loop_delay)  # wait before refreshing
        except KeyboardInterrupt:
            logging.warning(
                "Keyboard interrupt received. Disconnecting and exiting.")
        except Exception as e:
            logging.error(e)
        finally:
            await onewheel.disconnect()
            quit(0)
    else:
        logging.warning("Cannot read data, not connected")

if __name__ == "__main__":
    asyncio.run(main())
