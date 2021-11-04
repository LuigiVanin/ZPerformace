import time
from typing import Optional
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice, XBeeMessage
from time import sleep, time


def throughput_sender(local: ZigBeeDevice,
                      remote: RemoteZigBeeDevice,
                      rep_amount: Optional[int] = None,
                      disable_messages: bool = False) -> None:
    if rep_amount is None:
        rep_amount = 100
    # TODO: remove sleep and give production status
    pack_amount = 100
    payload = "!ufW8hs<P=jxLR$55KrKVh5bvc>yxLR$55KrKVh5bvc>y<gRDiDsb%kg~}1$A}S5&Fk"

    for i in range(rep_amount):
        if i != 0 : 
            local.send_data_async(remote, "begin_{}".format(i + 1))  
        else:
            local.send_data(remote, "start_{}".format(rep_amount))
            
        for _ in range(pack_amount):
            local.send_data_async(remote, "{}-{:.6}".format(payload, time()))
        
        local.send_data_async(remote, "end_")
        if not disable_messages : print("packet sended!")
        sleep(1)
        
    print("the process is finished!")
    input()

__pack_amount = 100
__rep_amount = 100
__pack_count = 0
__rep_count = 0

def __receive_callback(message: XBeeMessage):
    global __pack_amount, __rep_amount, __pack_count, __pack_amount
    pack_amount, rep_amount, pack_count, pack_amount = __pack_amount, __rep_amount, __pack_count, __pack_amount

def throughput_receiver(local:ZigBeeDevice):
    pass