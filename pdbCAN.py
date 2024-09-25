from PCANBasic import *

channel = 81                            
BitrateFD = b'f_clock_mhz=8,nom_brp=10,nom_tseg1=5,nom_tseg2=2,nom_sjw=1,data_brp=4,data_tseg1=7,data_tseg2=2,data_sjw=1'
#BitrateFD = "f_clock=1000000,nom_brp=10,nom_tseg1=5,nom_tseg2=2,nom_sjw=1,data_brp=4,data_tseg1=7,data_tseg2=2,data_sjw=1"
#BitrateFD = b'f_clock_mhz=20, nom_brp=5, nom_tseg1=2, nom_tseg2=1, nom_sjw=1, data_brp=2, data_tseg1=3, data_tseg2=1, data_sjw=1'

pcan = PCANBasic()

# Get the number of attached channels
_, channel_count = pcan.GetValue(PCAN_NONEBUS, PCAN_ATTACHED_CHANNELS_COUNT)

# Retrieve attached channels' information
_, channels = pcan.GetValue(PCAN_NONEBUS, PCAN_ATTACHED_CHANNELS)

"""Initialize a specific CAN channel."""
result = pcan.InitializeFD(channel, BitrateFD)
print(pcan.GetErrorText(result))

MessageBuffer = "0x0000"
print(pcan.GetErrorText(pcan.WriteFD(channel, MessageBuffer)))

