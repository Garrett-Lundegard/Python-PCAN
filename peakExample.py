from PCANBasic import *

p = PCANBasic()

mR = p.Initialize(PCAN_USBBUS2, PCAN_BAUD_1M)
msg = TPCANMsg()

msg.ID = 0x001
msg.LEN = 1
msg.DATA[0] = 0x00
msg.MSGTYPE = PCAN_MESSAGE_STANDARD
result = p.Write(PCAN_USBBUS2, msg)
print(p.GetErrorText(result))

returnMsg = p.Read(PCAN_USBBUS2)
print(p.GetErrorText(returnMsg[0]))
print(returnMsg[1])