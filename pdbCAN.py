from PCANBasic import *

# Initialize the PCANBasic instance
p = PCANBasic()

# Define the CAN-FD bitrate (matching your system's configuration)
bitrate = b"f_clock_mhz=24, nom_brp=1, nom_tseg1=16, nom_tseg2=7, nom_sjw=1, data_brp=1, data_tseg1=3, data_tseg2=1, data_sjw=1"

# Initialize the channel (assuming PCAN_USBBUS1 for this example)
channel = PCAN_USBBUS1
result = p.InitializeFD(channel, bitrate)
if result != PCAN_ERROR_OK:
    print(f"Failed to initialize CAN channel: {result}")
    exit(1)
else:
    print("Initialized")
    # Read the response from the PDB
    result, returnMsg, timestamp = p.ReadFD(channel)
    if result == PCAN_ERROR_OK:
        print(f"Received message ID: {returnMsg.ID}")
        print(f"DLC: {returnMsg.DLC}")
        print(f"Data: {returnMsg.DATA[:returnMsg.DLC]}")
    else:
        print(f"Error reading CAN message: {result}")

# Create a CAN-FD message
msg = TPCANMsgFD()

# Set the ID to the default PDB CAN ID (32 or 0x20 in hex)
msg.ID = 0x8000 | 0x20

# Set the message type for CAN FD
msg.MSGTYPE = PCAN_MESSAGE_FD

# Set the Data Length Code (DLC) - based on how much data you're sending (example: 8 bytes)
msg.DLC = 8

# Fill the DATA field with the appropriate request (example: sending a request for status)
# The exact contents of DATA will depend on the specific request format expected by the PDB.
msg.DATA[0] = 0x00  # Command byte (example)
msg.DATA[1] = 0x01  # Sub-command byte (example)
msg.DATA[2] = 0x00  # Additional data (example)
msg.DATA[3] = 0x00  # Additional data (example)
msg.DATA[4] = 0x00  # Additional data (example)
msg.DATA[5] = 0x00  # Additional data (example)
msg.DATA[6] = 0x00  # Additional data (example)
msg.DATA[7] = 0x00  # Additional data (example)

# Send the message using WriteFD
result = p.WriteFD(channel, msg)
if result != PCAN_ERROR_OK:
    print(f"Error sending CAN message: {p.GetErrorText(result)}")
else:
    print("Status request sent successfully")

# Read the response from the PDB
result, returnMsg, timestamp = p.ReadFD(channel)
if result == PCAN_ERROR_OK:
    print(f"Received message ID: {returnMsg.ID}")
    print(f"DLC: {returnMsg.DLC}")
    print(f"Data: {returnMsg.DATA[:returnMsg.DLC]}")
else:
    print(f"Error reading CAN message: {p.GetErrorText(result)}")
