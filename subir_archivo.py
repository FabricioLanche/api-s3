import base64
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    nombre_archivo = event['body']['archivo']  # Ruta completa: directorio/archivo.ext
    contenido_base64 = event['body']['contenido']  # Archivo en base64
    
    # Proceso
    s3 = boto3.resource('s3')
    try:
        # Subir archivo decodificando el base64
        s3.Object(nombre_bucket, nombre_archivo).put(Body=base64.b64decode(contenido_base64))
        
        # Salida
        return {
            'statusCode': 200,
            'mensaje': f'Archivo {nombre_archivo} subido exitosamente al bucket {nombre_bucket}',
            'bucket': nombre_bucket,
            'archivo': nombre_archivo,
            'location': f's3://{nombre_bucket}/{nombre_archivo}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'mensaje': f'Error al subir el archivo: {str(e)}',
            'bucket': nombre_bucket,
            'archivo': nombre_archivo
        }
