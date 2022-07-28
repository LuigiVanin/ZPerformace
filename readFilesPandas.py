import pandas as pd
import matplotlib.pyplot as mp
import glob

df_list = []

path = "data/"
fileOut = "graphs/medias.csv"

csv_files = glob.glob(path + "/*.csv")
for file in csv_files:
	f = pd.read_csv(file)
	newF = pd.DataFrame()
	#print(f["Tamanho de pacote"].mean())
	newF["Tamanho de pacote"] =           int(f["Tamanho de pacote"].mean())
	newF["Média de Packet Loss"] =        f["Packet Loss"].mean()
	newF["Média de Loss Percentage(%)"] = "0" 	#f["Loss Percentage(%)"].mean()
	newF["Média do Time Delta Mean(s)"] = f["Time Delta Mean(s)"].mean()
	newF["Média do Total Time(s)"] =      f["Total Time(s)"].mean()
	newF["Média de Total Bytes(B)"] =     f["Total Bytes(B)"].mean()
	newF["Média do Throughput(Kbps)"] =   f["Throughput(Kbps)"].mean()
	
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
