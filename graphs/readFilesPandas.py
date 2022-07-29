import pandas as pd
import matplotlib.pyplot as mp
import glob

df_list = []

path = "data/"
fileOut = "graphs/medias.csv"

csv_files = glob.glob(path + "/*.csv")

dic = {"Tamanho de pacote" : [], "Média de Packet Loss" : [], "Média de Loss Percentage(%)" : [], 
"Média de Packet Loss" : [], "Média de Loss Percentage(%)" : [], "Média do Time Delta Mean(s)" : [],
"Média do Total Time(s)" : [], "Média de Total Bytes(B)" : [], "Média do Throughput(Kbps)" : []}
newF = pd.DataFrame()

#cont = 0

for file in csv_files:
	f = pd.read_csv(file)
	df2 = pd.DataFrame({
	"Tamanho de pacote" : [int(f["Tamanho de pacote"].mean())],
	"Média de Packet Loss" : [int(f["Packet Loss"].mean())],
	"Média de Loss Percentage(%)" : "0%",		#[f["Packet Loss"].mean()],
	"Média do Time Delta Mean(s)" : [f["Time Delta Mean(s)"].mean()],
	"Média do Total Time(s)" : [f["Total Time(s)"].mean()],
	"Média de Total Bytes(B)" : [f["Total Bytes(B)"].mean()],
	"Média do Throughput(Kbps)" : [f["Throughput(Kbps)"].mean()],
	})
	newF = newF.append(df2)

newF = newF.sort_values(by = ["Tamanho de pacote"])

newF.to_csv(fileOut, index=False)	
	
"""
for file in csv_files:
	#print(file)
	newF = pd.read_csv(file)
	newF["Tamanho de pacote"] = newF['Total Bytes(B)']/100
	#print(newF)
	newF.to_csv(file, index=False)

df_list = (pd.read_csv(file) for file in csv_files)

big_df = pd.concat(df_list)
big_df = big_df.sort_values(by = ['Total Bytes(B)'])

#print(big_df.to_numpy())
#print(big_df.columns)

#['Packet Loss', 'Loss Percentage(%)', 'Time Delta Mean(s)',
#'Total Time(s)', 'Total Bytes(B)', 'Throughput(Kbps)']

big_df.plot(x="Total Bytes(B)", y="Throughput(Kbps)", kind="line")
big_df.plot(x="Total Bytes(B)", y="Total Time(s)", kind="line")


df_list = []

for file in csv_files:
	df = pd.read_csv(file)
	df_list.append(df.mean(axis = 0))

newDf = pd.DataFrame(df_list)
newDf = newDf.sort_values(by = ['Total Bytes(B)'])

newDf.plot(x="Tamanho de pacote", y="Throughput(Kbps)", kind="line")

mp.show()
"""
