import logging
import asyncio
from argparse import ArgumentParser
from binascii import hexlify
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError
from onewheel import UUIDs, unlock


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

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

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
        exit()
    return ow_mac


async def main():
    ow_mac = await load_cli_configuration()
    device = await BleakScanner.find_device_by_address(ow_mac, timeout=20.0)
    try:
        if not device:
            raise BleakError(
                f"A device with address {ow_mac} could not be found.")
        async with BleakClient(device) as client:
            logging.debug("Connected...")
            try:
                await unlock(client)
                logging.debug("Reading Onewheel status:")
                battery_remaining_value = await client.read_gatt_char(UUIDs.BatteryRemaining)
                lifetime_odometer_value = await client.read_gatt_char(UUIDs.LifetimeOdometer)
                trip_odometer_value = await client.read_gatt_char(UUIDs.Odometer)
                logging.info("Battery Remaining: %s%%" %
                             int(hexlify(battery_remaining_value), 16))
                logging.info("Lifetime Odometer: %s Miles" %
                             int(hexlify(lifetime_odometer_value), 16))
                logging.info("Trip Odometer: %s Miles" %
                             int(hexlify(trip_odometer_value), 16))
            except Exception as e:
                logging.error(e)
            finally:
                await client.disconnect()
    except BleakError as e:
        logging.error(e)


if __name__ == "__main__":
    asyncio.run(main())
