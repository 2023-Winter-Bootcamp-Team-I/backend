# tasks.py

from __future__ import absolute_import, unicode_literals

import os

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
            model="dall-e-3",
            prompt=f"{enContent}"
                   f" Please draw the sentence in a cute art 2d style.",
            n=1,
            size="1024x1024"
        )
        imageUrl = response['data'][0]['url']
        image_data = requests.get(imageUrl).content
        return upload_to_s3(image_uuid, image_data, 'image')
    except Exception as e:
        print(f"Error generating DALL-E image: {e}")
        return None

@shared_task
def gtts_async(tts_uuid,content,lan):
    print("진입")
    tts = gTTS(text=content, lang=lan)
    temp_file_path = f"{tts_uuid}.mp3"
    tts.save(temp_file_path)

    with open(temp_file_path, 'rb') as file_data:
        url = upload_to_s3(tts_uuid, file_data, 'tts')

    os.remove(temp_file_path)
    return url

def upload_to_s3(file_uuid, file, type):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=get_secret("Access_key_ID"),
            aws_secret_access_key=get_secret("Secret_access_key")
        )
        print('진입 2')
        if type == 'image':
            file_key = file_uuid + ".jpg"
            s3_client.put_object(Body=file, Bucket=get_secret("AWS_BUCKET_NAME"), Key=file_key, ContentType='image/jpeg')
            url = get_secret("FILE_URL") + "/" + file_key
            url = url.replace(" ", "_")
            return url
        elif type == 'tts':
            print('진입3')
            file_key = file_uuid + ".mp3"
            s3_client.put_object(Body=file, Bucket=get_secret("AWS_BUCKET_NAME"), Key=file_key, ContentType='audio/mpeg')
            url = get_secret("FILE_URL") + "/" + file_key
            url = url.replace(" ", "_")
            return url

    except NoCredentialsError:
        print("AWS credentials not available.")
        return None