# tasks.py

from __future__ import absolute_import, unicode_literals

import os
import urllib.request

# from gtts import gTTS
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
                   f"Please draw the sentence in a cute art 2d style."
                   f"Please draw only in pictures",
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
def gtts_async(tts_uuid, content, lan):
    print("진입")

    # 네이버 API 사용을 위한 설정 (클라이언트 ID와 시크릿)
    client_id = get_secret("Naver_client_ID")  # 네이버 클라우드 플랫폼에서 발급받은 클라이언트 ID
    client_secret = get_secret("Naver_client_SECRET") # 네이버 클라우드 플랫폼에서 발급받은 클라이언트 시크릿

    # 변환할 텍스트 인코딩
    encText = urllib.parse.quote(content)

    # 네이버 음성합성 API 요청 데이터 설정
    data = "speaker=nshasha&volume=0&speed=0&pitch=0&format=mp3&text=" + encText

    # 네이버 음성합성 API URL
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

    # HTTP 요청 생성 및 헤더 설정
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    # HTTP 요청 전송 및 응답 받기
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    # 응답 처리
    if rescode == 200:
        temp_file_path = f"{tts_uuid}.mp3"

        with open(temp_file_path, 'wb') as file_data:
            file_data.write(response.read())

        with open(temp_file_path, 'rb') as file_data:
            url = upload_to_s3(tts_uuid, file_data, 'tts')

        os.remove(temp_file_path)
        return url
    else:
        print("Error Code:" + rescode)
        return None

    # print("진입")
    # tts = gTTS(text=content, lang=lan)
    # temp_file_path = f"{tts_uuid}.mp3"
    # tts.save(temp_file_path)
    #
    # with open(temp_file_path, 'rb') as file_data:
    #     url = upload_to_s3(tts_uuid, file_data, 'tts')
    #
    # os.remove(temp_file_path)
    # return url

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