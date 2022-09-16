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
		cont = 84
		while cont < len(b):
			#tempo = 
			device.send_data(remote, data = b[cont-84 : cont])
			cont += 84
			
		device.send_data(remote, data = b[cont-84 : ])
	else:
		device.send_data(remote, data=data)
	#device.send_data_async(remote, "fim!!!")
	print("Data sended!!!")

_packets = []
_antes =  -1
_depois = 0

def __receive_callback(message: XBeeMessage):
	global _packets , _antes, _depois
	msg: str = message.data
	
	if _antes == -1:
		_antes = time.time()
	if len(msg) < 84:	
		#newMsg = message.data.decode()
		_depois = time.time()
		print("\n---FIM DO PROGRAMA---\nPress Enter For Results")
	
	_packets.append(msg)


def receiver(
	local:ZigBeeDevice
) -> None:
	global _packets, _antes, _depois

	local.add_data_received_callback(__receive_callback)
	input()
	#time.sleep(25)

	imageOutput = "imageFrag/imageOutput.png"
	p = bytearray()
	for i in _packets:
		for j in i:
			p.append(j)

	arrayImage = []

	#bytearrayImage = bytearray(arrayImage)
	image = Image.open(io.BytesIO(p))
	image.save(imageOutput)

	height = os.stat(imageOutput).st_size

	newNow = (_depois - _antes)

	df2 = pd.DataFrame({
	"Tamanho real da imagem (KB)" : [height],
	"Tamanho máximo da trasferência de dados (KB)" : [len(_packets) * 84],
	"Quantidade de pacotes enviados" : [len(_packets)],
	"Tempo total de recebimento (s)" : [newNow],
	"Throughput Bytes (KBps)" : [height/newNow],
	"Média de tempo por pacote" : [newNow/len(_packets)]
	#"Throughput bits (Kbps)" : [8*(height/newNow)]
	})
	df2.to_csv("imageFrag/data.csv",  mode='a', index=False, header=False)

	#else:
	#	print("A mensagem eviada foi: ", _packets[0])
	#print(newNow)
