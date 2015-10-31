#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    dicc = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        client_infor = self.client_address
        print ('IP: ' + client_infor[0])
        print ('Port: ' + str(client_infor[1]))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line_decod = line.decode('utf-8')
            if (len(line_decod) >= 2):
                if (line_decod.split()[0].upper() == 'REGISTER'):
                    if ('@' in line_decod.split()[1]):
                            self.dicc[line_decod.split()[1]] = client_infor[0]
                    print (self.dicc)
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                else:
                    self.wfile.write(b"Hemos recibido tu peticion\r\n")
                    print("El cliente nos manda " + line_decod)
            else:
                self.wfile.write(b"Hemos recibido tu peticion\r\n")
                print("El cliente nos manda " + line_decod)

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    if PORT < 1024:
        sys.exit("Error: port is invalid")
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
