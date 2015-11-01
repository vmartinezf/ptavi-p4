#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time
import os.path


def regist(line_decod, dicc_usuarios, dicc, client_infor):
    direction = line_decod.split()[1]
    expiration = int(line_decod.split()[2])
    expires = int(time.time()) + expiration
    time_expiration = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.gmtime(expires))
    dicc_usuarios["address"] = client_infor[0]
    dicc_usuarios["expires"] = time_expiration
    if (expiration == 0):
        if ((len(dicc) != 0) and (direction in dicc)):
            del dicc[direction]
    elif ('@' in direction):
        dicc[direction] = dicc_usuarios
    print (dicc)
    for usuario in dicc:
        time_now = time.strftime('%Y­%m­%d %H:%M:%S',
                                 time.gmtime(time.time()))
        direct = dicc[usuario]
        value = direct["expires"]
        if ((str(time_now) > value)and (direction in dicc)):
            del dicc[direction]
            break


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    dicc = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.json2registered()
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
                    regist(line_decod, dicc_usuarios, self.dicc, client_infor)
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

    def json2registered(self):
        fichero_json = 'registered.json'
        if (os.path.exists(fichero_json)):
            self.dicc = json.loads(open(fichero_json).read())
        else:
            self.dicc = {}

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    if PORT < 1024:
        sys.exit("Error: port is invalid")
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
