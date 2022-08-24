from digi.xbee.util.utils import hex_to_string
from digi.xbee import devices
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice, XBeeMessage
from os import listdir
from os.path import isfile, join

#Verifica os dispositivos conectados fisicamente e os salva em um arquivo para ser utilizados de forma seletiva.
#Funcional apenas no linux.
def checkAllDevices():
	mypath = "/sys/class/tty/"
	discovered = False
	dispositivos = []
	cont = 1
	for fileName in listdir(mypath):
		if fileName.find("ttyUSB") != -1:
			newFileName = "/dev/" + fileName
			device = ZigBeeDevice(newFileName, 115200)
			device.open()
			
			node = str(newFileName) + " - " + str(device.get_node_id()) + " - " + hex_to_string(device.get_pan_id()).replace(" ", "")
			
			dispositivos.append(node)
			device.close()
			discovered = True
			
	if discovered:
		if len(dispositivos) > 1:
			print("Foram encontrados {} dispositos:".format(len(dispositivos)))
		else:
			print("Encontramos esse dispositivo:")
			
		print("PORT - NODE - MAC")
		for i in dispositivos:
			print("({}){}".format(cont, i))
			cont += 1
		
		destination_file = "./zigbee_tool/core/dispositivosConectados/dispositivos.txt"
		f = open(destination_file, "w", newline="\n")
		with f as myDevices:
			for i in dispositivos:
				myDevices.write(i)
				myDevices.write("\n")
		f.close()
	else:
		print("Nenhum dispositivo conectado")

#Retorna o dispositivo através de um número, somente utilizar após o checkdevices.
def returnDevice(choice, info):
	destination_file = "./zigbee_tool/core/dispositivosConectados/dispositivos.txt"
	cont = 1
	dados = []
	dispositivos = []
	miniString = ""
	try:
		choice = int(choice)
		info = int(info)
	
		f = open(destination_file, "r")
		frase = f.read()
		for i in frase:
			if i != "\n" and i != '-' and i != ' ':
				miniString += i
			else:
				if len(miniString) > 0:
					dados.append(miniString)
					miniString = ""
				if i == "\n":
					dispositivos.append(dados)
					dados = []
		return dispositivos[choice-1][info]		
		
	except:
		return -1








