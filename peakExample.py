import time
from PCANBasic import *

p = PCANBasic()

mR = p.Initialize(PCAN_USBBUS2, PCAN_BAUD_1M)

idRange = [1, 16] #range(1, 128)
scanDelay = 0.1

for canID in idRange:
    
    print(f"Scanning CAN ID: {canID}")
    
    msg = TPCANMsg()
    msg.ID = canID
    msg.LEN = 1
    msg.DATA[0] = 0x00
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    
    result = p.Write(PCAN_USBBUS2, msg)
    if result != PCAN_ERROR_OK:
        print(f"Failed to send CAN message to ID {canID}. Error: {result}")
        continue  # Skip to the next ID if sending fails
    
    time.sleep(scanDelay)

    result, returnMsg, _ = p.Read(PCAN_USBBUS2)
    if result == PCAN_ERROR_OK:
        print(returnMsg.ID)
        print(returnMsg.LEN)
        print(returnMsg.DATA[:])

    time.sleep(scanDelay)