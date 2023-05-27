##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: record.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los almacena en un archivo de texto que simula el expediente de los pacientes
#
#   Este archivo también define el punto de ejecución del Suscriptor
#
#   A continuación se describen los métodos que se implementaron en esta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |       __init__()       |  - self: definición de   |  - constructor de la  |
#           |                        |    la instancia de la    |    clase              |
#           |                        |    clase                 |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       on_error()       |  - self: definición de   |  - reporta un error   |
#           |                        |    la instancia de la    |    en un mensaje      |
#           |                        |    clase                 |                       |
#           |                        |  - message: es el        |                       |
#           |                        |    mensaje que causó el  |                       |
#           |                        |    error                 |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       on_message()     |  - self: definición de   |  - se manda llamar    |
#           |                        |    la instancia de la    |    cuando se recibe   |
#           |                        |    clase                 |    un mensaje, guarda |
#           |                        |  - message: es el        |    los datos del      |
#           |                        |    mensaje que se        |    paciente en un     |
#           |                        |    recibió               |    archivo de texto   |
#           +------------------------+--------------------------+-----------------------+
#           |       suscribe()       |  - self: definición de   |  - inicializa el      |
#           |                        |    la instancia de la    |    proceso de         |
#           |                        |    clase                 |    monitoreo de       |
#           |                        |                          |    signos vitales     |
#           +------------------------+--------------------------+-----------------------+
#           |        consume()       |  - queue: ruta a la que  |  - realiza la         |
#           |                        |    el suscriptor está    |    suscripción en el  |
#           |                        |    interesado en recibir |    distribuidor de    |
#           |                        |    mensajes              |    mensajes para      |
#           |                        |                          |    comenzar a recibir |
#           |                        |                          |    mensajes           |
#           |                        |                          |                       |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import json, time, sys, os, stomp

class Record(stomp.ConnectionListener):

    def __init__(self):
        try:
            os.mkdir('records')
        except OSError as _:
            pass
        self.topic = "record"
        self.msg_recieved = 0
    
    def on_error(self, message):
        print("Error recibido")
        print(message)

    def on_message(self, message):
        print("datos recibidos, actualizando expediente del paciente...")
        data = json.loads(message.body)
        record_file = open (f"./records/{data['ssn']}.txt",'a')
        record_file.write(f"\n[{data['wearable']['date']}]: {data['name']} {data['last_name']}... ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        record_file.close()
        time.sleep(1)

    def suscribe(self):
        print("Esperando datos del paciente para actualizar expediente...")
        print()
        consume(queue=self.topic, callback=self.callback)

def consume(queue):
    try:
        conn = stomp.Connection([("localhost", 61613)])
        listener = Record()
        conn.set_listener("notifier", listener)
        conn.connect("", "", wait=True)
    except (KeyboardInterrupt, SystemExit):
        conn.disconnect()
        sys.exit("Conexión finalizada...")

    while True:
        conn.subscribe(queue, header={}, id="notifier", ack="cliente")
        time.sleep(5)

if __name__ == '__main__':
    record = Record()
    record.suscribe()