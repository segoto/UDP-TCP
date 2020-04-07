# Import socket module
import hashlib
import time
import os
import socket
from datetime import datetime

def millis(start_time):
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms


def Main():
    # local host IP '127.0.0.1'
    host = ''

    # Define the port on which you want to connect
    port = 11001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    # Mensaje preparado para recibir
    message_prep = "Preparado para recibir"

    # Mensaje recibido
    message_rec = "Recibido"

    # Mensaje recibido no integro
    message_rec_in = "Mensaje no recibido"
    # Archivo log
    logClient = open('log.txt', 'a')
    logClient.write('---------------------------------------')
    logClient.write('Fecha y hora de la prueba\n')
    logClient.write(time.asctime())

    # message preparado para recibir
    s.send(message_prep.encode('utf-8'))
    ans = input('Que archivo quiere recibir(100MiB o 200MiB)? 1/2\n')
    s.send(str(ans).encode('utf-8'))
    # Hash
    dataHash = s.recv(2048)
    print(dataHash)
    if ans == 1:
        # Data
        print('Entre a 100')
        with open('output100.zip', 'wb') as f:
            logClient.write('\nNombre del archivo\n')
            logClient.write('output100.zip')
            logClient.write('\nDireccion del cliente\n')
            logClient.write(socket.gethostbyname(socket.gethostname()))

            start_time = datetime.now()
            contador = 0
            data = s.recv(4096)
            while data:
                f.write(data)
                data = s.recv(4096)
                contador += 1
            logClient.write('\nCantidad de pauetes recibidos\n')
            logClient.write(str(contador))
            logClient.write('\nTiempo APROXIMADO de llegada\n')
            logClient.write(str(millis(start_time)))
            logClient.write('Tamanio del archivo\n')
            logClient.write(str(os.stat('output100.zip').st_size))
        with open('output100.zip', 'rb') as f1:
            m = hashlib.sha256();
            contenido = f1.read()
            m.update(contenido);
            dig = m.digest();
    else:
        # Data
        with open('output200.zip', 'wb') as f:
            logClient.write('\nNombre del archivo\n')
            logClient.write('output200.zip')
            logClient.write('\nDireccion del cliente\n')
            logClient.write(socket.gethostbyname(socket.gethostname()))

            start_time = datetime.now()
            data = s.recv(4096)
            while data:
                f.write(data)
                data = s.recv(4096)
            logClient.write('\nTiempo APROXIMADO de llegada\n')
            logClient.write(str(millis(start_time)))
            logClient.write('\nTamanio del archivo\n')
            logClient.write(str(os.stat('output200.zip').st_size))
        with open('output200.zip', 'rb') as f1:
            m = hashlib.sha256();
            contenido = f1.read()
            m.update(contenido);
            dig = m.digest();
    if dig == dataHash:
        logClient.write('\nEl archivo llego correctamente\n')
        print('Recibido exitosamente')
    else:
        logClient.write('\nEl archivo NO llego correctamente\n')
        print('No cumple con la integridad:')

        # close the connection
    logClient.close()
    s.close()


if __name__ == '__main__':
    Main()
