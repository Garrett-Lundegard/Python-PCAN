import time
from PCANBasic import *

def initialize_fd_channel(channel):
    """Initialize the CAN FD channel."""
    pcan = PCANBasic()
    bitrate_fd = b"f_clock=80000000,nom_brp=5,nom_tseg1=15,nom_tseg2=5,nom_sjw=1,data_brp=5,data_tseg1=7,data_tseg2=2,data_sjw=1"
    result = pcan.InitializeFD(channel, bitrate_fd)
    if result != PCAN_ERROR_OK:
        print(f"Error initializing CAN FD channel {channel}. Error code: {result}")
        return None
    return pcan

def read_motor_fd_messages(pcan, channel):
    """Read messages from a CAN FD channel."""
    msg = TPCANMsgFD()  # Use TPCANMsgFD for CAN FD
    status, msg, timestamp = pcan.ReadFD(channel)
    if status != PCAN_ERROR_OK:
        return None
    return msg

def detect_can_fd_channels():
    """Detect available CAN FD channels."""
    pcan = PCANBasic()
    
    # Get the number of attached channels
    _, channel_count = pcan.GetValue(PCAN_NONEBUS, PCAN_ATTACHED_CHANNELS_COUNT)
    
    # Retrieve attached channels' information
    _, channels = pcan.GetValue(PCAN_NONEBUS, PCAN_ATTACHED_CHANNELS)
    
    available_channels = []
    
    # Iterate over the channels structure properly
    for i in range(channel_count):
        ch = channels[i]
        available_channels.append(ch.channel_handle)
    
    return available_channels

def identify_motors_on_fd_bus():
    """Identify motors on the CAN FD bus."""
    detected_channels = detect_can_fd_channels()
    motor_channels = []
    for channel in detected_channels:
        pcan = initialize_fd_channel(channel)
        if not pcan:
            continue
        for _ in range(50):  # Adjust the number of attempts as needed
            msg = read_motor_fd_messages(pcan, channel)
            if msg:
                print(f"Motor device detected on FD channel {channel}: {msg}")
                motor_channels.append(channel)
                break
            time.sleep(0.1)
        pcan.Uninitialize(channel)
    if not motor_channels:
        print("No motors detected on any CAN FD channels.")
    else:
        print(f"Motors detected on CAN FD channels: {motor_channels}")

if __name__ == "__main__":
    identify_motors_on_fd_bus()
