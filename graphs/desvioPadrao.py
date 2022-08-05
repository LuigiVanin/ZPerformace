import pandas as pd
import matplotlib.pyplot as mp
import glob

df_list = []

path = "../data/"
fileOut = "desvioPadrao.csv"

csv_files = glob.glob(path + "/*.csv")

#dic = {"Tamanho de pacote" : [], "Média de Packet Loss" : [], "Média de Loss Percentage(%)" : [], 
#"Média de Packet Loss" : [], "Média de Loss Percentage(%)" : [], "Média do Time Delta Mean(s)" : [],
#"Média do Total Time(s)" : [], "Média de Total Bytes(B)" : [], "Média do Throughput(Kbps)" : []}

newF = pd.DataFrame()

for file in csv_files:
	f = pd.read_csv(file)
	df2 = pd.DataFrame({
	"Tamanho do pacote" : [int(f["Tamanho de pacote"].mean())],
	"Desvio Padrão de Packet Loss" : [int(f["Packet Loss"].std())],
	"Desvio Padrão de Loss Percentage(%)" : "0%",		#[f["Packet Loss"].mean()],
	"Desvio Padrão do Time Delta Mean(s)" : [f["Time Delta Mean(s)"].std()],
	"Desvio Padrão do Total Time(s)" : [f["Total Time(s)"].std()],
	"Desvio Padrão de Total Bytes(B)" : [int(f["Total Bytes(B)"].std())],
	"Desvio Padrão do Throughput(Kbps)" : [f["Throughput(Kbps)"].std()],
	})
	newF = newF.append(df2)

newF = newF.sort_values(by = ["Tamanho do pacote"])

newF.to_csv(fileOut, index=False)
