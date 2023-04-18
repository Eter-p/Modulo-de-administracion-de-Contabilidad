def escribirArchivo(datos,nombreArchivo):
	try:
		archivo = open(nombreArchivo,"w")
	except FileNotFoundError:
		return False
	for x in range(len(datos)-1):
		archivo.write(datos[x]+"\n")
	archivo.write(datos[len(datos)-1])
	archivo.close()

def leerArchivo(nombreArchivo):
	try:
		archivo = open(nombreArchivo,"r")
	except FileNotFoundError:
		return False
	datos = list()
	datosTemp = archivo.readlines()
	for x in datosTemp:
		datos.append(x[:len(x)-1])
	datos[-1] = datosTemp[-1]
	archivo.close()
	return datos
