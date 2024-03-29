from typer import Typer, Argument, echo
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice
from digi.xbee.util.utils import hex_to_string
from ..core.tests.throughput import throughput_receiver, throughput_sender
from ..core.plot import plot_throughput_data, plot_delay_data, plot_packet_loss_data, generateData, menuPlot
from ..core.features import checkAllDevices, returnDevice
#from imageFrag.dataCommunication import sender, receiver
from imageFrag.dataCommunicationBytearray import sender, receiver
from typing import Optional
import time

import os
import io
import PIL.Image as Image
import sys

from array import array

cli = Typer()

@cli.command()
def checkDevices(
) -> None:
	'''
	Verifica se existe algum dispositivo conectado e retorna sua porta e nó
	'''
	checkAllDevices()

@cli.command()
def broadcast(
    port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    data: str = Argument(..., help="a mensagem é o texto a ser transmitido via boradcast")
) -> None:
    '''
    Comando que realiza uma mensagem por broadcast a partir do dispositivo a qual a porta foi declarada
    '''
    
    if returnDevice(port, 0) != -1:
    	port = returnDevice(port, 0)
    
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
	if port.find("/dev/") == -1 and returnDevice(port, 0) != -1:
		port = returnDevice(port, 0)
	
	if dest.find("rou") == -1 and returnDevice(dest, 1) != -1:
		dest = returnDevice(dest, 1)

	device = ZigBeeDevice(port, 115200)
	try:
		device.open()
		remote = RemoteZigBeeDevice(device, node_id=dest)
		remote.read_device_info()
		sender(data, device, remote)
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
	
	if port.find("/dev/") == -1 and returnDevice(port, 0) != -1:
		port = returnDevice(port, 0)

	device = ZigBeeDevice(port, 115200)
	try:
		device.open()
		receiver(device)
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
    
    if port.find("/dev/") == -1 and returnDevice(port, 0) != -1:
    	port = returnDevice(port, 0)
    
    if dest.find("rou") == -1 and returnDevice(dest, 1) != -1:
    	dest = returnDevice(dest, 1)
    
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
    port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido")#,
    #dest_file: Optional[str] = "./data/data.csv" #Argument(..., help="Caminho para o arquivo csv em que os resultados serão armazenados")
) -> None:
    '''
    Prepara um dispositivo para ser o receptor de um teste de performace(throughput, delay e perca de pacotes). Assim que ocorrer o fim do teste os dados coletados podem ser armazenados.
    O processo se encerra após a quantidade de execuções(execution_number) definido no dispositvo que envia os pacotes do teste(throughputsender).
    '''
    
    if port.find("/dev/") == -1 and returnDevice(port, 0) != -1:
        port = returnDevice(port, 0)
    
    echo(message="Começando o processo de receber pacotes para o teste de throughput \n\n")
    local = ZigBeeDevice(port, baud_rate=115200)
    try:
        local.open()
        #throughput_receiver(local, dest_file)
        throughput_receiver(local)
    finally:
        if local is not None and local.is_open():
            local.close()
            
    
@cli.command()
def plotThroughput(
    src_file: str = Argument(..., help="Caminho para o arquivo csv em que os dados serão retirados para a plotagem"),
    graph_type: str = Argument(..., help="O tipo de gráfico a ser plotado, podendo assumir o valor de 'histogram', 'violin ou line")
):
    '''
    Desenha um gráfico violino ou histogarama do throughput de acordo com um arquivo CSV retirado de um teste de performace feito pela ferramenta.
    '''
    plot_throughput_data(src_file, graph_type)
    
@cli.command()
def plotDelay(
    src_file: str = Argument(..., help="Caminho para o arquivo csv em que os dados serão retirados para a plotagem"),
    graph_type: str = Argument(..., help="O tipo de gráfico a ser plotado, podendo assumir o valor de 'histogram', 'violin ou line"),
):
    '''
    Desenha um gráfico de linha do delay de acordo com um arquivo CSV retirado de um teste de performace feito pela ferramenta.
    '''
    plot_delay_data(src_file, graph_type)
    

@cli.command()
def plotPacketLoss(
    src_file: str = Argument(..., help="Caminho para o arquivo csv em que os dados serão retirados para a plotagem"),
    graph_type: str = Argument(..., help="O tipo de gráfico a ser plotado, podendo assumir o valor de 'histogram', 'violin ou line"),
):
    '''
    Desenha um gráfico de linha do delay de acordo com um arquivo CSV retirado de um teste de performace feito pela ferramenta.
    '''
    plot_packet_loss_data(src_file, graph_type)


@cli.command()
def dataGenerator(
	src_file: str = Argument(None, help="Caminho para a pasta em que os dados serão retirados para a geração dos dados"),
	dest_file: str = Argument(None, help="Caminho para a pasta em que os dados serão gravados"),
) -> None:
	'''
	Gera os dados de média e desvio padrão de uma determinada pasta de arquivos csv e salva em outra pasta.
	'''
	generateData(src_file, dest_file)


@cli.command()
def menuPlotGenerator(
	src_file: str = Argument(None, help="caminho para a pasta em que os dados serão retirados para a geração dos dados"),
	opt: str = Argument(None, help="Gerar todos os gráficos"),
) -> None:
	'''
	Ferramenta auxiliar para geração de gráficos.
	'''
	menuPlot(src_file, opt)



