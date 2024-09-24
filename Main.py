from PCANBasic import *
import time

# Initialize the PCAN instance
pcan = PCANBasic()

STATUS_COMMAND_ID = 0x8001  # Example ID for the "Status" command (based on documentation)
MAX_CAN_ID = 127  # Assuming a 7-bit CAN ID range for standard devices

def initialize_pcan_channel(channel, baudrate=PCAN_BAUD_500K):
    """Initialize a specific CAN channel."""
    result = pcan.Initialize(channel, baudrate)
    if result != PCAN_ERROR_OK:
        print(f"Error initializing CAN channel {channel}. Error code: {result}")
        return False
    return True

def uninitialize_pcan_channel(channel):
    """Uninitialize a specific CAN channel."""
    pcan.Uninitialize(channel)

def send_status_request(channel, target_id):
    """Send a status request command to the specified target CAN ID."""
    msg = TPCANMsg()
    msg.ID = target_id  # Set the message to the target device ID
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg.LEN = 2  # Assuming command message length of 2 bytes
    msg.DATA = (STATUS_COMMAND_ID & 0xFF, (STATUS_COMMAND_ID >> 8) & 0xFF)  # Status command data

    result = pcan.Write(channel, msg)
    if result != PCAN_ERROR_OK:
        print(f"Error sending status request to ID {target_id}. Error code: {result}")
    else:
        print(f"Status request sent to ID {target_id}")

def read_response(channel):
    """Read incoming messages from the CAN channel."""
    result, msg, timestamp = pcan.Read(channel)
    if result == PCAN_ERROR_OK:
        print(f"Received message on channel {channel} from ID: {msg.ID}, Data: {list(msg.DATA)}")
        return msg.ID, list(msg.DATA)
    return None, None

def search_for_device(channel):
    """Search for a device that responds to the 'Status' command."""
    for can_id in range(1, MAX_CAN_ID + 1):
        send_status_request(channel, can_id)
        time.sleep(0.05)  # Short delay to allow for response

        device_id, data = read_response(channel)
        if device_id is not None:
            print(f"Device detected at CAN ID: {device_id} with data: {data}")
            return device_id
    print("No device responded to the Status request.")
    return None

if __name__ == "__main__":
    # Initialize CAN1 (PCAN_USBBUS1)
    channel = PCAN_USBBUS1
    if initialize_pcan_channel(channel):
        print(f"CAN1 (channel {channel}) initialized successfully.")
        
        # Search for a device that responds to the status request
        search_for_device(channel)

        # Uninitialize CAN1
        uninitialize_pcan_channel(channel)
    else:
        print("Failed to initialize CAN1.")
