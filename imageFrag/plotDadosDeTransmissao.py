import pandas as pd
import matplotlib.pyplot as mp
import glob
import pandas as pd

f = pd.read_csv("data.csv")

#for i in f:
#	print(f[i][0])
#	break
	#for j in i:

f.plot(x="Tamanho da imagem (KB)", y="Throughput Bytes (Kbps)", kind="line")
mp.show()
