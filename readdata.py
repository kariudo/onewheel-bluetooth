import logging
import asyncio
from argparse import ArgumentParser
from binascii import hexlify
from hashlib import md5
from time import sleep
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError


from onewheel import UUIDs


key_input = bytearray()


def load_cli_configuration():
    """ configure CLI arguments and return the device address """
    parser = ArgumentParser()
    parser.add_argument("device", type=str,
                        help="bluetooth address of the Onewheel to connect to")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="display debug level logging")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    return args.device


async def main():
    ow_mac = load_cli_configuration()
    device = await BleakScanner.find_device_by_address(ow_mac, timeout=20.0)
    try:
        if not device:
            raise BleakError(
                f"A device with address {ow_mac} could not be found.")
        async with BleakClient(device) as client:
            logging.debug("Connected...")
            try:
                await unlock_gatt_sequence(client)
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


def handle_key_response(_, data):
    """ Append all key responses to the global key """
    global key_input
    key_input += data


async def unlock_gatt_sequence(client):
    """ Unlock lasts about 25 seconds, if we are doing more than one read, we will need to call this more """
    logging.debug("Requesting encryption key...")
    await client.start_notify(UUIDs.UartSerialRead, handle_key_response)

    version = await client.read_gatt_char(UUIDs.FirmwareRevision)
    await client.write_gatt_char(UUIDs.FirmwareRevision, version, True)

    wait_for_key_response()

    key_output = create_response_key_output()
    logging.debug("Sending unlock key...")
    await client.write_gatt_char(UUIDs.UartSerialWrite, key_output)
    await client.stop_notify(UUIDs.UartSerialRead)
    sleep(0.5)  # wait a moment for unlock
    logging.debug("Unlock sequence complete...")


def create_response_key_output():
    """ Build the response key we will send to the board to unlock access to characteristic values """
    array_to_md5 = key_input[3:19] + bytearray.fromhex(
        "D9 25 5F 0F 23 35 4E 19 BA 73 9C CD C4 A9 17 65")
    hashed = md5(array_to_md5)
    key_output = bytearray.fromhex("43 52 58")
    key_output += hashed.digest()
    key_output += calculate_check_byte(key_output)
    return key_output


def wait_for_key_response():
    """ Wait for full key from notifications with 30 second timeout """
    timeout = 30.0
    while len(key_input) < 20 and timeout > 0:
        logging.debug("Waiting for encryption key...")
        sleep(0.25)
        timeout -= 0.25
    if timeout == 0:
        logging.error(
            "Error: timeout reached waiting for encryption key response.")
        quit(2)


def calculate_check_byte(key_output):
    """ Calculate the final check byte for the response key """
    check_byte = 0x00
    i = 0
    arr_len = len(key_output)
    while i < arr_len:
        check_byte = key_output[i] ^ check_byte
        i += 1
    return bytes([check_byte])


if __name__ == "__main__":
    asyncio.run(main())
