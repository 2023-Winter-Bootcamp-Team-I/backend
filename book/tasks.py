# tasks.py

from __future__ import absolute_import, unicode_literals
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
            prompt=[{
                    "role": "system",
                    "content": "당신은 유능한 동화 그림 작가입니다. 말 없이 요청하는 사항에 대해서 그림만 그려주세요."
                },{
                    "role": "user",
                    "content": f"{enContent}라는 내용의 그림 하나 만들어주세요."
                }],
            n=1,
            size="1024x1024"
        )
        # 여기 에러 위험 있어요..
        imageUrl = response['data'][0]['url']
        #print(imageUrl)
        image_data = requests.get(imageUrl).content
        return upload_to_s3(image_uuid, image_data)
    except Exception as e:
        print(f"Error generating DALL-E image: {e}")
        return None

def upload_to_s3(image_uuid, file):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=get_secret("Access_key_ID"),
            aws_secret_access_key=get_secret("Secret_access_key")
        )
        file_key = image_uuid + ".jpg"
        s3_client.put_object(Body=file, Bucket=get_secret("AWS_BUCKET_NAME"), Key=file_key)
        url = get_secret("FILE_URL") + "/" + file_key
        url = url.replace(" ", "_")
        return url
    except NoCredentialsError:
        print("AWS credentials not available.")
        return None