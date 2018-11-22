import logging
from argparse import ArgumentParser
from binascii import hexlify
from hashlib import md5
from time import sleep

from pygatt import BLEAddressType, GATTToolBackend, exceptions

from onewheel import UUIDs


def load_cli_configuration():
    """ configure CLI arguments and return the device address """
    parser = ArgumentParser()
    parser.add_argument("device", type=str,
                        help="bluetooth address of the Onewheel to connect to")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig()
        logging.getLogger('pygatt').setLevel(logging.DEBUG)
    return args.device


adapter = GATTToolBackend()
ADDRESS_TYPE = BLEAddressType.public
key_input = bytearray()


def main():
    ow_mac = load_cli_configuration()
    adapter.start()
    device = adapter.connect(ow_mac, address_type=ADDRESS_TYPE)
    try:
        unlock_gatt_sequence(device)
        print("Reading Onewheel status:")
        battery_remaining_value = device.char_read(UUIDs.BatteryRemaining)
        lifetime_odometer_value = device.char_read(UUIDs.LifetimeOdometer)
        trip_odometer_value = device.char_read(UUIDs.Odometer)
        print("Battery Remaining: %s%%" % int(hexlify(battery_remaining_value), 16))
        print("Lifetime Odometer: %s Miles" % int(hexlify(lifetime_odometer_value), 16))
        print("Trip Odometer: %s Miles" % int(hexlify(trip_odometer_value), 16))
    except exceptions.NotificationTimeout:
        print("Timed out.")
    finally:
        device.disconnect()
        adapter.stop()


def handle_key_response(_, data):
    """ Append all key responses to the global key """
    global key_input
    key_input += data


def unlock_gatt_sequence(device):
    print("Requesting encryption key...")
    device.subscribe(UUIDs.UartSerialRead, callback=handle_key_response)
    version = device.char_read(UUIDs.FirmwareRevision)
    device.char_write(UUIDs.FirmwareRevision, version, True)
    wait_for_key_response()
    key_output = create_response_key_output()
    print("Sending unlock key...")
    device.char_write(UUIDs.UartSerialWrite, key_output)
    device.unsubscribe(UUIDs.UartSerialRead)
    sleep(0.5)  # wait a moment for unlock


def create_response_key_output():
    """ Build the response key we will send to the board to unlock access to characteristic values """
    array_to_md5 = key_input[3:19] + bytearray.fromhex("D9 25 5F 0F 23 35 4E 19 BA 73 9C CD C4 A9 17 65")
    hashed = md5(array_to_md5)
    key_output = bytearray.fromhex("43 52 58")
    key_output += hashed.digest()
    key_output += calculate_check_byte(key_output)
    return key_output


def wait_for_key_response():
    """ Wait for full key from notifications with 30 second timeout """
    timeout = 30.0
    while len(key_input) < 20 and timeout > 0:
        print("Waiting for encryption key...")
        sleep(0.25)
        timeout -= 0.25
    if timeout == 0:
        print("Error: timeout reached waiting for encryption key response.")
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
    main()
