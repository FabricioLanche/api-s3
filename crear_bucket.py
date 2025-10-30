import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    
    # Proceso
    s3 = boto3.client('s3', region_name='us-east-1')
    try:
        # Crear bucket en us-east-1 (no requiere LocationConstraint)
        response = s3.create_bucket(Bucket=nombre_bucket)
        
        # Salida
        return {
            'statusCode': 200,
            'mensaje': f'Bucket {nombre_bucket} creado exitosamente',
            'bucket': nombre_bucket
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'mensaje': f'Error al crear el bucket: {str(e)}',
            'bucket': nombre_bucket
        }
