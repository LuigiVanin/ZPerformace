from typing import Any, Optional, Union, List, Tuple
from time import time
from secrets import choice
import pandas as pd

number = Union[int, float]

def array_mean(array: List[number]) -> number:
    sum: Union[int, float] = 0
    for i in array:
        sum+= i

    return sum/len(array)


def array_sum(array: List[number]) -> number:
    sum = 0
    for i in array:
        sum+=i

    return sum


def print_results(
    results:List[Tuple[Any]],
    header:Optional[List[str]]=None,  
)->None:
    row_len: int
    if header is None:
        row_len = len(results[0])
    else:
        row_len = len(header)
        for idx, item in enumerate(header):
            if idx < row_len - 1:
                print(item, end=", ")
            else:
                print(item, end=";\n")

    for row in results:
        for i, item in enumerate(row):
            if i < row_len - 1:
                print(item, end=", ")
            else:
                print(item, end=";\n")


def packet_generator(length: int) -> str:
    ascii_let: List[str] = [chr(i).lower() for i in range(65, 91)]
    time_size = len("{:.7f}".format(time()))
    packet = ''
    for _ in range(length-(time_size+1)):
        packet = packet + choice(ascii_let)
        
    return packet


def file_name_conc(file_dest, i):
	mensage = file_dest.split("/")
	tam = len(mensage)
	final_ = mensage.pop(tam-1)
	final_no_dot = final_.split(".")[0] 
	path = "/".join(mensage) + "/"
	part  = "_" + i[0] + "_" + i[1] + "_" + i[2] + ".csv"
	dest_file = path + final_no_dot + part
	return dest_file

#
def path_name_conc(file_dest):
	mensage = file_dest.split("/")
	tam = len(mensage)
	mensage.pop(tam-1)
	path = "/".join(mensage) + "/"
	return path

#Função utilizada para retirar o símbolo % da coluna 'packet loss %'
def dataCleaner(pandas):
	cont = 0
	pandinha = pandas.loc[:]

	for i in pandas:
		pandinha[cont] = float( pandinha[cont].split("%")[0] )
		cont += 1

	return pandinha



	
