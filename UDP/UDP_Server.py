import socket
import hashlib
from datetime import datetime
from threading import Thread
import math as mt
clientSupported = int(input('Cuantos clientes desea en simultaneo \n'))
file = int(input('Que archivo quiere enviar(100MiB o 200MiB)? 1/2'))
ConnectedClients = []
numberClientsConnected = 0


dd = open('100MB.zip', 'rb')
contenido1 = dd.read()
dd2 = open('200MB.zip', 'rb')
contenido2 = dd2.read()
m1 = hashlib.sha256();
m1.update(contenido1)
dig1 = m1.digest();
print(m1.digest_size, '100 mb')
m2 = hashlib.sha256();
m2.update(contenido2)
dig2 = m2.digest()
print(m2.digest_size, '200 mb')

def millis(start_time):
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms


class Client(Thread):
    def __init__(self, s,addr):
        Thread.__init__(self)
        self.s = s
        self.addr = addr
    def run(self):
        logServer = open('logServer.txt', 'a')
        logServer.write('---------------------------------')
        # Tamanio del archivo



        # reverse the given string from client
        if file == 1:
            print(dig1)
            self.s.sendto(dig1, self.addr)
            packages = str(mt.ceil(10000000000/4096))
            self.s.sendto(packages.encode('utf-8'), self.addr)
            with open('100MB.zip', 'rb') as de:
                start_time = datetime.now()
                contenido = de.read(4096)

                contador = 0
                print(contenido, contador)
                while contenido:
                    self.s.sendto(contenido, self.addr)
                    contenido = de.read(4096)
                    contador += 1
                    print(contenido, contador)
            print(contador)
            logServer.write('Tiempo en enviar los paquetes\n')
            logServer.write(str(millis(start_time)))
            logServer.write('\nCantidad de paquetes enviados\n')
            logServer.write(str(contador))
        else:
            # with open('500.mp4','rb') as dd:
            print(dig2, 'dig2')
            self.s.sendto(dig2, self.addr)
            packages = str(mt.ceil(20000000000 / 4096))
            self.s.sendto(packages.encode('utf-8'), self.addr)
            with open('200MB.zip', 'rb') as de:
                contenido = de.read(4096)
                start_time = datetime.now()
                contador = 0
                while contenido:
                    self.s.sendto(contenido, self.addr)
                    contenido = de.read(4096)
                    contador += 1
                    logServer.write('Tiempo en enviar los paquetes\n')
                    logServer.write(str(millis(start_time)))
            logServer.write('\nCantidad de paquetes enviados\n')
            logServer.write(str(contador))
        print('En Cliente recibio el archivo correctamente')
        logServer.close()


def Main():
    global ConnectedClients
    global numberClientsConnected
    host = '127.0.0.1'
    port = 11000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    print('Esperando los',clientSupported,'Clientes')
    while numberClientsConnected<clientSupported:
        data,addr = s.recvfrom(1024)
        if data.decode('utf-8')== 'Preparado para recibir':
            c = Client(s,addr)
            ConnectedClients.append(c)
            numberClientsConnected += 1
    for x in ConnectedClients:
        x.start()




if __name__ == '__main__':
    Main()


