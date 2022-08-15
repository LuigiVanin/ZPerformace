import os
import io
import PIL.Image as Image
import sys

from array import array

import PIL

"""
an_image = PIL.Image.open("image.jpeg")
another_image = PIL.Image.open("imageOutput.jpeg")

#print(an_image)
#print(another_image)
#print(an_image == another_image)

with open("image.jpeg", "rb") as image:
	b = bytearray(image.read())
	
image = Image.open(io.BytesIO(b))
image.save("imageOutput.jpeg")

with open("imageOutput.jpeg", "rb") as image:
	c = bytearray(image.read())

image = Image.open(io.BytesIO(c))
image.save("newImageOutput.jpeg")


for i, j in zip(b, c):
	if i != j:
		print(i, j)
		print("ERROR")
		break
"""

with open("imageOutput.jpeg", "rb") as image:
	b = bytearray(image.read())
pacote = ""
predictedPacket = ""
array = []
for i in b:
	predictedPacket = pacote + str(i) + "/"
	if sys.getsizeof(predictedPacket) > 84:
		#device.send_data(remote, pacote)
		###
		array.append(pacote)
		###
		pacote = ""
		#time.sleep(0.5) #pq?
	pacote += str(i) + "/"
array.append(pacote)
#imageOutput = "imageFrag/imageOutput.png"
pacote = ""
#fim = False
#array = []
#finalizar = bytearray(b'fim!!!')

"""
while not fim:
	device_message = device.read_data()
	if device_message != None:
		if device_message.data != finalizar:
			array.append(device_message)
			#pacote += device_message.data.decode()
		else:
			fim = True
			#print(device_message.data == bytearray(b'fim!!!'))
"""
for i in array:
	pacote += i
	#print("oi")

splittedPacket = pacote.split("/")
splittedPacket.pop(len(splittedPacket)-1)
		
arrayImage = []

for point in splittedPacket:
	arrayImage.append(int(point))

bytearrayImage = bytearray(arrayImage)
#print(bytearrayImage)
image = Image.open(io.BytesIO(bytearrayImage))
image.save("newImageOutput.jpeg")
			
			

