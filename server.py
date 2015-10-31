#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import calendar
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    dicc = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        dicc_usuarios = {}
        client_infor = self.client_address
        print ('IP: ' + client_infor[0])
        print ('Port: ' + str(client_infor[1]))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line_decod = line.decode('utf-8')
            if (len(line_decod) >= 2):
                if (line_decod.split()[0].upper() == 'REGISTER'):
                    direction = line_decod.split()[1]
                    expiration = int(line_decod.split()[2])
                    expires = int(time.time()) + expiration
                    time_expiration = time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.gmtime(expires))
                    dicc_usuarios["address"] = client_infor[0]
                    dicc_usuarios["expires"] = time_expiration
                    if (expiration == 0):
                        if (len(self.dicc) != 0):
                            del self.dicc[direction]
                    elif ('@' in direction):
                        self.dicc[direction] = dicc_usuarios
                    print (self.dicc)
                    for usuario in self.dicc:
                        time_now = time.strftime('%Y­%m­%d %H:%M:%S',
                                                 time.gmtime(time.time()))
                        direct = self.dicc[usuario]
                        value = direct["expires"]
                        if (str(time_now) > value):
                            del self.dicc[direction]
                            break
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    self.register2json()
                else:
                    self.wfile.write(b"Hemos recibido tu peticion\r\n")
                    print("El cliente nos manda " + line_decod)
            else:
                self.wfile.write(b"Hemos recibido tu peticion\r\n")
                print("El cliente nos manda " + line_decod)

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

    def register2json(self):
        fichero_json = json.dumps(self.dicc)
        with open('registered.json', 'w') as fichero_json:
            json.dump(self.dicc, fichero_json, sort_keys=True, indent=4)


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    if PORT < 1024:
        sys.exit("Error: port is invalid")
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
