import os
import io
import PIL.Image as Image
import sys

from array import array

import PIL

imageInput = "image.jpeg"
fileName = "demofile2.txt"
imageOutput = "imageOutput.jpeg"

an_image = PIL.Image.open(imageInput)

output = io.BytesIO()
an_image.save(output, format="jpeg")
image_as_string = output.getvalue()

#print(image_as_string)

a = ""

for i in image_as_string:
	#if a > i:
	a += str(i)
	a += "/"
	#if sys.getsizeof(a) > 84:
	#	print(a)
	#	print(sys.getsizeof(a))
	#	break


#///////////////////////////////////


aa = a.split("/")
aa.pop(len(aa)-1)

ac = []

for i in aa:
	ac.append(int(i))

ad = bytearray(ac)

image = Image.open(io.BytesIO(ad))
image.save(imageOutput)

#p

"""
sla = False

#a = bytearray()

#a = str(b)

#print(a)


for i in b:
	if sys.getsizeof(i) > 28:
		print("aqui")
	a += str(i.to_bytes(8, 'little'))
	#a.append(i)
	continue
	if len(a) == 4:
		#print(sys.getsizeof(a))
		a = str(a)
		if sys.getsizeof(a) > 84:
			print("error")
			#break
		#print(sys.getsizeof(a))
		a = bytearray()
		#break
		
	if sys.getsizeof(a) > 84:
		print("error")
		break


#print(sys.getsizeof(a))
#print(b[0])
"""
#if a != b:
#	print("error")
#print(a)
########################################    IN /|\   |||   OUT \|/     #############


#def readimage(path):
	#count = os.stat(path).st_size / 2
	#with open(path, "rb") as f:
		#return bytearray(f.read())

#bytes = readimage(fileName)
#bytes = bytearray(a)

#image = Image.open(io.BytesIO(bytes))
#image.save(imageOutput)
