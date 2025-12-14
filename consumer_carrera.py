from confluent_kafka import Consumer
import boto3
import uuid

# --- 1. CONFIGURACIÓN MINIO (S3) ---
BUCKET_NAME = 'strava-data'

s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)

# --- 2. CONFIGURACIÓN KAFKA ---
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'consumidor-carrera',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
topic_kafka = 'datos_strava'
consumer.subscribe([topic_kafka])

print(f"ESPERANDO DATOS DE CARRERA en '{topic_kafka}'...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        mensaje = msg.value().decode('utf-8')

        # --- 3. LÓGICA DE FILTRADO Y GUARDADO ---
        if 'Carrera' in mensaje:
            
            # Nombre del archivo: Carrera/dato_unico.json
            nombre_archivo = f"Carrera/dato_{uuid.uuid4()}.json"

            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=nombre_archivo,
                Body=mensaje,
                ContentType='application/json'
            )

            print(f"✅ Guardado en MinIO: {nombre_archivo}")

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    consumer.close()