import pandas as pd
import matplotlib.pyplot as mp
import glob

dataFile = "desvioPadrao.csv"
newDF = pd.read_csv(dataFile)
newDF = newDF.sort_values(by = ['Tamanho do pacote'])

newDF.plot(x="Tamanho do pacote", y="Desvio Padrão do Throughput(Kbps)", kind="line")
newDF.plot(x="Tamanho do pacote", y="Desvio Padrão do Time Delta Mean(s)", kind="line")

#newDF.plot(x="Tamanho de pacote", y="Throughput(Kbps)", kind="line")

mp.show()
