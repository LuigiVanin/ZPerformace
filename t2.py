from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice, XBeeMessage
from zigbee_tool.core.tests.throughput import throughput_receiver
    
PORT_RECEIVER = "/dev/ttyUSB6"
BAUD_RATE = 115200

# count = 0
# def callback(message: XBeeMessage):
#     global count
#     print(message.data.decode())
#     count = count + 1
    
device_receiver = ZigBeeDevice(PORT_RECEIVER, BAUD_RATE)
device_receiver.open()
print(device_receiver.get_node_id())
throughput_receiver(device_receiver, file_dest='data/data.csv')
# device_receiver.add_data_received_callback(callback)