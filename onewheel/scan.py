from bleak import BleakScanner
import logging


async def scan_for_onewheel(multi: bool = False, timeout: int = 5):
    """Detect bluetooth devices that are likely a Onewheel.

    It is expected that any device in range that starts its name with "ow" (like ow123456) is most
    likely a onewheel and will be returned.


    Args:
        multi (bool): If set to true, a list will be returned instead of the first match.
        timeout (int): Time to scan for. (default: 5 seconds)

    Raises:
        Exception: No devices matching the pattern were found.

    Returns:
        str: MAC address of the first onewheel in range.
        List[str]: (If `multi`) List of all matching MAC addresses.
    """
    devices = await BleakScanner.discover(timeout)
    onewheels = []
    for d in devices:
        logging.debug(f"Found a bluetooth device: {d}")
        if d.name.startswith("ow"):
            logging.info(f"Likely found a onewheel, using {d.address}")
            if multi:
                onewheels.append(d.address)
            else:
                return d.address
    if len(onewheels) > 0:
        return onewheels
    raise ScanError("No bluetooth devices found that appear to be a Onewheel.")


class ScanError(IOError):
    """An error occurred while scanning for Onewheel devices."""
    pass
