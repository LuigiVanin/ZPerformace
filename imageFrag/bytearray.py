prime_numbers = [2, 3, 5, 7]
a = bytearray(prime_numbers)
b = [a, a]
c = bytearray(a[:])
print(c)
for i in a:
	c.append(i)
#c.append(a)
#print(prime_numbers[:2])
#print(b)
print(c[1:])
