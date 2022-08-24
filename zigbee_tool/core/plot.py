import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from ..core.utils import dataCleaner

#Gera os gráficos de throughput
def plot_throughput_data(dest_file: str, style: str="hist"):
    props = {
        'facecolor':'blue', 
        'alpha':0.10
    }
    database = pd.read_csv(dest_file)
    data = database["Throughput(Kbps)"]
    _, ax = plt.subplots()
    if style == "hist" or style == "histogram":
        ax.hist(data, bins=5)
        plt.title("Histograma da incidência do throughput(Kpbs) das iterações")
        plt.xlabel('ThroughPut(Kbps)') 
        plt.ylabel('Incidência de Valores')
    elif style == "violin":
        ax.violinplot(data)
        plt.title("Gráfico Violino da incidência do throughput(Kpbs) das iterações")
        plt.ylabel('Incidência de Valores')
        plt.ylabel('ThroughPut(Kbps)') 
    elif style == "line":
        ax.plot(data)
        plt.title("Histograma da incidência do throughput(Kpbs) das iterações")
        plt.ylabel('ThroughPut(Kbps)') 
        plt.xlabel('Número da iteração')
    else:
        print("Invalid graph style")
        return
        
    plt.ylim((0, 20))
    mean = data.mean()
    std = data.std()
    textstr = '\n'.join((
        r'media($\mu)=%.4f$' % (mean, ),
        r'desvio padrão($\sigma)=%.4f$' % (std, )))
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)     
    plt.grid()  
    plt.show()
    return

#Gera os gráficos de delay
def plot_delay_data(dest_file: str, style: str="line"):
    props = {
        'facecolor':'blue', 
        'alpha':0.15
    }
    _, ax = plt.subplots()
    database = pd.read_csv(dest_file)
    data = database["Time Delta Mean(s)"]
    mean = data.mean()
    std = data.std()
    textstr = '\n'.join((
        r'media($\mu)=%.4f$' % (mean, ),
        r'desvio padrão($\sigma)=%.4f$' % (std, )))
    if style == "line":
        ax.plot(data)
        plt.title("Gráfico de Delay de acordo com iteração")
        plt.ylabel('Delay(s)') 
        plt.xlabel('Iteração')
    elif style == "hist" or style == "histogram":
        ax.hist(data, bins=5)
        plt.title("Gráfico de Histrograma do Delay")
        plt.xlabel('Delay(s)') 
        plt.ylabel('Iteração')
    elif style == "violin":
        ax.violinplot(data)
        plt.title("Gráfico de Violino do Delay")
        plt.ylabel('Delay(s)') 
        plt.xlabel('Incidência de Valores')
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    plt.grid()
    plt.show()

#Gera os gráficos de packet loss
def plot_packet_loss_data(dest_file: str, style: str="line"):
    props = {
        'facecolor':'blue', 
        'alpha':0.15
    }
    _, ax = plt.subplots()
    database = pd.read_csv(dest_file)
    data = database["Packet Loss"]
    mean = data.mean()
    std = data.std()
    textstr = '\n'.join((
        r'media($\mu)=%.4f$' % (mean, ),
        r'desvio padrão($\sigma)=%.4f$' % (std, )))
    if style == "line":
        ax.plot(data)
        plt.title("Gráfico de Pacotes Perdido de acordo com iteração")
        plt.ylabel('Pacote Pedido)') 
        plt.xlabel('Iteração')
    elif style == "hist" or style == "histogram":
        ax.hist(data, bins=5)
        plt.title("Gráfico Histograma de Pacotes Perdidos")
        plt.xlabel('Pacote Pedido') 
        plt.ylabel('Incidência de Valores')
    elif style == "violin":
        ax.violinplot(data)
        plt.title("Gráfico de Violino de Pacotes Perdidos")
        plt.ylabel('Pacote Pedido') 
        plt.xlabel('Incidência de Valores')
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    plt.grid()
    plt.show()

#Gera os dados de média e desvio padrão na forma de arquivo csv e os armazena na pasta escolhida
def generateData(src_file: str, dest_file: str):

	if src_file is None : src_file = "./data/"
	if dest_file is None : dest_file = "./graphs/"	
	
	fileOutDP = "desvioPadrao.csv"
	fileOutM = "media.csv"
	csv_files = glob.glob(src_file + "/*.csv")
	#print(csv_files)
	mf = pd.DataFrame()
	dpf = pd.DataFrame()

	for file in csv_files:
		f = pd.read_csv(file)
		dppd = pd.DataFrame({
		"Tamanho do pacote" : [int(f["Tamanho de pacote"].mean())],
		"Desvio Padrão de Packet Loss" : [int(f["Packet Loss"].std())],
		"Desvio Padrão de Loss Percentage(%)" : [ float(dataCleaner(f["Loss Percentage(%)"]).std()) ],
		"Desvio Padrão do Time Delta Mean(s)" : [f["Time Delta Mean(s)"].std()],
		"Desvio Padrão do Total Time(s)" : [f["Total Time(s)"].std()],
		"Desvio Padrão de Total Bytes(B)" : [int(f["Total Bytes(B)"].std())],
		"Desvio Padrão do Throughput(Kbps)" : [f["Throughput(Kbps)"].std()],
		})
		mpd = pd.DataFrame({
		"Tamanho do pacote" : [int(f["Tamanho de pacote"].mean())],
		"Média de Packet Loss" : [int(f["Packet Loss"].mean())],
		"Média de Loss Percentage(%)" : [ float((f["Loss Percentage(%)"]).mean()) ],
		"Média do Time Delta Mean(s)" : [f["Time Delta Mean(s)"].mean()],
		"Média do Total Time(s)" : [f["Total Time(s)"].mean()],
		"Média de Total Bytes(B)" : [int(f["Total Bytes(B)"].mean())],
		"Média do Throughput(Kbps)" : [f["Throughput(Kbps)"].mean()]
		})
		mf = mf.append(mpd)
		dpf = dpf.append(dppd)

	mf = mf.sort_values(by = ["Tamanho do pacote"])
	dpf = dpf.sort_values(by = ["Tamanho do pacote"])

	mf.to_csv(dest_file+fileOutM, index=False)
	dpf.to_csv(dest_file+fileOutDP, index=False)

