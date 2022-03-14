import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
        plt.xlabel('ThroughPut(Kpbs)') 
        plt.ylabel('Incidência de Valores')
    elif style == "violin":
        ax.violinplot(data)
        plt.title("Gráfico Violino da incidência do throughput(Kpbs) das iterações")
        plt.ylabel('Incidência de Valores')
        plt.ylabel('ThroughPut(Kpbs)') 
    elif style == "line":
        ax.plot(data)
        plt.title("Histograma da incidência do throughput(Kpbs) das iterações")
        plt.ylabel('ThroughPut(Kpbs)') 
        plt.xlabel('Número da iteração')
    else:
        print("Invalid graph style")
        return
        
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

