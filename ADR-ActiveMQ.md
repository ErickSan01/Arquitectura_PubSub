# Cambio de RabbitMQ a ActiveMQ

## Status

Aceptado

## Context

VMWare ha decidido que, a partir de julio del 2023, el broker de mensajes RabbitMQ empezará a ser de licencia de paga, mediante renta mensual.
Esto ha causado que se tenga que cambiar de tecnología, ya que a Setén no le conviene este cambio de parte de RRabbitMQ.

## Decision

Se decidió usar ActiveMQ como alternativa ya que funciona de manera similar y esta seguirá siendo de licencia gratuita.


## Consequences

What becomes easier or more difficult to do because of this change?
Debido a este cambio, se tendrá que modificar la forma en la que los publicadores se conectan a dicho servicio, ya que ahora usarán el protocolo STOMP, esto causará que se cambie la forma en que se mandan los mensajes.  
De igual forma, los suscriptores tendrán que cambiar, ya que utilizarán de igual forma el protocolo STOMP en lugar del protocolo AMQP. Esto hará que se cambie la forma en la que se consuman los mensajes.