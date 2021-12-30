import asyncio
import logging
from bleak import BleakScanner, BleakClient
from .auth import bounce_version, unlock as unlock_gatt
from .characteristics import UUIDs
from binascii import hexlify


class Onewheel:
    def __init__(self, address):
        self.address = address
        self.name = None
        self.client = BleakClient(self.address)

    async def connect(self):
        """ Connect to the device """
        logging.debug(f"Connecting to {self.address}")
        try:
            await self.client.connect()
            if await self.is_locked():
                await self.unlock()
            logging.debug("Connected")
            self.name = (await self.client.read_gatt_char(UUIDs.DeviceName)).decode()
            asyncio.create_task(self.keep_alive())
        except Exception as e:
            logging.error(f"Connection error: {e}")
            return False
        finally:
            return self.client.is_connected

    async def disconnect(self):
        """ Disconnect from device """
        logging.debug(f"Disconnecting from {self.address}")
        try:
            await self.client.disconnect()
            logging.debug("Disconnected")
        except Exception as e:
            logging.error(e)

    async def read_uuid_as_int(self, uuid):
        """ Read the provided UUID and return an int """
        value = await self.client.read_gatt_char(uuid)
        int_value = bin2int(value)
        return int_value

    async def batt_percentage(self):
        """ Read the current battery percentage """
        return await self.read_uuid_as_int(UUIDs.BatteryRemaining)

    async def odometer(self):
        """ Read the odometer """
        return await self.read_uuid_as_int(UUIDs.LifetimeOdometer)

    async def tripmeter(self):
        """ Read the trip odometer """
        return await self.read_uuid_as_int(UUIDs.Odometer)

    # TODO Add remaining property functions

    async def unlock(self):
        """ send teh"""
        await unlock_gatt(self.client)

    async def keep_alive(self):
        """ Send the command to keep us unlocked every 20 seconds """
        await asyncio.sleep(20)
        if self.client.is_connected:
            await bounce_version(self.client)
            logging.debug(f"Keep-alive sent")
            await asyncio.create_task(self.keep_alive())
        else:
            logging.warning("Not connected, cannot keep alive")

    async def is_locked(self):
        """ Attempt to read some data to see if we need to unlock GATT """
        batt = await self.batt_percentage()
        # If the battery reads as 0 we are not getting data.
        locked = batt == 0
        logging.debug(f"Locked: {locked}")
        return locked


def bin2int(value):
    return int(hexlify(value), 16)
