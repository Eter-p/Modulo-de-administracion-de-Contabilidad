import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer ,Table, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pysnmp.hlapi import *
from getSNMP import consultaSNMP
from ReadWrite import leerArchivo

def crearReporte(lapso,agente):
	datos = leerArchivo(agente)

	doc = SimpleDocTemplate("Reporte"+agente[8:]+".pdf", pagesize = A4)
	estilo1 = ParagraphStyle('estilo1',fontName='Times-Roman',fontSize=24,leading=20)
	estilo2 = ParagraphStyle('estilo2',fontName='Times-Roman',fontSize=12,leading=20)
	story=[]

	#Pagina 1
	P1 = Paragraph("Administracion de Servivios en red", estilo1)
	P2 = Paragraph("Practica 1", estilo1)
	P3 = Paragraph("Fabian Hernandez Hernandez", estilo1)

	descripSistema = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.1.0").split()
	
	sistema = str()
	for x in descripSistema:
		sistema = x
		if ("Linux" in x):
			break
		elif ("Windows" in x):
			break
	
	version = str()
	flag = False
	for x in descripSistema:
		version = x
		if (flag):
			break
		if ("#" in x):
			break
		elif ("Version" in x):
			flag = True
		
	if ("Ubuntu" in version):
		logo = Image('Logos/Ubuntu.jpg', width=100, height=100,hAlign='RIGHT')
	else:
		logo = Image('Logos/Windows.jpg', width=100, height=100,hAlign='RIGHT')
	
	nomDispositivo = descripSistema[3]+" "+descripSistema[4]
	contacto = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.4.0").split()[2]
	ubicacion = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.6.0").split()[2]
	numInterfaces = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.1.0").split()[2]

	P4 = Paragraph("Sistema Operativo: "+sistema+" "+version, estilo2)
	P5 = Paragraph("Dispositivo: "+nomDispositivo, estilo2)
	P6 = Paragraph("Informacion de contacto: " +contacto, estilo2)
	P7 = Paragraph("Ubicacion: "+ubicacion, estilo2)
	P8 = Paragraph("Numero de Interfaces: " +numInterfaces, estilo2)

	datosTabla = [["Interfaz", "Estado"]]
	for x in range(int(numInterfaces)):
		if(x==5):
			break
		fila = list()
		nomInterfaz = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.2.1.2."+str(x+1)).split()[2]
		fila.append(nomInterfaz if sistema == "Linux" else bytearray.fromhex(nomInterfaz[2:]).decode())
		estado = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.2.1.7."+str(x+1)).split()[2]
		if estado=="1":
			fila.append("UP")
		elif estado == "2":
			fila.append("DOWN")
		elif estado == "3":
			fila.append("TESTING")
		else:
			fila.append("ERROR")
		datosTabla.append(fila)

	tabla = Table(data = datosTabla,
				style = [
						('GRID',(0,0),(-1,-1),0.5,colors.grey),
						('BOX',(0,0),(-1,-1),2,colors.black),
						('BACKGROUND', (0, 0), (-1, 0), colors.blue),
						]
				)
	story.append(P1)
	story.append(P2)
	story.append(P3)
	story.append(logo)
	story.append(P4)
	story.append(P5)
	story.append(P6)
	story.append(P7)
	story.append(P8)
	story.append(tabla)
	story.append(Spacer(0,(320 if sistema=="Linux" else 300)))

	#Pagina 2
	P9 = Paragraph("Version: 1", estilo2)
	P10 = Paragraph("Dispositivo: "+nomDispositivo, estilo2)
	P11 = Paragraph("Fecha: "+time.asctime(time.gmtime(time.time()-21600)), estilo2)
	P12 = Paragraph("Fecha y hora de inicio de toma de datos: "+time.asctime(lapso[0]), estilo2)
	P13 = Paragraph("Fecha y hora de final de toma de datos: "+time.asctime(lapso[1]), estilo2)
	P14 = Paragraph("#Paquetes multicast que ha enviado la interfaz de la interfaz de red de un agente", estilo2)
	P15 = Paragraph("#Paquetes IP que los protocolos locales (incluyendo ICMP) suministraron a IP en las solicitudes de transmisión.", estilo2)
	P16 = Paragraph("#Mensajes ICMP que ha recibido el agente. ", estilo2)
	P17 = Paragraph("#Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente", estilo2)
	P18 = Paragraph("#Datagramas enviados por el dispositivo.", estilo2)

	G1 = Image('Graficas/paquetesMulticast.png', width=372, height=126,hAlign='CENTER')
	G2 = Image('Graficas/paquetesIP.png', width=372, height=126,hAlign='CENTER')
	G3 = Image('Graficas/mensajesICMP.png', width=372, height=126,hAlign='CENTER')
	G4 = Image('Graficas/segmentosTCP.png', width=372, height=126,hAlign='CENTER')
	G5 = Image('Graficas/datagramasUDP.png', width=372, height=126,hAlign='CENTER')

	story.append(P9)
	story.append(P10)
	story.append(P11)
	story.append(Spacer(0,20))
	story.append(P12)
	story.append(P13)
	story.append(Spacer(0,20))
	story.append(P14)
	story.append(G1)
	story.append(P15)
	story.append(G2)
	story.append(P16)
	story.append(G3)
	story.append(Spacer(0,50))
	story.append(P17)
	story.append(G4)
	story.append(P18)
	story.append(G5)
	
	doc.build(story)