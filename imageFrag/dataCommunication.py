from typer import Typer, Argument, echo
from typing import List, Optional, Tuple
from digi.xbee.util.utils import hex_to_string
from digi.xbee import devices
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice, XBeeMessage

#from datetime import datetime
import pandas as pd

import time

import csv
import os
import io
import PIL.Image as Image
import sys

from array import array

def sender(
	data,
	device,
	remote
) -> None:
	echo(message="O dispositivo encontrado foi:\n- MAC: {}\n- Node ID: {}".format(hex_to_string(remote.get_pan_id()).replace(" ", ""), remote.get_node_id()))

	if data.find(".png") != -1 or data.find(".jpeg") != -1 or data.find(".jpg") != -1:
		with open(data, "rb") as image:
			b = bytearray(image.read())
		pacote = ""
		for i in b:
			if len(pacote) > 82:
				device.send_data(remote, pacote)
				pacote = ""
			if i == 0:
				pacote += 'o'
			elif i == 255:
				pacote += 't'
			elif i < 16:
				pacote = pacote + '0' + str(hex(i))[2]
			else:
				pacote = pacote + str(hex(i))[2] + str(hex(i))[3]
		device.send_data(remote,data=pacote)
	else:
		device.send_data(remote, data=data)
	device.send_data_async(remote, "fim!!!")
	print("Data sended!!!")

_packets = []
_antes =  -1
_depois = 0

def __receive_callback(message: XBeeMessage):
	global _packets , _antes, _depois
	msg: str = message.data.decode()
	
	if _antes == -1:
		_antes = time.time()
	
	if msg.find("fim!!!") != -1 :
		_depois = time.time()
		print("\n---FIM DO PROGRAMA---\nPress Enter For Results")
		return
	
	_packets.append(msg)


def receiver(
	local:ZigBeeDevice
) -> None:
	global _packets, _antes, _depois 
	
	local.add_data_received_callback(__receive_callback)
	input()
	if len(_packets) != 1:
		imageOutput = "imageFrag/imageOutput.png"
		splittedPacket = []
		for i in _packets:
			semi = ''
			for j in i:
				if len(semi) == 2:
					splittedPacket.append(semi)
					semi = ''
				if j == 'o' or j == 't':
					if j == 'o':
						splittedPacket.append("0")
					else:
						splittedPacket.append("ff")
				else:		
					semi += j

			if semi != '':
				if j == 'o' or j == 't':
					if j == 'o':
						splittedPacket.append("0")
					else:
						splittedPacket.append("ff")
				else:		
					splittedPacket.append(semi)

		arrayImage = []

		for point in splittedPacket:
			arrayImage.append(int(point, base=16))

		bytearrayImage = bytearray(arrayImage)
		image = Image.open(io.BytesIO(bytearrayImage))
		image.save(imageOutput)

		height = os.stat(imageOutput).st_size

		newNow = (_depois - _antes)

		df2 = pd.DataFrame({
		"Tamanho da imagem (KB)" : [height],
		"Tempo total de recebimento (s)" : [newNow],
		"Throughput Bytes (KBps)" : [height/newNow],
		"Throughput bits (Kbps)" : [8*(height/newNow)]
		})
		df2.to_csv("imageFrag/data.csv",  mode='a', index=False, header=False)

	else:
		print("A mensagem eviada foi: ", _packets[0])

