class UUIDs:
    FirmwareVersion = "e659f311-ea98-11e3-ac10-0800200c9a66"
    OnewheelServiceUUID = "e659f300-ea98-11e3-ac10-0800200c9a66"
    OnewheelConfigUUID = "00002902-0000-1000-8000-00805f9b34fb"
    SerialNumber = "e659F301-ea98-11e3-ac10-0800200c9a66"  # 2085
    RidingMode = "e659f302-ea98-11e3-ac10-0800200c9a66"
    BatteryRemaining = "e659f303-ea98-11e3-ac10-0800200c9a66"
    BatteryLow5 = "e659f304-ea98-11e3-ac10-0800200c9a66"
    BatteryLow20 = "e659f305-ea98-11e3-ac10-0800200c9a66"
    BatterySerial = "e659f306-ea98-11e3-ac10-0800200c9a66"  # 22136
    TiltAnglePitch = "e659f307-ea98-11e3-ac10-0800200c9a66"
    TiltAngleRoll = "e659f308-ea98-11e3-ac10-0800200c9a66"
    TiltAngleYaw = "e659f309-ea98-11e3-ac10-0800200c9a66"
    Temperature = "e659f310-ea98-11e3-ac10-0800200c9a66"
    StatusError = "e659f30f-ea98-11e3-ac10-0800200c9a66"
    BatteryCells = "e659f31b-ea98-11e3-ac10-0800200c9a66"
    BatteryTemp = "e659f315-ea98-11e3-ac10-0800200c9a66"
    BatteryVoltage = "e659f316-ea98-11e3-ac10-0800200c9a66"
    CurrentAmps = "e659f312-ea98-11e3-ac10-0800200c9a66"
    CustomName = "e659f3fd-ea98-11e3-ac10-0800200c9a66"
    FirmwareRevision = "e659f311-ea98-11e3-ac10-0800200c9a66"  # 3034
    HardwareRevision = "e659f318-ea98-11e3-ac10-0800200c9a66"  # 2206
    LastErrorCode = "e659f31c-ea98-11e3-ac10-0800200c9a66"
    LifetimeAmpHours = "e659f31a-ea98-11e3-ac10-0800200c9a66"
    LifetimeOdometer = "e659f319-ea98-11e3-ac10-0800200c9a66"
    LightingMode = "e659f30c-ea98-11e3-ac10-0800200c9a66"
    LightsBack = "e659f30e-ea98-11e3-ac10-0800200c9a66"
    LightsFront = "e659f30d-ea98-11e3-ac10-0800200c9a66"
    Odometer = "e659f30a-ea98-11e3-ac10-0800200c9a66"
    SafetyHeadroom = "e659f317-ea98-11e3-ac10-0800200c9a66"
    SpeedRpm = "e659f30b-ea98-11e3-ac10-0800200c9a66"
    TripRegenAmpHours = "e659f314-ea98-11e3-ac10-0800200c9a66"
    TripTotalAmpHours = "e659f313-ea98-11e3-ac10-0800200c9a66"
    UartSerialRead = "e659f3fe-ea98-11e3-ac10-0800200c9a66"
    UartSerialWrite = "e659f3ff-ea98-11e3-ac10-0800200c9a66"


'''
0x0000 = e659F301-ea98-11e3-ac10-0800200c9a66 (OnewheelServiceUUID)
0x001a = e659F301-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicSerialNumber)
0x001d = e659f302-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicRidingMode)
0x0021 = e659f303-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicBatteryRemaining)
0x0025 = e659f304-ea98-11e3-ac10-0800200c9a66
0x0029 = e659f305-ea98-11e3-ac10-0800200c9a66
0x003d = e659f306-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicBatterySerial)
0x0041 = 659f307-ea98-11e3-ac10-0800200c9a66
0x0045 = e659f308-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicTiltAngleRoll)
0x0049 = e659f309-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicTiltAngleYaw)
0x003e = e659f30a-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicOdometer)
0x0041 = e659f30b-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicSpeed)
0x0045 = e659f30c-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicLightingMode)
0x0049 = e659f30d-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicLightsFront)
0x004d = e659f30e-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicLightsBack)
0x0051 = e659f30f-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicStatusError)
0x0055 = e659f310-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicTemperature)
0x0059 = e659f311-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicFirmwareRevision)
0x005d = e659f312-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicCurrentAmps)
0x0061 = e659f313-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicTripTotalAmpHours)
0x0065 = e659f314-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicTripRegenAmpHours)
0x0069 = e659f315-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicBatteryTemp)
0x006d = e659f316-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicBatteryVoltage)
0x0071 = e659f317-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicSafetyHeadroom)
0x0075 = e659f318-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicHardwareRevision)
0x0079 = e659f319-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicLifetimeOdometer)
0x007d = e659f31a-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicLifetimeAmpHours)
0x0081 = e659f31b-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicBatteryCells)
0x0085 = e659f31c-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicLastErrorCode)
0x0089 = e659f31d-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicUNKNOWN1)
0x009d = e659f31e-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicUNKNOWN2)
0x0101 = e659f31f-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicUNKNOWN3)
0x0105 = e659f320-ea98-11e3-ac10-0800200c9a66 (OnewheelCharacteristicUNKNOWN4)
0x0045=00 then lights are OFF
0x0045=01 is default lights
0x0045=02 is manual mode for lights
In manual mode (0x0045=02) 0x0049 is front lights and 0x004d is back lights
For both, the first byte is the level of light for white and second byte for red. Levels are 00 (off) to 75 (super bright)
SETS FRONT TO BRIGHT RED AND BACK TO BRIGHT WHITE:
gatttool --device=D0:39:72:BE:0A:32 --char-write-req --value=0002 --handle=0x0045
gatttool --device=D0:39:72:BE:0A:32 --char-write-req --value=0075 --handle=0x0049
gatttool --device=D0:39:72:BE:0A:32 --char-write-req --value=7500 --handle=0x004d
'''
