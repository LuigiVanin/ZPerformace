from typer import Typer, Argument, echo
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice
from digi.xbee.util.utils import hex_to_string
from ..core.tests.throughput import throughput_receiver, throughput_sender
from ..core.plot import plot_throughput_data, plot_delay_data, plot_packet_loss_data
from typing import Optional

import os
import io
import PIL.Image as Image
import sys

from array import array

cli = Typer()

@cli.command()
def broadcast(
    port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    data: str = Argument(..., help="a mensagem é o texto a ser transmitido via boradcast")
) -> None:
    '''
    comando que realiza uma mensagem por broadcast a partir do dispositivo a qual a porta foi declarada
    '''
    device = ZigBeeDevice(port, 115200)
    try:
        device.open()
        device.send_data_broadcast(data)
    finally:
        if device is not None and device.is_open():
            device.close()
            
            
@cli.command()
def sendData(
    port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    dest: str = Argument(..., help="nome do nó(node id) do destinatário"),
    data: str = Argument(..., help="dados a serem enviados")
) -> None:
	'''
	Manda uma mensagem direta ao dispositivo especificado por meio de um envio sincrono.
	'''
	device = ZigBeeDevice(port, 115200)
	try:
		device.open()
		remote = RemoteZigBeeDevice(device, node_id=dest)
		remote.read_device_info()
		
		echo(message="O dispositivo encontrado foi:\n- MAC: {}\n- Node ID: {}".format(hex_to_string(remote.get_pan_id()).replace(" ", ""),
		remote.get_node_id()))
		
		if data.find(".png") != -1 or data.find(".jpeg") != -1:
			#print("oi")
			device.send_data(remote, "image")
			with open(data, "rb") as image:
				b = bytearray(image.read())
			pacote = ""
			predictedPacket = ""
			for i in b:
				predictedPacket = pacote + str(i) + "/"
				if sys.getsizeof(predictedPacket) > 84:
					device.send_data(remote, pacote)
					#print(pacote)
					pacote = ""
				pacote += str(i) + "/"
			device.send_data(remote,data=pacote)
		else:
			device.send_data_async(remote,data=data)
		device.send_data_async(remote, "fim!!!")
	finally:
		if device is not None and device.is_open():
			device.close()


@cli.command()
def receiveData(
	port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido")	
) -> None:
	'''
	Recebe uma mensagem diretamente do dispositivo especificado por meio de um envio sincrono.
	'''
	device = ZigBeeDevice(port, 115200)
	try:
		device.open()
		device_message = None
		while device_message == None:
			device_message = device.read_data()
		#print(device_message.data.decode())

		if device_message.data.decode() == "image":
			imageOutput = "imageFrag/imageOutput.png"
			pacote = ""
			fim = False
			array = []
			fin = bytearray(b'fim!!!')
			while not fim:
				device_message = device.read_data()
				if device_message != None:
					if device_message.data != fin:
						array.append(device_message)
						#pacote += device_message.data.decode()
					else:
						fim = True
						#print(device_message.data == bytearray(b'fim!!!'))
			
			for i in array:
				pacote += i.data.decode()
			#print("oi")
			splittedPacket = pacote.split("/")
			splittedPacket.pop(len(splittedPacket)-1)
			
			arrayImage = []
			
			for point in splittedPacket:
				arrayImage.append(int(point))
			
			bytearrayImage = bytearray(arrayImage)
			#print(bytearrayImage)
			image = Image.open(io.BytesIO(bytearrayImage))
			image.save(imageOutput)
		else:
			while device_message == None:
				device_message = device.read_data()
			print(device_message.data.decode())
			#print("error")
        
	finally:
		if device is not None and device.is_open():
			device.close()


@cli.command()
def performaceSender(
    port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    dest: str = Argument(..., help="Nome do nó(node id) do destinatário"),
    packet_length: str = Argument(..., help="Tamanho do(s) pacote(s) a ser(em) enviado(s)"),
    pack_amount: int = Argument(..., help="Quantidade de pacotes a serem enviados"),
    executions_number: int = Argument(..., help="Número de vezes que o teste é executado.")
) -> None:
    '''
    Executa a parte de envio de dados de um teste de performace(throughput, delay e perca de pacotes). As repetições e tamanho das mensagens podem ser alterados.
    Vale salientar que cada iteração do teste(execution_number) envia um total de 100 pacotes/mensagens, com esse valor sendo fixado.
    '''
    
    print("Começando o processo de enviar pacotes para teste de throughput \n\n")
    local = ZigBeeDevice(port, baud_rate=115200)
    try:
        local.open()
        remote = RemoteZigBeeDevice(local, node_id=dest)
        remote.read_device_info()
        throughput_sender(local, remote, packet_length, pack_amount, executions_number)
    finally:
        if local is not None and local.is_open():
            local.close()
            

@cli.command()
def performaceReceiver(
    port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    dest_file: Optional[str] = "./data/data.csv" #Argument(..., help="Caminho para o arquivo csv em que os resultados serão armazenados")
) -> None:
    '''
    Prepara um dispositivo para ser o receptor de um teste de performace(throughput, delay e perca de pacotes). Assim que ocorrer o fim do teste os dados coletados podem ser armazenados.
    O processo se encerra após a quantidade de execuções(execution_number) definido no dispositvo que envia os pacotes do teste(throughputsender).
    '''
    echo(message="Começando o processo de receber pacotes para o teste de throughput \n\n")
    local = ZigBeeDevice(port, baud_rate=115200)
    try:
        local.open()
        throughput_receiver(local, dest_file)
    finally:
        if local is not None and local.is_open():
            local.close()
            
    
@cli.command()
def plotThroughput(
    src_file: str = Argument(..., help="caminho para o arquivo csv em que os dados serão retirados para a plotagem"),
    graph_type: str = Argument(..., help="O tipo de gráfico a ser plotado, podendo assumir o valor de 'histogram', 'violin ou line")
):
    '''
    Desenha um gráfico violino ou histogarama do throughput de acordo com um arquivo CSV retirado de um teste de performace feito pela ferramenta.
    '''
    plot_throughput_data(src_file, graph_type)
    
@cli.command()
def plotDelay(
    src_file: str = Argument(..., help="caminho para o arquivo csv em que os dados serão retirados para a plotagem"),
    graph_type: str = Argument(..., help="O tipo de gráfico a ser plotado, podendo assumir o valor de 'histogram', 'violin ou line"),
):
    '''
    Desenha um gráfico de linha do delay de acordo com um arquivo CSV retirado de um teste de performace feito pela ferramenta.
    '''
    plot_delay_data(src_file, graph_type)
    

@cli.command()
def plotPacketLoss(
    src_file: str = Argument(..., help="caminho para o arquivo csv em que os dados serão retirados para a plotagem"),
    graph_type: str = Argument(..., help="O tipo de gráfico a ser plotado, podendo assumir o valor de 'histogram', 'violin ou line"),
):
    '''
    Desenha um gráfico de linha do delay de acordo com um arquivo CSV retirado de um teste de performace feito pela ferramenta.
    '''
    plot_packet_loss_data(src_file, graph_type)
