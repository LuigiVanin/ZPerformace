from digi.xbee.devices import ZigBeeDevice
from zigbee_tool.core.tests.throughput import throughput_receiver
    
PORT_RECEIVER = "/dev/ttyUSB5"
BAUD_RATE = 115200

device_receiver = ZigBeeDevice(PORT_RECEIVER, BAUD_RATE)

try:
    device_receiver.open()
    print(device_receiver.get_node_id())
    throughput_receiver(device_receiver)
finally:
    if device_receiver is not None and device_receiver.is_open():
            device_receiver.close()