import os
import rrdtool
import time
from getSNMP import consultaSNMP
from ReadWrite import leerArchivo

if (not os.path.exists("Agentes")):
	os.mkdir("Agentes")
        
while 1:
    listaAgentes = os.listdir("Agentes/")
    for x in listaAgentes:
        nomBase = "baseDatos"+x+".rrd"
        #si no exite alguna base la crea
        if (not os.path.isfile(nomBase)):
            ret = rrdtool.create(nomBase,
                            "--start",'N',
                            "--step",'60',
                            "DS:Multicast:COUNTER:120:U:U",
                            "DS:IP:COUNTER:120:U:U",
                            "DS:ICMP:COUNTER:120:U:U",
                            "DS:TCP:COUNTER:120:U:U",
                            "DS:UDP:COUNTER:120:U:U",
                            "RRA:AVERAGE:0.5:5:5",
                            "RRA:AVERAGE:0.5:1:20")
        rrdtool.dump(nomBase,nomBase[:-4]+".xml")

        #actualiza las bases de datos
        datos = leerArchivo("Agentes/"+x)
        if (not bool(datos)):
            continue
        sistema = consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.1.1.0')
        paquetesMulticast = int( consultaSNMP(datos[0],datos[3],
                                    '1.3.6.1.2.1.2.2.1.18.'+("2" if "Linux" in sistema else "16")).split()[2])
        paquetesIP = int(consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.4.9.0').split()[2])
        mensajesICMP = int(consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.5.1.0').split()[2])
        segmentosTCP = int(consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.6.12.0').split()[2])
        datagramasUDP = int(consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.7.4.0').split()[2])

        valor = "N:" + str(paquetesMulticast) + ':' + str(paquetesIP) + ':' + str(mensajesICMP) + ':' + str(segmentosTCP) + ':' + str(datagramasUDP)
        print (x+": "+valor)
        rrdtool.update(nomBase, valor)
        rrdtool.dump(nomBase,nomBase[:-4]+".xml")
        time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)