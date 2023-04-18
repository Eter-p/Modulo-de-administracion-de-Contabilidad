import rrdtool
import time
import os

def dibujarGraficas(inicio,fin,agente):
    tiempo_final = int(time.mktime(fin))
    tiempo_inicial = int(time.mktime(inicio))
    
    if (not os.path.exists("Graficas")):
        os.mkdir("Graficas")
	
    ret = rrdtool.graph( "Graficas/paquetesMulticast.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Bytes/s",
                     "--title=Paquetes multicast que ha enviado\nla interfaz de la interfaz de red de un agente",
                     "DEF:multicast=baseDatos"+agente[8:]+".rrd:Multicast:AVERAGE",
                     "CDEF:escalaMulticast=multicast,8,*",
                     "LINE5:escalaMulticast#FF0000:Tráfico Multicast")

    ret = rrdtool.graph( "Graficas/paquetesIP.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Bytes/s",
                     "--title=Paquetes IP que los protocolos locales (incluyendo ICMP)\nsuministraron a IP en las solicitudes de transmisión.",
                     "DEF:ip=baseDatos"+agente[8:]+".rrd:IP:AVERAGE",
                     "CDEF:escalaIP=ip,8,*",
                     "LINE5:escalaIP#00FF00:Tráfico IP")

    ret = rrdtool.graph( "Graficas/mensajesICMP.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Bytes/s",
                     "--title=Mensajes ICMP que ha recibido el agente",
                     "DEF:icmp=baseDatos"+agente[8:]+".rrd:ICMP:AVERAGE",
                     "CDEF:escalaICMP=icmp,8,*",
                     "LINE5:escalaICMP#0000FF:Tráfico ICMP")

    ret = rrdtool.graph( "Graficas/segmentosTCP.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Bytes/s",
                     "--title=Segmentos retransmitidos; es decir, el número\nde segmentos TCP transmitidos que contienen uno\no más octetos transmitidos previamente",
                     "DEF:tcp=baseDatos"+agente[8:]+".rrd:TCP:AVERAGE",
                     "CDEF:escalaTCP=tcp,8,*",
                     "LINE5:escalaTCP#FFF000:Tráfico TCP")

    ret = rrdtool.graph( "Graficas/datagramasUDP.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Bytes/s",
                     "--title=Datagramas UDP enviados por el dispositivo",
                     "DEF:udp=baseDatos"+agente[8:]+".rrd:UDP:AVERAGE",
                     "CDEF:escalaUDP=udp,8,*",
                     "LINE5:escalaUDP#0FFFF0:Tráfico UDP")

def modificarLapso(tiempo):
	temp = list(tiempo)
	while(True):
		print("\n1. Modificar fecha")
		print("2. Modificar hora")
		print("3. Guardar")
		opcion = input("\nElije una opcion: ")
		if opcion == str(1):
			fecha = input("Coloque una fecha (formato: aaaa mm dd): ")
			temp[0:3] = [int(x) for x in fecha.split()]
		elif opcion == str(2):
			hora = input("Coloque una hora (formato : hh mm ss): ")
			horario = hora.split()
			#no se porque al convertirlo a "struct_time" de nuevo el reloj se adelanta 6 horas
			horario[0]=int(horario[0])-6
			#esta linea es para corregirlo pero si no se adelanta en su sistema comente la linea de arriba
			temp[3:6] = [int(x) for x in horario]
		elif opcion == str(3):
			return time.gmtime(time.mktime(tuple(temp)))
		else:
			print("\n!!! Opcion no valida !!!")

def capturarTrafico(agente):
	global actual,inicio,fin
	actual = time.time()-21600
	fin = time.gmtime(actual)
	inicio = time.gmtime(actual-600)
	while(True):
		print("\nFecha y hora de inicio:\t"+time.asctime(inicio))
		print("Fecha y hora de fin:\t"+time.asctime(fin))
		print("\n1. Modificar inicio")
		print("2. Modificar fin")
		print("3. Crear graficas")
		print("4. Regresar")
		opcion = input("\nElije una opcion: ")
		if opcion == str(1):
			inicio = modificarLapso(inicio)
		elif opcion == str(2):
			fin = modificarLapso(fin)
		elif opcion == str(3):
			dibujarGraficas(inicio,fin,agente)
			return [inicio,fin,True]
		elif opcion == str(4):
			return [0,0,False]
		else:
			print("\n!!! Opcion no valida !!!")