from os import write
from digi.xbee.devices import ZigBeeDevice, RemoteZigBeeDevice, XBee64BitAddress
import csv

PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

device = ZigBeeDevice(PORT, BAUDRATE)

#variables
start = 0
stop = 0
count_byte = 0
total_package = 0
received_package = 0
package_loss = 0
send_time = 0

header = ["time(seconds)", "total_bytes", "Kbps", "packages"]

device.open()

remote_device = RemoteZigBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041AEB242"))

remote_device.read_device_info()
print(remote_device.get_node_id())

def data_receive_callback(xbee_message):
        global stop
        global received_package
        global total_package
        global start
        global send_time


        data = xbee_message.data.decode()
        if(data.find("begin")!=-1):
                total_package= int(data[data.find("_")+1:])
                received_package = 0
                start = xbee_message.timestamp
        else:
                if(data == "end"):
                        count_byte = received_package*84
                        througput = (count_byte*8)/((stop-start)*1024)
                        package_loss = total_package-received_package
                        package_loss = "{}%".format(package_loss/total_package)
                        delay = stop-send_time
                        data_list = [stop-start, count_byte, througput, received_package, package_loss,delay]
                        # print("Concluído o recebimento de pacotes\n")
                        with open('data/teste.csv', 'a', newline= '') as file:

                                writer = csv.writer(file)       

                                writer.writerow(data_list)
                else:
                        send_time = float(data[len(data)-17:])
                        received_package += 1
                        stop = xbee_message.timestamp

device.add_data_received_callback(data_receive_callback)

input()

device.close()