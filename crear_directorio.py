import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    nombre_directorio = event['body']['directorio']
    
    # Asegurar que el directorio termine con /
    if not nombre_directorio.endswith('/'):
        nombre_directorio += '/'
    
    # Proceso
    s3 = boto3.client('s3')
    try:
        # En S3, los directorios son objetos vacíos que terminan en /
        s3.put_object(Bucket=nombre_bucket, Key=nombre_directorio)
        
        # Salida
        return {
            'statusCode': 200,
            'mensaje': f'Directorio {nombre_directorio} creado exitosamente en el bucket {nombre_bucket}',
            'bucket': nombre_bucket,
            'directorio': nombre_directorio
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'mensaje': f'Error al crear el directorio: {str(e)}',
            'bucket': nombre_bucket,
            'directorio': nombre_directorio
        }
