import time
from PCANBasic import *

p = PCANBasic()

bitrate = "f_clock_mhz=24, nom_brp=1, nom_tseg1=17, nom_tseg2=6, nom_sjw=1, data_brp=1, data_tseg1=16, data_tseg2=7, data_sjw=1"
channel = PCAN_USBBUS1

mR = p.InitializeFD(channel, bitrate)

idRange = [1, 32] #range(16,35)
scanDelay = 0.1

for canID in idRange:
    
    print(f"Scanning CAN ID: {canID}")
    
    msg = TPCANMsgFD()
    msg.ID = canID
    msg.DLC = 3
    msg.DATA[0] = 0x0
    msg.DATA[1] = 0x0
    msg.DATA[2] = 0x0
    msg.MSGTYPE = PCAN_MESSAGE_FD
    
    result = p.WriteFD(channel, msg)
    if result != PCAN_ERROR_OK:
        print(f"Failed to send CAN message to ID {canID}. Error: {result}")
        continue  # Skip to the next ID if sending fails
    
    time.sleep(scanDelay)

    result, returnMsg, _ = p.ReadFD(channel)
    if result == PCAN_ERROR_OK:
        print(returnMsg.ID)
        print(returnMsg.DLC)
        print(returnMsg.DATA[:])

    time.sleep(scanDelay)