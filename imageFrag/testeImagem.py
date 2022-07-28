import os
import io
import PIL.Image as Image
import sys

from array import array

imageInput = "image.jpeg"
fileName = "demofile2.txt"
imageOutput = "imageOutput.jpeg"

with open(imageInput, "rb") as image:
	f = image.read()
	b = bytearray(f)

frags = []
piece = []
cont = 0

print(type(b))

a = bytearray()

for i in b:
	if sys.getsizeof(i) > 28:
		print("aqui")
	cont += 1
	a += bytearray(i)
	piece.append(i)
	if cont % 84 == 0:
		frags.append(piece)
		piece = []
		#print(sys.getsizeof(a))
if piece != []:
	
	frags.append(piece)

fr = bytearray()

for i in frags:
	fr += bytearray(i)

if f != fr:
	print("error")

########################################    IN /|\   |||   OUT \|/     #############


def readimage(path):
	#count = os.stat(path).st_size / 2
	with open(path, "rb") as f:
		return bytearray(f.read())

bytes = readimage(fileName)


image = Image.open(io.BytesIO(bytes))
image.save(imageOutput)
