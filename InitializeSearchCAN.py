from PCANBasic import *

pcan = PCANBasic()

def initialize_channel(channel):
    """Initialize a specific channel with PCAN Basic API"""
    result = pcan.Initialize(channel, PCAN_BAUD_500K)
    return result

def uninitialize_channel(channel):
    """Uninitialize a specific channel with PCAN Basic API"""
    pcan.Uninitialize(channel)

def check_device(channel):
    """Check if a CAN device is active on a specific channel"""
    status = pcan.GetStatus(channel)
    return status == PCAN_ERROR_OK

def list_connected_devices():
    """List all connected CAN devices on the PCAN-PCI bus"""
    connected_devices = []
    channels = [PCAN_PCIBUS1, PCAN_PCIBUS2, PCAN_PCIBUS3, PCAN_PCIBUS4,
                PCAN_PCIBUS5, PCAN_PCIBUS6, PCAN_PCIBUS7, PCAN_PCIBUS8]

    pcan_instance = pcan
    
    for channel in channels:
        result = initialize_channel(channel)
        if result == PCAN_ERROR_OK and check_device(channel):
            connected_devices.append(channel)
        uninitialize_channel(channel)

    return connected_devices

if __name__ == "__main__":
    
    devices = list_connected_devices()
    if devices:
        print("Connected CAN devices found on PCAN-PCI Bus:")
        for device in devices:
            print(f"Device on Channel: {device}")
    else:
        print("No CAN devices found on the PCAN-PCI Bus.")
