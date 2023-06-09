##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: notifier.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 3.0.0 Marzo 2022
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y lo notificará a un(a) enfermero(a) én particular para la atención del adulto mayor en
#   cuestión
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
#           |                        |    clase                 |    un mensaje, manda  |
#           |                        |  - message: es el        |    un mensaje por     |
#           |                        |    mensaje que se        |    Telegram al        |
#           |                        |    recibió               |    enfermero          |
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
import json, time, sys, stomp
import telepot

class Notifier(stomp.ConnectionListener):

    def __init__(self):
        self.topic = "notifier"
        self.token = ""
        self.chat_id = ""
        self.msg_recieved = 0
    
    def on_error(self, message):
        print("Error recibido")
        print(message)

    def on_message(self, message):
        print("enviando notificación de signos vitales...")
        if self.token and self.chat_id:
            data = json.loads(message.body)
            message = f"ADVERTENCIA!!!\n[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}...\nssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}"
            bot = telepot.Bot(self.token)
            bot.sendMessage(self.chat_id, message)
        time.sleep(1)

    def suscribe(self):
        print("Inicio de gestión de notificaciones...")
        print()
        consume(queue=self.topic, callback=self.callback)

def consume(queue):
    try:
        conn = stomp.Connection([("localhost", 61613)])
        listener = Notifier()
        conn.set_listener("notifier", listener)
        conn.connect("", "", wait=True)
    except (KeyboardInterrupt, SystemExit):
        conn.disconnect()
        sys.exit("Conexión finalizada...")

    while True:
        conn.subscribe(queue, header={}, id="notifier", ack="cliente")
        time.sleep(5)

if __name__ == '__main__':
    notifier = Notifier()
    notifier.suscribe()