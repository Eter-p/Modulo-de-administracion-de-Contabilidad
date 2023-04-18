import os

from reporte import crearReporte
from ABC import obtenerAgente,agregarAgente, eliminarAgente, cambiarInfoAgente
from trafico import capturarTrafico

if (not os.path.exists("Agentes")):
	os.mkdir("Agentes")

print("""\nSistema de Administracion de red
Practica 2 - Trafico de Red
Fabian Hernandez Hernandez 4CM14 2019630344""")

while(True):
	print("\n********** Menu **********\n")
	print("1. Agregar Agente")
	print("2. Eliminar Agente")
	print("3. Cambiar informacion de un Agente")
	print("4. Generar Reporte")
	print("5. Salir")

	opcion = input("\nElije una opcion: ")
	if opcion == str(1):
		agregarAgente()
	elif opcion == str(2):
		eliminarAgente()
	elif opcion == str(3):
		cambiarInfoAgente()
	elif opcion == str(4):
		agente = obtenerAgente()
		lapso = capturarTrafico(agente)
		if (lapso[2]):
			crearReporte(lapso,agente)
	elif opcion == str(5):
		break
	else:
		print("\n!!! Opcion no valida !!!")