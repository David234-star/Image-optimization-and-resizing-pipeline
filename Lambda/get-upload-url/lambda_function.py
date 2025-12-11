import boto3
import json
from botocore.config import Config

# 1. FORCE THE REGION HERE
my_config = Config(
    region_name='us-east-2',
    signature_version='s3v4',
    s3={
        'addressing_style': 'virtual'
    }
)

# 2. Apply the config
s3 = boto3.client('s3', config=my_config)

BUCKET_NAME = 'my-image-pipeline-source-1'


def lambda_handler(event, context):
    file_name = event.get('queryStringParameters', {}
                          ).get('filename', 'image.jpg')

    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET_NAME, 'Key': file_name,
                'ContentType': 'image/jpg'},
        ExpiresIn=300
    )

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,GET"
        },
        'body': json.dumps({'uploadURL': presigned_url, 'filename': file_name})
    }
