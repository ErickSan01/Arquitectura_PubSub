##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: monitor.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los mostrará al área interesada para su monitoreo continuo
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
#           |       suscribe()       |  - self: definición de   |  - inicializa el      |
#           |                        |    la instancia de la    |    proceso de         |
#           |                        |    clase                 |    monitoreo de       |
#           |                        |                          |    signos vitales     |
#           +------------------------+--------------------------+-----------------------+
#           |        consume()       |  - self: definición de   |  - realiza la         |
#           |                        |    la instancia de la    |    suscripción en el  |
#           |                        |    clase                 |    distribuidor de    |
#           |                        |  - queue: ruta a la que  |    mensajes para      |
#           |                        |    el suscriptor está    |    comenzar a recibir |
#           |                        |    interesado en recibir |    mensajes           |
#           |                        |    mensajes              |                       |
#           |                        |  - callback: accion a    |                       |
#           |                        |    ejecutar al recibir   |                       |
#           |                        |    el mensaje desde el   |                       |
#           |                        |    distribuidor de       |                       |
#           |                        |    mensajes              |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       callback()       |  - self: definición de   |  - muetra en pantalla |
#           |                        |    la instancia de la    |    los datos del      |
#           |                        |    clase                 |    adulto mayor       |
#           |                        |  - ch: canal de          |    recibidos desde el |
#           |                        |    comunicación entre el |    distribuidor de    |
#           |                        |    suscriptor y el       |    mensajes           |
#           |                        |    distribuidor de       |                       |
#           |                        |    mensajes [propio de   |                       |
#           |                        |    RabbitMQ]             |                       |
#           |                        |  - method: método de     |                       |
#           |                        |    conexión utilizado en |                       |
#           |                        |    la suscripción        |                       |
#           |                        |    [propio de RabbitMQ]  |                       |
#           |                        |  - properties:           |                       |
#           |                        |    propiedades de la     |                       |
#           |                        |    conexión [propio de   |                       |
#           |                        |    RabbitMQ]             |                       |
#           |                        |  - body: contenido del   |                       |
#           |                        |    mensaje recibido      |                       |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import json, time, sys, stomp

class Monitor(stomp.ConnectionListener):

    def __init__(self):
        self.topic = "monitor"
        self.msg_recieved = 0

    def on_error(self, message):
        print("Error recibido")
        print(message)

    def on_message(self, message):
        data = json.loads(message.body)
        print("ADVERTENCIA!!!")
        print(f"[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}... con wearable {data['wearable']['id']}")
        print(f"ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        print()
        time.sleep(1)

    def suscribe(self):
        print("Inicio de monitoreo de signos vitales...")
        print()
        consume(queue=self.topic)

def consume(queue):
    try:
        conn = stomp.Connection([("localhost", 61613)])
        listener = Monitor()
        conn.set_listener("monitor", listener)
        conn.connect("", "", wait=True)
    except (KeyboardInterrupt, SystemExit):
        conn.disconnect()
        sys.exit("Conexión finalizada...")

    while True:
        conn.subscribe(queue, header={}, id="monitor", ack="cliente")
        time.sleep(5)

if __name__ == '__main__':
    monitor = Monitor()
    monitor.suscribe()