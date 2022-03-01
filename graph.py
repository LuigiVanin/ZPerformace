import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

database = pd.read_csv("./data/sample_data_84.csv")
data = database["Throughput(Kbps)"]

graph = plt.hist(data, bins=5)
print(graph)
plt.title("Histograma da incidência do throughput(Kpbs) das iterações")
plt.xlabel('ThroughPut(Kpbs)') 
plt.ylabel('Incidência de Valores')
plt.show()

print(data)
