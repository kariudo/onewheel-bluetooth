import logging
from .characteristics import UUIDs
from time import sleep
from hashlib import md5
from time import sleep


async def unlock(client):
    """Unlock access to GATT characteristics; lasts about 25 seconds, if we are doing more than one read, we will need to call this more.

    Args:
        client (BleakClient): The `BleakClient` to use for the bluetooth connection.
    """

    logging.debug("Requesting encryption key...")

    key_input = bytearray()

    def handle_key_response(_, data):
        """Append all key responses to the global key."""
        logging.debug("Received key response bytes: %s" % data)
        nonlocal key_input
        key_input += data

    await client.start_notify(UUIDs.UartSerialRead, handle_key_response)

    await bounce_version(client)

    wait_for_key_response(key_input)

    await client.stop_notify(UUIDs.UartSerialRead)

    key_output = create_response_key_output(key_input)
    logging.debug("Sending unlock key...")
    await client.write_gatt_char(UUIDs.UartSerialWrite, key_output)

    sleep(0.5)  # wait a moment for unlock before requesting data
    logging.debug("Unlock sequence complete...")


async def bounce_version(client):
    """Read and write back the firmware revision. This is used to trigger the unlock sequence and to keep unlocked.

    Args:
        client (BleakClient): The `BleakClient` to use for the bluetooth connection.
    """
    version = await client.read_gatt_char(UUIDs.FirmwareRevision)
    await client.write_gatt_char(UUIDs.FirmwareRevision, version, True)


def create_response_key_output(key_input):
    """Build the response key we will send to the board to unlock access to characteristic values.

    Args:
        client (key_input): The key retrieved as a response from the board, used for the unlock.

    Return:
    """
    array_to_md5 = key_input[3:19] + bytearray.fromhex(
        "D9 25 5F 0F 23 35 4E 19 BA 73 9C CD C4 A9 17 65")
    hashed = md5(array_to_md5)
    key_output = bytearray.fromhex("43 52 58")
    key_output += hashed.digest()
    key_output += calculate_check_byte(key_output)
    return key_output


def wait_for_key_response(key_input):
    """Wait for full key from notifications with 30 second timeout."""
    timeout = 30.0
    while len(key_input) < 20 and timeout > 0:
        logging.debug("Waiting for encryption key...")
        sleep(0.25)
        timeout -= 0.25
    if timeout == 0:
        logging.error(
            "Error: timeout reached waiting for encryption key response.")
        raise Exception("Timeout reached waiting for encryption key response")


def calculate_check_byte(key_output):
    """Calculate the final check byte for the response key."""
    check_byte = 0x00
    i = 0
    arr_len = len(key_output)
    while i < arr_len:
        check_byte = key_output[i] ^ check_byte
        i += 1
    return bytes([check_byte])
