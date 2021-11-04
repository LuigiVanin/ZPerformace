from typer import Typer, Argument, echo, Option
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice
from digi.xbee.util.utils import hex_to_string
from ..core.tests.throughput import throughput_sender

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
        echo(message="o dispositivo encontrado foi:\n- MAC: {}\n- Node ID: {}".format(hex_to_string(remote.get_pan_id()).replace(" ", ""),
                                                                                      remote.get_node_id()))
        device.send_data_async(remote,data=data)
        
    finally:
        if device is not None and device.is_open():
            device.close()


@cli.command()
def throughputSender(
    port:str = Argument(..., help="A porta se refere a entrada física a qual o dispositivo está inserido"),
    dest:str = Argument(..., help="nome do nó(node id) do destinatário"),
    rep: int = Argument(..., help="número de repetições que ocorrerão")
) -> None:
    '''
    Executa um teste de throughput em que o pacote é composto por 100 mensagens de n bits
    '''
    local = ZigBeeDevice(port, baud_rate=115200)
    try:
        local.open()
        remote = RemoteZigBeeDevice(local, node_id=dest)
        remote.read_device_info()
        throughput_sender(local, remote, rep)
    finally:
        if local is not None and local.is_open():
            local.close()