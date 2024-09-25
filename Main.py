import time
from PCANBasic import *

# Constants
CAN_CHANNEL = PCAN_USBBUS1  # Channel for PCAN-USB Pro FD
BITRATE_FD = b"f_clock=80000000,nom_brp=10,nom_tseg1=5,nom_tseg2=2,nom_sjw=1,data_brp=4,data_tseg1=7,data_tseg2=2,data_sjw=1"
PDB_CAN_ID = 32  # Default CAN ID for the power distribution board

# Create an instance of the PCANBasic class
pcan = PCANBasic()

# Initialize the CAN-FD channel
result = pcan.InitializeFD(CAN_CHANNEL, BITRATE_FD)
if result != PCAN_ERROR_OK:
    print("Failed to initialize CAN-FD channel. Error:", result)
    exit()

# Prepare a CAN FD message to request PDB status (0x000 - State register)
msg = TPCANMsgFD()
msg.ID = PDB_CAN_ID
msg.MSGTYPE = PCAN_MESSAGE_FD
msg.DLC = 1  # Length of the message
msg.DATA[0] = 0x00  # Command to read PDB state (register 0x000)

# Send the CAN FD message
result = pcan.WriteFD(CAN_CHANNEL, msg)
if result != PCAN_ERROR_OK:
    print("Failed to send CAN message. Error:", result)
    exit()

print("Message sent, waiting for response...")

# Read the response from the PDB
time.sleep(0.1)  # Small delay to allow response
result, response_msg, timestamp = pcan.ReadFD(CAN_CHANNEL)

if result == PCAN_ERROR_OK:
    # Print the received response
    print("Response received:")
    print("ID: 0x%X" % response_msg.ID)
    print("DLC: %d" % response_msg.DLC)
    print("Data: %s" % " ".join(["0x%X" % byte for byte in response_msg.DATA[:response_msg.DLC]]))
else:
    print("Failed to receive response. Error:", result)

# Uninitialize the CAN channel
pcan.Uninitialize(CAN_CHANNEL)
