from PCANBasic import *  # Import PCANBasic API
import time

# Initialize the PCAN instance
pcan = PCANBasic()

# Define CAN IDs and message constants based on the reference manual (adjust as needed)
STATUS_COMMAND = 0x10  # Example "Status" command identifier (replace with actual value)
START_ID = 0x00
END_ID = 0x7F  # Search through standard 11-bit ID range

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

def send_status_request(channel, device_id):
    """Send a status request message to the specified CAN ID."""
    msg = TPCANMsg()
    msg.ID = device_id  # Set the CAN ID for the device
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg.LEN = 1  # Length of the data (1 byte for the command)
    msg.DATA = (STATUS_COMMAND, )  # Command for status request (replace if different)

    result = pcan.Write(channel, msg)
    if result != PCAN_ERROR_OK:
        print(f"Error sending message to ID {device_id}. Error code: {result}")
    else:
        print(f"Sent status request to ID {device_id}")

def read_status_response(channel):
    """Read the response from the CAN bus and check for a status message."""
    result, msg, timestamp = pcan.Read(channel)
    if result == PCAN_ERROR_OK:
        print(f"Received message from ID {msg.ID} with data: {msg.DATA}")
        if msg.DATA[0] == STATUS_COMMAND:  # Check if it's a status response
            print(f"Status response received from device ID {msg.ID}")
            return True
    else:
        print(f"No response. Status: {result}")
    return False

def search_for_device(channel):
    """Search through a range of CAN IDs for a response to the status command."""
    for device_id in range(START_ID, END_ID + 1):
        send_status_request(channel, device_id)
        time.sleep(0.1)  # Small delay to allow response time
        if read_status_response(channel):
            print(f"Device found with ID {device_id}")
            break
    else:
        print("No device responded to the status request.")

if __name__ == "__main__":
    # Initialize CAN1 (PCAN_USBBUS1)
    channel = PCAN_USBBUS1
    if initialize_pcan_channel(channel):
        print(f"CAN1 (channel {channel}) initialized successfully.")
        
        # Search for the device by sending a status request
        search_for_device(channel)

        # Uninitialize CAN1
        uninitialize_pcan_channel(channel)
    else:
        print("Failed to initialize CAN1.")
