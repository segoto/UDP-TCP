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
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 11000
    server_address =(host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




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
    s.sendto(message_prep.encode('utf-8'), server_address)

    # Hash
    dataHash, server = s.recvfrom(2048)
    packagesExpected, server = s.recvfrom(2048)
    packages = int(packagesExpected.decode('utf-8'))
    print(dataHash)
    print(packagesExpected)
    # Data

    with open('outputFile.zip', 'wb') as f:
        logClient.write('\nNombre del archivo\n')
        logClient.write('output100.zip')
        logClient.write('\nDireccion del cliente\n')
        logClient.write(socket.gethostbyname(socket.gethostname()))

        start_time = datetime.now()
        data, server = s.recvfrom(4096)
        contador = 1
        try:
            while data:
                print(contador)
                f.write(data)
                s.settimeout(2)
                data, server = s.recvfrom(4096)
                contador += 1
        except socket.timeout:
            logClient.write('\nCantidad paquetes esperados '+ str( packages)+'\n')
            logClient.write('\nCantidad de pauetes recibidos\n')
            logClient.write(str(contador))
            logClient.write('\nTiempo APROXIMADO de llegada\n')
            logClient.write(str(millis(start_time)))
            logClient.write('\nTamanio del archivo\n')
            logClient.write(str(os.stat('outputFile.zip').st_size))
        with open('outputFile.zip', 'rb') as f1:
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
