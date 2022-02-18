import numpy as np

def d(angle):
	lamb = 0.71073
	print('d spacing:')
	for n in range(1,5):
		d = ((1/n)*lamb)/(2*np.sin(np.math.radians(angle/2)))
		print(d)

def a(spacing):
	lamb = 0.71073
	print('angles')
	for n in range(1,10):
		a = 2*np.math.degrees(np.arcsin((n*lamb)/(2*spacing)))
		print(a)
