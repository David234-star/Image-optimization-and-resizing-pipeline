import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import io

s3_client = boto3.client('s3')


def resize_image(image_path, resized_path, width):
    with Image.open(image_path) as image:
        aspect_ratio = image.height / image.width
        height = int(width * aspect_ratio)
        image.thumbnail((width, height))
        image.save(resized_path, optimize=True, quality=85)


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # Define destination bucket (hardcoded or env var)
        dest_bucket = bucket.replace('source', 'dest')

        download_path = '/tmp/{}'.format(key)

        # Download
        print(f"Downloading {key} from {bucket}")
        s3_client.download_file(bucket, key, download_path)

        # Processing Resolutions
        widths = {
            '1080p': 1920,
            '720p': 1280,
            'mobile': 480
        }

        filename_base = os.path.splitext(key)[0]

        for label, width in widths.items():
            upload_path = f"/tmp/processed_{label}_{key}"

            # Convert to WebP and Resize
            with Image.open(download_path) as image:
                aspect_ratio = image.height / image.width
                height = int(width * aspect_ratio)

                # Resize
                image.thumbnail((width, height))

                # Save as WebP
                new_key = f"{label}/{filename_base}.webp"
                buffer = io.BytesIO()
                image.save(buffer, format="WEBP", quality=80, optimize=True)
                buffer.seek(0)

                # Upload
                print(f"Uploading {new_key} to {dest_bucket}")
                s3_client.put_object(
                    Bucket=dest_bucket,
                    Key=new_key,
                    Body=buffer,
                    ContentType='image/webp'
                )

    return "Processing Complete"