#Menu interativo para plotagem de gráficos de um arquivo escolhido
def menuPlot(src_file: str, opt: str):
	printAll = False

	if src_file is None and opt is None :
		src_file = "./graphs/media.csv"

	elif src_file == "all" :
		src_file = "./graphs/media.csv"
		printAll = True
	
	elif opt == "all" :
		printAll = True
	
	elif opt != "all" and opt is not None :
		print("Opção não encontrada utilize o comando all")
		return 0 

	try:
		f = pd.read_csv(src_file)
	except:
		print(src_file)
		print("Arquivo não encontrada ou com erro! Verifique o arquivo e tente novamente!")
		return 0

	listaDeColunas = [i for i in f]

	x = 0
	y = 0
	z = 0

	#_, ax = plt.subplots()

	if printAll:
		for i in f:
			if i == listaDeColunas[0]:
				continue
			else:
				string = "Gráfico do(a) " + listaDeColunas[0] + " em relação a(o) " + i
				f.plot(x = listaDeColunas[0], y = i, kind="line", title=string)
			#print(i)
		#f.plot(x = listaDeColunas[0], y = listaDeColunas[6], kind="line", title=string)
		plt.grid()
		plt.show()
		return 0
	else:
		continuar = True
		graficos = []
		
		if len(listaDeColunas) == 0:
			print("Nenhuma coluna encontrada! Verifique o arquivo e tente novamente!")
			return 0
		
		while continuar:
			os.system('clear')
			if len(graficos) !=0 : print("Gráficos a ser(em) plotados: ", graficos)
			
			cont = 1
			print("Menu plot escolha X e Y:")
			for i in f:
				print("({}). {}".format(cont, i))
				cont += 1
			x = int(input("Escolha o valor de X: "))
			cont = 1
			
			for i in f:
				print("({}). {}".format(cont, i))
				cont += 1
			y = int(input("Escolha o valor de Y: "))
	
			print("1. histogram")
			print("2. line")
			print("3. violin")

			z = int(input("Escolha o tipo de gráfico: "))

			_, ax = plt.subplots()
				
			if z == 1:
				#histograma
				ax.hist(f[listaDeColunas[y-1]], bins = len(f[listaDeColunas[y-1]]))
				#print(len(f[listaDeColunas[y-1]]))
				plt.title("Histograma da incidência do throughput(Kpbs) das iterações")
				#plt.xlabel(listaDeColunas[x-1]) 
				#plt.ylabel(listaDeColunas[y-1])
			elif z == 2:
				#line
				ax.plot(f[listaDeColunas[x-1]], f[listaDeColunas[y-1]])
				string = "Gráfico do(a) " + listaDeColunas[x-1] + " em relação a(o) " + listaDeColunas[y-1]
				plt.title(string)
				plt.xlabel(listaDeColunas[x-1])
				plt.ylabel(listaDeColunas[y-1])
			elif z == 3:
				#violin
				ax.violinplot(f[listaDeColunas[x-1]])
				plt.title("Gráfico Violino da incidência do throughput(Kpbs) das iterações")
				plt.ylabel(listaDeColunas[x-1])
				plt.xlabel(listaDeColunas[y-1])
			string = listaDeColunas[x-1] + " x " +  listaDeColunas[y-1]
			graficos.append(string)

			choise = input("Continuar plotando? (s/y) or (n/...)")
			if choise != 'y' and choise != 's':
				continuar = False

		plt.grid()
		plt.show()
			
	return 0


'''
cont = 1
print("Menu plot escolha X e Y:")
for i in f:
	print("({}). {}".format(cont, i))
	cont += 1
	x = int(input("Escolha o valor de X: "))

	cont = 1
for i in f:
	print("({}). {}".format(cont, i))
	cont += 1
	y = int(input("Escolha o valor de Y: "))
			
print("1. line")
print("2. histogram")
print("3. histogram")
			
z = int(input("Escolha o tipo de gráfico: "))
			
if z == 1:
	kinde = "line"
elif z == 2:
	kinde = "hist"
elif z == 3:
	kinde = "violin"
			
f.plot(x = listaDeColunas[x-1], y = listaDeColunas[y-1], kind=kinde)
plt.grid()
plt.show()
'''













































