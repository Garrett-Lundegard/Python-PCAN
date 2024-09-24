import time
from PCANBasic import *

def initialize_channel(channel):
    pcan = PCANBasic()
    result = pcan.Initialize(channel, PCAN_BAUD_500K)
    if result != PCAN_ERROR_OK:
        print(f"Error initializing channel {channel}. Error code: {result}")
        return None
    return pcan

def read_motor_messages(pcan, channel):
    msg = TPCANMsg()
    status = pcan.Read(channel, msg)
    if status != PCAN_ERROR_OK:
        return None
    return msg

def detect_can_channels():
    pcan = PCANBasic()
    channels_count = pcan.GetValue(PCAN_NONEBUS, PCAN_ATTACHED_CHANNELS_COUNT)
    channels = pcan.GetValue(PCAN_NONEBUS, PCAN_ATTACHED_CHANNELS)
    available_channels = [ch['channel_handle'] for ch in channels if ch['channel_condition'] in (0x02, 0x03)]  # Available or in use by PCAN-View
    return available_channels

def identify_motors_on_bus():
    detected_channels = detect_can_channels()
    motor_channels = []
    for channel in detected_channels:
        pcan = initialize_channel(channel)
        if not pcan:
            continue
        for _ in range(10):  # Adjust the number of attempts as needed
            msg = read_motor_messages(pcan, channel)
            if msg:
                print(f"Motor device detected on channel {channel}: {msg}")
                motor_channels.append(channel)
                break
            time.sleep(0.1)
        pcan.Uninitialize(channel)
    if not motor_channels:
        print("No motors detected on any channels.")
    else:
        print(f"Motors detected on channels: {motor_channels}")

if __name__ == "__main__":
    identify_motors_on_bus()
