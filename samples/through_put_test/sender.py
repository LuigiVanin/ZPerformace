from digi.xbee.devices import ZigBeeDevice, XBee64BitAddress, RemoteZigBeeDevice
from zigbee_tool.core.tests.throughput import throughput_sender

PORT = "/dev/ttyUSB6"
BAUD_RATE = 115200

REMOTE_DEVICE = XBee64BitAddress.from_hex_string("0013A20041AECCD5")

device =  ZigBeeDevice(PORT, BAUD_RATE)

try:
    device.open()
    remote = RemoteZigBeeDevice(device, node_id="ROUTER_02")

    remote.read_device_info()

    print(device.get_node_id(), remote.get_node_id())
    
    throughput_sender(
        local=device,
        remote=remote,
        rep_amount=2
    )
finally:
    if device is not None and device.is_open():
            device.close()