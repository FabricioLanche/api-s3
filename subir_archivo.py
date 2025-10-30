import base64
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    directorio = event['body'].get('directorio', '')  # Opcional, ej: "imagenes/" o ""
    nombre_archivo = event['body']['nombre_archivo']  # Ej: "foto.jpg"
    contenido_base64 = event['body']['contenido_base64']  # Archivo en base64
    
    # Construir la ruta completa en S3
    # Si hay directorio: "imagenes/foto.jpg", si no: "foto.jpg"
    ruta_s3 = f"{directorio}{nombre_archivo}" if directorio else nombre_archivo
    
    # Proceso
    s3 = boto3.resource('s3')
    try:
        # Decodificar base64 y subir a S3
        s3.Object(nombre_bucket, ruta_s3).put(Body=base64.b64decode(contenido_base64))
        
        # Salida
        return {
            'statusCode': 200,
            'mensaje': f'Archivo {nombre_archivo} subido exitosamente',
            'bucket': nombre_bucket,
            'ruta_s3': ruta_s3,
            'location': f's3://{nombre_bucket}/{ruta_s3}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'mensaje': f'Error al subir el archivo: {str(e)}',
            'bucket': nombre_bucket
        }
