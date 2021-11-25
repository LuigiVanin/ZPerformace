from typing import List, Optional, Tuple
from digi.xbee import devices
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice, XBeeMessage
from time import time
from ..utils import array_mean, print_results
import csv


def throughput_sender(
    local: ZigBeeDevice,
    remote: RemoteZigBeeDevice,
    rep_amount: Optional[int] = None,
    disable_messages: bool = False
) -> None:
    print(remote.get_node_id())
    
    if rep_amount is None:
        rep_amount = 100
        
    pack_amount = 100
    payload = "!ufW8hs<P=jxLR$55KrKVh5bvc>yxLR$55KrKVh5bvc>y<gRDiDsb%kg~}1$A}S5&Fk"
    local.send_data(remote, "START_{}".format(rep_amount))

    for i in range(rep_amount):
        
        local.send_data_async(remote, "begin_{}".format(i + 1))    
        for _ in range(pack_amount):
            local.send_data(remote, "{}-{}".format(payload, time()))
        local.send_data_async(remote, "end_")
        if not disable_messages : print("packet {} sended!".format(i+1)) 
    input()

_pack_amount = 100
_rep_amount = 100
_pack_count = 0
_rep_count = 0
_data: List[Tuple] = []
_delta_times: List[float] = []


def __receive_callback(message: XBeeMessage):
    global _pack_count,_pack_amount, _rep_amount, _rep_count
    global _data, _delta_times
    size: int = 100
    msg: str = message.data.decode()
    idx = msg.find("_")
    
    if(idx == -1):
        _pack_count += 1
        time_idx = msg.find("-")
        start_time = float(msg[time_idx+1: len(msg)])
        _delta_times.append(time() - start_time)

    else:
        if msg[:idx] == "begin":
            _pack_count = 0
            _delta_times = []
            print("começo do teste {}".format(_rep_count + 1))
            
        elif msg[:idx] == "end":
            _rep_count+=1
            data = (
                _pack_amount - _pack_count,
                "{}%".format((_pack_amount - _pack_count) / _pack_amount),
                array_mean(_delta_times),
            )
            _data.append(data)
            
            print("fim do  teste {}\n".format(_rep_count))
            
            if _rep_amount == _rep_count : print(
                "\n---FIM DO PROGRAMA---\nPress Enter For Results"
            )
            
        elif msg[:idx] == "START":
            size = int(msg[idx+1 : len(msg)])
            _pack_count = 0
            _rep_count = 0
            _rep_amount = size
            _delta_times = []
            _data = []
    

def throughput_receiver(
    local:ZigBeeDevice, 
    file_dest:Optional[str]=None
):
    global _pack_count, _rep_amount, _rep_count, _delta_times
    local.add_data_received_callback(__receive_callback)
    input()
    
    header = [
        'Packet Loss',
        'Loss Percentage(%)',
        'Time Delta Mean(ms)'
    ]
    if file_dest is not None:
        try:
            with open(file_dest, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for i in _data:
                    writer.writerow(i)
        except FileNotFoundError:
            print("Erro: Problema ao encontrar o arquivo {}".format(file_dest))        
        
    print(_pack_count, _rep_count)
    print_results(_data, header)