import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_throughput_data(dest_file: str, style: str="hist"):
    database = pd.read_csv(dest_file)
    if style == "hist":
        plt.hist(database["Throughput(Kbps)"], bins=5)
        plt.title("Histograma da incidência do throughput(Kpbs) das iterações")
        plt.xlabel('ThroughPut(Kpbs)') 
        plt.ylabel('Incidência de Valores')
    # elif style == "violin":
        
    plt.show()
    return

