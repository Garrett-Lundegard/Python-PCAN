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

def check_device_id(channel, target_id=32):
    """Check for the mjbots power distribution board based on its default ID."""
    result, msg, timestamp = pcan.Read(channel)
    if result == PCAN_ERROR_OK:
        if msg.ID == target_id:
            print(f"mjbots Power Distribution Board detected with ID {msg.ID}")
        else:
            print(f"Detected device with ID {msg.ID}, but it does not match the expected ID {target_id}.")
    else:
        print(f"No message read from CAN. Status: {result}")

if __name__ == "__main__":
    # Initialize CAN1 (PCAN_USBBUS1)
    channel = PCAN_USBBUS1
    if initialize_pcan_channel(channel):
        print(f"CAN1 (channel {channel}) initialized successfully.")
        
        # Check for the mjbots power distribution board ID
        check_device_id(channel, target_id=32)

        # Uninitialize CAN1
        uninitialize_pcan_channel(channel)
    else:
        print("Failed to initialize CAN1.")
