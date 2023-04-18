import os
from ReadWrite import escribirArchivo, leerArchivo

def obtenerAgente():
	listaAgentes = os.listdir("Agentes/")
	if len(listaAgentes) == 0:
		print("!!! No exiten Agentes !!!")
		exit()
	print("Indice\tAgente")
	i=0
	for agente in listaAgentes:
		i+=1
		print(str(i)+".\t"+agente)
	nAgente = input("\nElija un agente (indice): ")
	nomAgente = "Agentes/"+listaAgentes[int(nAgente)-1]
	return nomAgente

def agregarAgente():
	print("\n***** Agregar Agente *****\n")
	totalAgentes = 0
	datos = list()
	datos.append(input("Comunidad: "))
	datos.append(input("Version de SNMP: "))
	datos.append(input("Puerto: "))
	datos.append(input("IP: "))
	existeAgente = True
	while existeAgente:
		totalAgentes+=1
		rutaArchivo = "Agentes/Agente"+str(totalAgentes)
		if(not os.path.exists(rutaArchivo)):
			escribirArchivo(datos,rutaArchivo)
			existeAgente = False
	print("\n!!!! Agente Agregado !!!")
	
def eliminarAgente():
	print("\n***** Elmininar Agente *****\n")
	os.remove(obtenerAgente())
	print("\n!!! Agente eliminado !!!")

def cambiarInfoAgente():
	nomAgente = obtenerAgente()
	datos = leerArchivo(nomAgente)
	while(True):
		print("Indice\tDato")
		print("1.\tComunidad: "+datos[0])
		print("2.\tVersion de SNMP: "+datos[1])
		print("3.\tPuerto: "+datos[2])
		print("4.\tIP: "+datos[3])
		print("5.\tGuardar\n")
		ndato = input("Que valor desea cambiar (indice): ")
		if int(ndato)<1 or int(ndato)>5:
			print("\n!!! Opcion no valida!!!\n")
			continue
		if ndato==str(5):
			break
		datos[int(ndato)-1] = input("Nuevo valor: ")
		print("\n!!! Valor cambiado !!!\n")
	escribirArchivo(datos,nomAgente)
	print("\n!!! Archivo Agente Actualizado !!!")