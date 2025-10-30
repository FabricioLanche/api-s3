import base64
import boto3
import json

def lambda_handler(event, context):
    try:
        # Parsear el body si viene como string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Entrada
        nombre_bucket = body.get('bucket')
        nombre_archivo = body.get('archivo')  # Ruta completa: directorio/archivo.ext
        
        # El contenido puede venir como:
        # 1. Base64 en el campo 'contenido' (API Gateway REST con binary media types)
        # 2. Ya decodificado en 'contenido' si API Gateway lo procesó
        contenido = body.get('contenido', '')
        
        # Si el contenido está en base64, decodificarlo
        if event.get('isBase64Encoded', False):
            contenido_bytes = base64.b64decode(contenido)
        else:
            # Intentar decodificar si viene como string base64
            try:
                contenido_bytes = base64.b64decode(contenido)
            except:
                # Si falla, asumir que ya está en bytes o string
                contenido_bytes = contenido.encode() if isinstance(contenido, str) else contenido
        
        if not nombre_bucket or not nombre_archivo:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'mensaje': 'Faltan parámetros requeridos: bucket y archivo'
                })
            }
        
        # Proceso
        s3 = boto3.resource('s3')
        
        # Subir archivo
        s3.Object(nombre_bucket, nombre_archivo).put(Body=contenido_bytes)
        
        # Salida
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': f'Archivo {nombre_archivo} subido exitosamente al bucket {nombre_bucket}',
                'bucket': nombre_bucket,
                'archivo': nombre_archivo,
                'location': f's3://{nombre_bucket}/{nombre_archivo}'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'mensaje': f'Error al subir el archivo: {str(e)}'
            })
        }
