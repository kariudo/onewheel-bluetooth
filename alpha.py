import logging
from argparse import ArgumentParser
from binascii import hexlify
from hashlib import md5
from time import sleep
from pygatt import BLEAddressType, GATTToolBackend, exceptions
from onewheel import UUIDs
##########
import os
import threading
from functools import partial
import binascii
import pygatt

adapter = GATTToolBackend()
ADDRESS_TYPE = BLEAddressType.public
key_input = bytearray()
adapter.start()
battery_level,trip_odometer,trip_regen_amp,trip_total_amp=bytearray(b'\x00\x00'),bytearray(b'\x00\x00'),bytearray(b'\x00\x00'),bytearray(b'\x00\x00')
        
def int_to_hex_string(value):
    return "{0:0{1}X}".format(value & ((1<<8) - 1), 8//4)

def custom_light(device):
    print("Sending Custom lighting:")
    device.char_write(UUIDs.LightingMode,(bytearray.fromhex("00 02")),True) # Manual light Mode, automatically turns off all lights
    fw = dec_to_hex(int(input("Front white level 0-75:")))
    fr = dec_to_hex(int(input("Front red level 0-75:")))
    bw = dec_to_hex(int(input("Back white level 0-75:")))
    br = dec_to_hex(int(input("Back red level 0-75:")))
    device.char_write(UUIDs.LightsFront,(bytearray.fromhex("%s %s" % (fw, fr))),True)
    device.char_write(UUIDs.LightsBack,(bytearray.fromhex("%s %s" %  (bw, br))),True)

def custom_shape(device):
    print("Custom Shape:")
    stance = int_to_hex_string(int(input("Stance level -20 to 60:")))
    carvability = int_to_hex_string(int(input("Carvability level -100 to 100:")))
    agressivness = int_to_hex_string(int(input("Aggressiveness level -80 to 127:")))
    print("Sending custom stance ->")
    device.char_write(UUIDs.CustomShape,(bytearray.fromhex("00 %s" % (stance))),True)
    print("Sending custom carvability ->")
    device.char_write(UUIDs.CustomShape,(bytearray.fromhex("01 %s" %  (carvability))),True)
    print("Sending custom agressivness ->")
    device.char_write(UUIDs.CustomShape,(bytearray.fromhex("02 %s" %  (agressivness))),True)

def light_off(device):
    print("Turning lights off:")
    device.char_write(UUIDs.LightingMode,(bytearray.fromhex("00 00")),True)

def dec_to_hex(x):
    """Converts Decimal to hex and adds a leading zero"""
    x = hex(x)[2:]
    x = str(x)
    if len(x) < 2:
        x = "0"+x
    return x

def light_default(device):
    print("Setting to default lighting:")
    device.char_write(UUIDs.LightingMode,(bytearray.fromhex("00 01")),True)

def wee_woo(device):
    """Pulses alternating from fulll red to full white."""
    print("WeeWoo!")
    print("Press Ctr + c to stop")
    device.char_write(UUIDs.LightingMode,(bytearray.fromhex("00 02")),True) # Manual Mode
    while True:
        device.char_write(UUIDs.LightsFront,(bytearray.fromhex("4b 00")),True) # red front
        device.char_write(UUIDs.LightsBack,bytearray.fromhex("00 4b"),True) # white back
        sleep(0.6)
        device.char_write(UUIDs.LightsFront,(bytearray.fromhex("00 4b")),True) # white front
        device.char_write(UUIDs.LightsBack,bytearray.fromhex("4b 00"),True) # red back
        sleep(0.6)

def phase_light(device):
    """This will phase the lights from red to white and back. This is intensive on the board since there is so many writes."""
    print("Phase!")
    print("Press Ctr + c to stop")
    device.char_write(UUIDs.LightingMode,(bytearray.fromhex("00 02")),True) # Man Mode
    sleep(3)
    while True:
        for x in range(0, 75):
            if x % 2 == 0: # This is just to write on every 2nd loop, this still gives a good fade with minimal writes.
                device.char_write(UUIDs.LightsFront,(bytearray.fromhex("%s %s" % (dec_to_hex(75-x), dec_to_hex(x)))),True)
                device.char_write(UUIDs.LightsBack,(bytearray.fromhex("%s %s" % (dec_to_hex(75-x), dec_to_hex(x)))),True)
                sleep(0.01)
                #sleep(2)
        for x in range(75, 0):
            if x % 2 == 0:
                device.char_write(UUIDs.LightsFront,(bytearray.fromhex("%s %s" % (dec_to_hex(75-x), dec_to_hex(x)))),True)
                device.char_write(UUIDs.LightsBack,(bytearray.fromhex("%s %s" % (dec_to_hex(75-x), dec_to_hex(x)))),True)
                sleep(0.01)
                #sleep(2)

def read_batt_remain(device):
    #reads battery remaining data
    while True:
        battery_remaining_value = device.char_read(UUIDs.BatteryRemaining)
        print("Battery Remaining: %s%%" % int(hexlify(battery_remaining_value), 16))
        sleep(1)

def subscribe_data_output(handle, value, name):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    name -- string, identifier of callback made with partial

    This is a function to be used as a callback. I used partial to add the name var to the subscribe call back so the function would know how to handle it.

    TODO
    There is probably a more efficient way to do this.
    There are many more characteristics that can be subscribed to and added to this function.
    logging output file option
    """
    try:
        global battery_level,trip_odometer,trip_regen_amp,trip_total_amp,device
        os.system('clear')
        if name is "BatteryVoltage":
            battery_level=value
        if name is "Odometer":
            trip_odometer=value
        if name is "TripRegenAmpHours":
            trip_regen_amp=value
        if name is "TripTotalAmpHours":
            trip_total_amp=value
        print("Battery level: %s Volts" % int(hexlify(battery_level), 16))
        print("Trip Odometer: %s Miles" % int(hexlify(trip_odometer), 16))
        print("Trip Regen Amp Hours: %s"% int(hexlify(trip_regen_amp), 16))
        print("Trip Total Amp Hours: %s" % int(hexlify(trip_total_amp), 16))
        #battery_remaining_value = device.char_read(UUIDs.BatteryRemaining)
        #print("Battery Remaining: %s%%" % int(hexlify(battery_remaining_value), 16))
        #sleep(1)
    except:
        print("Subscribe Failure.")

def live_stats(device):
    """
    Call all of the different call backs.
    This function would not work until I read for hours on fourms that the subscribe pygatt function needs a little bit of time to complete the subscription with the device.

    TODO
    Trim or up the sleep times, I need to run test cases on different boards to minimize the wait time, but 0.5 seems to do the trick on a OW+
    threading
    see if people want UUIDs.CurrentAmps
    """
    print("Subscribing to OW Stats.")
    BatteryVoltage_callback = partial(subscribe_data_output, name = "BatteryVoltage")
    device.subscribe(UUIDs.BatteryVoltage, callback=BatteryVoltage_callback)
    sleep(0.3)
    Odometer_callback = partial(subscribe_data_output, name = "Odometer")
    device.subscribe(UUIDs.Odometer, callback=Odometer_callback)
    sleep(0.3)
    TripRegenAmpHours_callback = partial(subscribe_data_output, name = "TripRegenAmpHours")
    device.subscribe(UUIDs.TripRegenAmpHours, callback=TripRegenAmpHours_callback)
    sleep(0.3)
    TripTotalAmpHours_callback = partial(subscribe_data_output, name = "TripTotalAmpHours")
    device.subscribe(UUIDs.TripTotalAmpHours, callback=TripTotalAmpHours_callback)
    sleep(0.3)
    #The while loop keeps the thread open so the board can keep calling back.
    while True:
        sleep(10)

def speed_readout(device):
    """
    This function is included separate from the live_stats function for minimized read requests and so that you can easily pipe it to a screen on a rasberry pi or something.
    UUIDs.SpeedRpm might be a characteristic that can be subscribed to.
    """
    tire_circumfrence = 36.1283 # This could definitely be wrong, I didn't measure, I just looked at specs online
    os.system('clear')
    while True:
        speed = device.char_read(UUIDs.SpeedRpm) # have to convert rpm to mph/kph. Need wheel circumfrence to calculate.
        speed = int(hexlify(speed), 16)
        speed = round((speed* tire_circumfrence / 63360) * 60) #RPM to MPH conversion
        print("  %s" % speed, end='\r', flush='True') #I added two spaces to this so that the terminal curser wouldnt be on top of the read out.
        sleep(0.01)

def board_info_read(device):
    """
    The commented out board infomation that contains lies. I have rode my OW many more that 6 miles(I am probably just doing it wrong).
    """
    Hardware_Revision = device.char_read(UUIDs.HardwareRevision)
    Firmware_Revision = device.char_read(UUIDs.FirmwareRevision)
    Device_Name = device.char_read(UUIDs.DeviceName)
    Custom_Device_Name = device.char_read(UUIDs.CustomName)
    #Lifetime_Amp_Hours = device.char_read(UUIDs.LifetimeAmpHours)
    Serial_Number = device.char_read(UUIDs.SerialNumber)
    #Lifetime_Odometer = device.char_read(UUIDs.LifetimeOdometer)
    print("Hardware Revision: %s" % int(hexlify(Hardware_Revision), 16))
    print("Firmware Revision: %s" % int(hexlify(Firmware_Revision), 16))
    print("Device Name: %s" % Device_Name.decode("utf-8"))
    print("Device Name: %s" % Custom_Device_Name.decode("utf-8"))
    #print("Lifetime Amp Hours: %s" % int(hexlify(Lifetime_Amp_Hours), 16))
    print("Serial Number: %s" % int(hexlify(Serial_Number), 16))
    #print("Lifetime Odometer: %s" % int(hexlify(Lifetime_Odometer), 16))

def unlock_gatt_sequence(device):
    """ Unlock lasts about 25 seconds, if we are doing more than one read, we will need to call this more """
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
    """Start unlock_timer() to keep board unlocked """
    t1 = threading.Thread(target=unlock_timer, args=(device,))
    t1.start()

def create_response_key_output():
    """ Build the response key we will send to the board to unlock access to characteristic values """
    array_to_md5 = key_input[3:19] + bytearray.fromhex("D9 25 5F 0F 23 35 4E 19 BA 73 9C CD C4 A9 17 65")
    hashed = md5(array_to_md5)
    key_output = bytearray.fromhex("43 52 58")
    key_output += hashed.digest()
    key_output += calculate_check_byte(key_output)
    return key_output

def handle_key_response(_, data):
    """ Append all key responses to the global key """
    global key_input
    key_input += data

def wait_for_key_response():
    """ Wait for full key from notifications with 30 second timeout """
    timeout = 45.0
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

def unlock_timer(device):
    """Writes the firmware revision to the board every 15 secounds to keep the board unlocked"""
    version = device.char_read(UUIDs.FirmwareRevision)
    version = version.hex()
    print(version)
    while True:
        device.char_write(UUIDs.FirmwareRevision, bytearray.fromhex(version), True)
        sleep(15)

def main():
    parser = ArgumentParser()
    parser.add_argument("device", type=str,
                        help="bluetooth address of the Onewheel to connect to")
    mutually_exclusive = parser.add_mutually_exclusive_group()
    mutually_exclusive_2 = parser.add_mutually_exclusive_group()

    mutually_exclusive.add_argument("-ww", "--weewoo", action="store_true",
                        help="Activate ambulance mode")
    mutually_exclusive.add_argument("-p", "--phase", action="store_true",
                        help="Phase between red and white")
    mutually_exclusive.add_argument("-s", "--speed", action="store_true",
                        help="Constantly output speed in mph")
    mutually_exclusive_2.add_argument("-lo", "--lights-off", action="store_true",
                        help="Turns both lights off")
    mutually_exclusive_2.add_argument("-ld", "--lights-default", action="store_true",
                        help="Turns lights to default mode")
    mutually_exclusive_2.add_argument("-cl", "--customlight", action="store_true",
                        help="Custom light prompt")
    parser.add_argument("-bi", "--board-info", action="store_true",
                        help="Read out board information")
    parser.add_argument("-cs", "--custom-shape", action="store_true",
                        help="Custom shape prompt")
    parser.add_argument("-ls", "--live-statistics", action="store_true",
                        help="Read out of board statistics")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    opts = parser.parse_args()
    
    if opts.verbose:
        logging.basicConfig()
        logging.getLogger('pygatt').setLevel(logging.DEBUG)
    
    device = adapter.connect(opts.device, address_type=ADDRESS_TYPE)
    
    try:
        unlock_gatt_sequence(device)
        if opts.board_info:
            board_info_read(device)
        if opts.customlight:
            custom_light(device)
        if opts.custom_shape:
            custom_shape(device)
        if opts.live_statistics:
            live_stats(device)
        if opts.weewoo:
            wee_woo(device)
        if opts.phase:
            phase_light(device)
        if opts.lights_off:
            light_off(device)
        if opts.speed:
            speed_readout(device)
    except exceptions.NotificationTimeout:
        print("Timed out.")
    finally:
        #t1.join()
        device.disconnect()
        adapter.stop()

if __name__ == "__main__":
    main()