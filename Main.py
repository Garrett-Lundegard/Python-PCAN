from PCANBasic import *  # Import PCANBasic API

# Initialize the PCAN instance
pcan = PCANBasic()

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

def send_test_message(channel):
    """Send a test CAN message on the specified channel."""
    msg = TPCANMsg()
    msg.ID = 0x100  # Example message ID
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg.LEN = 8  # Data length
    msg.DATA = (0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08)

    result = pcan.Write(channel, msg)
    if result != PCAN_ERROR_OK:
        print(f"Error sending message on channel {channel}. Error code: {result}")
    else:
        print(f"Message sent successfully on channel {channel}")

def read_messages(channel):
    """Read incoming messages from the CAN channel."""
    result, msg, timestamp = pcan.Read(channel)
    if result == PCAN_ERROR_OK:
        print(f"Received message on channel {channel} with ID: {msg.ID}, Data: {msg.DATA}")
    else:
        print(f"No messages to read on channel {channel}. Status: {result}")

if __name__ == "__main__":
    # Initialize CAN1 (PCAN_USBBUS1)
    channel = PCAN_USBBUS1
    if initialize_pcan_channel(channel):
        print(f"CAN1 (channel {channel}) initialized successfully.")
        
        # Send a test message
        send_test_message(channel)

        # Attempt to read any incoming messages
        read_messages(channel)

        # Uninitialize CAN1
        uninitialize_pcan_channel(channel)
    else:
        print("Failed to initialize CAN1.")
