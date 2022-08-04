import pandas as pd
import matplotlib.pyplot as mp
import glob

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
