from digi.xbee.devices import ZigBeeDevice
from zigbee_tool.core.tests.throughput import throughput_receiver
    
PORT_RECEIVER = "/dev/ttyUSB1"
BAUD_RATE = 115200
    
device_receiver = ZigBeeDevice(PORT_RECEIVER, BAUD_RATE)
device_receiver.open()
print(device_receiver.get_node_id())
throughput_receiver(device_receiver, file_dest='data/data.csv')
