# tasks.py

from __future__ import absolute_import, unicode_literals
from gtts import gTTS
import uuid
from celery import shared_task
import openai
import requests
from backend.settings import get_secret  # get_secret 함수를 가정함
import boto3
from botocore.exceptions import NoCredentialsError

@shared_task
def generate_dalle_image_async(image_uuid, enContent):
    try:
        openai.api_key = get_secret("GPT_KEY")
        response = openai.Image.create(
            prompt=f"{enContent}in a fairy tale style",
            n=1,
            size="1024x1024"
        )
        imageUrl = response['data'][0]['url']
        image_data = requests.get(imageUrl).content
        return upload_to_s3(image_uuid, image_data,'image')
    except Exception as e:
        print(f"Error generating DALL-E image: {e}")
        return None

@shared_task
def gtts_async(tts_uuid,content,lan):
    tts = gTTS(text=content, lang=lan)
    return upload_to_s3(tts_uuid, tts,'tts')

def upload_to_s3(file_uuid, file, type):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=get_secret("Access_key_ID"),
            aws_secret_access_key=get_secret("Secret_access_key")
        )
        if type == 'image':
            file_key = file_uuid + ".jpg"
            s3_client.put_object(Body=file, Bucket=get_secret("AWS_BUCKET_NAME"), Key=file_key)
            url = get_secret("FILE_URL") + "/" + file_key
            url = url.replace(" ", "_")
            return url
        elif type == 'tts':
            file_key = file_uuid + ".mp3"
            s3_client.put_object(Body=file, Bucket=get_secret("AWS_BUCKET_NAME"), Key=file_key)
            url = get_secret("FILE_URL") + "/" + file_key
            url = url.replace(" ", "_")
            return url
    except NoCredentialsError:
        print("AWS credentials not available.")
        return None