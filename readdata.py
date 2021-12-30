import logging
import asyncio
from argparse import ArgumentParser
from bleak import BleakScanner
from onewheel import Onewheel
from time import sleep


async def load_cli_configuration():
    """ configure CLI arguments and return the device address """
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

    ow_mac = ""

    if args.scan:
        devices = await BleakScanner.discover()
        for d in devices:
            logging.debug(f"Found a bluetooth device: {d}")
            if d.name.startswith("ow"):
                # assuming this is a onewheel
                logging.info(f"Likely found a onewheel, using {d.address}")
                ow_mac = d.address
                break
    else:
        ow_mac = args.device
    if not ow_mac:
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
            retry = 5
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
                retry = 5  # reset retry count
                sleep(1)  # wait before refreshing
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
