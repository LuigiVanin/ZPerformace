from typer import Typer, Argument, echo, Option
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice
from digi.xbee.util.utils import hex_to_string
from ..core.tests.throughput import throughput_receiver, throughput_sender
from ..core.plot import plot_throughput_data

cli = Typer()

@cli.command()
def broadcast(
    port: str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    data: str = Argument(..., help="a mensagem é o texto a ser transmitido via boradcast")
) -> None:
    '''
    comando que realiza uma mensagem por broadcast a partir do dispositivo a qual a posta foi declarada
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
    port:str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    dest: str = Argument(..., help="nome do nó(node id) do destinatário"),
    data: str = Argument(..., help="dados a serem enviados")
) -> None:
    '''
    Manda uma mensagem direta ao dispositivo especificado
    '''
    device = ZigBeeDevice(port, 115200)
    try:
        device.open()
        remote = RemoteZigBeeDevice(device, node_id=dest)
        remote.read_device_info()
        echo(message="O dispositivo encontrado foi:\n- MAC: {}\n- Node ID: {}".format(hex_to_string(remote.get_pan_id()).replace(" ", ""),
                                                                                      remote.get_node_id()))
        device.send_data_async(remote,data=data)
        
    finally:
        if device is not None and device.is_open():
            device.close()


@cli.command()
def throughputSender(
    port:str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    dest:str = Argument(..., help="Nome do nó(node id) do destinatário"),
    packet_length:int = Argument(..., help="Tamanho do pacote a ser enviado"),
    executions_number: int = Argument(..., help="Número de vezes que o teste é executado.")
) -> None:
    '''
    Executa um teste de throughput com pacote definido. As repetições e tamanho das mensagens podem ser alterados.
    Vale salientar que cada iteração do teste(execution_number) envia um total de 100 pacotes/mensagens, com esse valor sendo fixado.
    '''
    
    print("Começando o processo de enviar pacotes para teste de throughput \n\n")
    local = ZigBeeDevice(port, baud_rate=115200)
    try:
        local.open()
        remote = RemoteZigBeeDevice(local, node_id=dest)
        remote.read_device_info()
        throughput_sender(local, remote, executions_number, packet_length)
    finally:
        if local is not None and local.is_open():
            local.close()
            

@cli.command()
def throughputReceiver(
    port:str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    dest_file: str = Argument(..., help="Caminho para o arquivo csv em que os resultados serão armazenados"),
) -> None:
    '''
    Prepara um dispositivo para ser o receptor de um teste de throughput. Assim que ocorrer o fim do teste os dados coletados podem ser armazenados.
    O processo se encerra após a quantidade de execuções(execution_number) definido no dispositvo que envia os pacotes do teste(throughputsender).
    '''
    echo("Começando o processo de receber pacotes para o teste de throughput \n\n")
    local = ZigBeeDevice(port, baud_rate=115200)
    try:
        local.open()
        throughput_receiver(local, dest_file)
    finally:
        if local is not None and local.is_open():
            local.close()
            
    
@cli.command()
def plot_throughput(
    src_file: str = Argument(..., help="caminho para o arquivo csv em que os dados serão retirados para a plotagem")
):
    '''
    Desenha um gráfico de acordo com um arquivo CSV retirado de um teste de throughput.
    '''
    plot_throughput_data(src_file)