from PCANBasic import *
import time

# Initialize the PCAN instance
pcan = PCANBasic()

STATUS_REQUEST_ID = 0x8001  # ID for sending from source 0 to destination 1
STATUS_RESPONSE_ID = 0x100  # ID for receiving response from device 1 to source 0

# CAN registers for status info (Voltage, Temperature, Fault Code)
REGISTER_VOLTAGE = 0x00D
REGISTER_TEMPERATURE = 0x00E
REGISTER_FAULT_CODE = 0x00F

def initialize_pcan_channel(channel, baudrate=PCAN_BAUD_1M):
    """Initialize a specific CAN channel."""
    result = pcan.Initialize(channel, baudrate)
    if result != PCAN_ERROR_OK:
        print(f"Error initializing CAN channel {channel}. Error code: {result}")
        return False
    return True

def uninitialize_pcan_channel(channel):
    """Uninitialize a specific CAN channel."""
    pcan.Uninitialize(channel)

def send_status_request(channel):
    """Send a status request command to the specified target CAN ID."""
    msg = TPCANMsg()
    msg.ID = STATUS_REQUEST_ID  # Send from source 0 to destination 1 with reply
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg.LEN = 4  # Read 3 registers starting from 0x00D
    msg.DATA = (0x14, 0x03, REGISTER_VOLTAGE, 0x00)  # Read 3 int16 registers (Voltage, Temp, Fault Code)

    result = pcan.Write(channel, msg)
    if result != PCAN_ERROR_OK:
        print(f"Error sending status request. Error code: {result}")
    else:
        print(f"Status request sent.")

def read_response(channel):
    """Read incoming messages from the CAN channel."""
    result, msg, timestamp = pcan.Read(channel)
    if result == PCAN_ERROR_OK and msg.ID == STATUS_RESPONSE_ID:
        print(f"Received response from device. Data: {list(msg.DATA)}")
        voltage = msg.DATA[0] | (msg.DATA[1] << 8)
        temperature = msg.DATA[2] | (msg.DATA[3] << 8)
        fault_code = msg.DATA[4]
        print(f"Voltage: {voltage / 10.0}V, Temperature: {temperature / 10.0}C, Fault Code: {fault_code}")
        return True
    return False

if __name__ == "__main__":
    # Initialize CAN1 (PCAN_USBBUS1)
    channel = PCAN_USBBUS1
    if initialize_pcan_channel(channel):
        print(f"CAN1 (channel {channel}) initialized successfully.")
        
        # Send the status request
        send_status_request(channel)
        time.sleep(0.1)  # Allow time for the device to respond

        # Read the response
        if not read_response(channel):
            print("No response received.")

        # Uninitialize CAN1
        uninitialize_pcan_channel(channel)
    else:
        print("Failed to initialize CAN1.")
