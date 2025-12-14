from confluent_kafka import Consumer

config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'consumidor-natacion',        
    'auto.offset.reset': 'earliest'         
}

consumer = Consumer(config)

topic_kafka = 'datos_strava'
consumer.subscribe([topic_kafka])

print(f"Esperando mensajes del tópico '{topic_kafka}'...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            # No hay mensaje disponible en este momento, seguimos esperando
            continue

        if msg.error():
            # Si hay un error en el mensaje, lo mostramos
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # Si el mensaje es válido, mostramos su contenido
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    consumer.close()