from typing import List, Optional, Tuple
from digi.xbee import devices
from digi.xbee.devices import RemoteZigBeeDevice, ZigBeeDevice, XBeeMessage
from time import time
from ..utils import array_mean, array_sum, print_results, packet_generator, file_name_conc, path_name_conc
import csv
import os

#packet_size  quantidade de bytes
#pack_amount  quantidade de pacotes
#rep_amount   quantidade de testes
def throughput_sender(
	local: ZigBeeDevice,
	remote: RemoteZigBeeDevice,
	packet_size: str = 84,
	pack_amount: int = 100,
	rep_amount:  int = 3,
	disable_messages: bool = False
) -> None:
	#if rep_amount is None : rep_amount = 30
	
	if packet_size.find("-") != -1:
		size = packet_size.split('-')
		minimo = int(size[0])
		maximo = int(size[1]) + 1
	else:
		minimo = int(packet_size)
		maximo = 1 + minimo

	for tam in range(minimo, maximo):
		local.send_data(remote, "config/{}/{}/{}".format(tam, pack_amount, rep_amount))

		payload = packet_generator(tam)
		local.send_data(remote, "START_{}".format(rep_amount))

		for i in range(rep_amount):
			local.send_data_async(remote, "begin_{}".format(i + 1))
			for _ in range(pack_amount):
				local.send_data(remote, "{}-{:.7f}".format(payload, time()))
			local.send_data(remote, "end_")
			if not disable_messages : print("teste {} enviado!".format(i+1))
	local.send_data(remote, "real_end_")
	print("---FIM DO PROGRAMA---")

_pack_amount = -1
_rep_amount = 100
_pack_count = 0
_rep_count = 0
_data: List[Tuple] = []
_delta_times: List[float] = []
_time_total: float = 0
_total_bytes = 0
_bit_value = 0
_configs_ = []

def __receive_callback(message: XBeeMessage):
    global _pack_count,_pack_amount, _rep_amount, _rep_count, _bit_value
    global _data, _delta_times, _time_total, _total_bytes
    global _configs_
    size: int = 50
    msg: str = message.data.decode()
    idx = msg.find("_")
    
    if msg.find("config") != -1:
    	dados = msg.split("/")
    	_pack_amount = int(dados[2])
    	_bit_value = 0
    	_pack_count = 0
    	_configs_.append(dados[1:])
    
    elif(idx == -1):
        if _bit_value == 0:
            _bit_value = len(msg)
        _pack_count += 1
        time_idx = msg.find("-")
        start_time = float(msg[time_idx+1: len(msg)])
        _delta_times.append(time() - start_time)

    else:
        if msg[:idx] == "begin":
            _pack_count = 0
            _delta_times = []
            # TODO: find a way to remove _time_total and _total_bps
            _time_total = 0
            _total_bytes = 0
            print("começo do teste {} - {}".format(_rep_count + 1, _bit_value))
            
        elif msg[:idx] == "end":
            _rep_count+=1
            _time_total = array_sum(_delta_times)
            _total_bytes = (_bit_value*_pack_count)
            data = (
                _pack_amount - _pack_count,
                "{}%".format((_pack_amount - _pack_count) / _pack_amount),
                array_mean(_delta_times),
                _time_total,
                _total_bytes,
                ((_total_bytes*8)/1000)/_time_total
            )
            _data.append(data)
            
            print("fim do  teste {}\n".format(_rep_count))
            
        elif msg[:idx] == "START":
            size = int(msg[idx+1 : len(msg)])
            _pack_count = 0
            _rep_count = 0
            _rep_amount = size
            _delta_times = []
            if len(_data) == 0 : _data = []
        
        elif msg.find("real_end_") != -1 : print(
            "\n---FIM DO PROGRAMA---\nPress Enter For Results"
        )
    

def throughput_receiver(
    local:ZigBeeDevice, 
    file_dest: str = "./data/data.csv"
):
	global _pack_count, _rep_amount, _rep_count, _delta_times, _time_total
	global _configs_
	local.add_data_received_callback(__receive_callback)
	input()

	header = [
		'Packet Loss',
		'Loss Percentage(%)',
		'Time Delta Mean(s)',
		'Total Time(s)',
		'Total Bytes(B)',
	'Throughput(Kbps)'
	]
    
	if file_dest is not None:
		try:
			path = path_name_conc(file_dest)
			if not os.path.exists(path):
				os.mkdir(path)

			quant = int(_configs_[0][2])

			for i, j in zip(_configs_, range(len(_configs_))):
				dest_file = file_name_conc(file_dest, i)
				with open(dest_file, 'a', newline="") as f:
					writer = csv.writer(f)
					writer.writerow(header)
					for k in range(int(_configs_[j][2])):
						writer.writerow(_data[j*quant+k])
		except FileNotFoundError:
			print("Erro: Problema ao encontrar o arquivo {}".format(file_dest))        
        
	if file_dest is not None : print("Resultados enviados para o arquivo: {}".format(file_dest))
	#print_results(_data, header)
   





