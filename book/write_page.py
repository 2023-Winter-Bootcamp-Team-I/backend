import json
import boto3
import openai
import requests
from botocore.exceptions import NoCredentialsError
from channels.generic.websocket import WebsocketConsumer
from django.db import IntegrityError
from pip._internal.operations.prepare import get_file_url
from .tasks import generate_dalle_image_async  # tasks.py 에서 정의한 함수 임포트
from .tasks import gtts_async

from book.models import Book
from page.models import Page
from user.models import User
from backend.settings import get_secret
import uuid


class WritePage(WebsocketConsumer):
    # ----------------------------------------------------------------------- 소켓 통신 연결
    def connect(self):
        print("connecting")  # 지금 이건 왜 안찍히져
        self.accept()
        # 책-페이지 저장 리스트 아래 작성
        self.book_content = []  # 전체 컨텐츠 저장
        self.book_image = []  # 이미지 저장
        self.book_content_ko = []
        self.book_content_en = []
        self.conversation = []

    # ---------------------------------------------------------------------- 소켓 통신 연결 해제
    def disconnect(self, closed_code):
        # 페이지 개수 비교해서 하는거보다는 제목이 지어져 있느냐 안 지어져있느냐로 삭제 하는게 좋을 것 같아서 이렇게 했습니다!
        # 'book_id' 속성이 있는지 확인
        if hasattr(self, 'book_id'):
            try:
                # 'book_id'로 책 조회
                book = Book.objects.get(book_id=self.book_id)
                print(book)
                # 'title' 필드가 비어 있는지 확인
                if not book.title:
                    # 'title' 필드가 비어 있으면 책 삭제
                    book.delete()
                    print(f"Deleted book with empty title and id {self.book_id}")
                else:
                    print(f"Book with id {self.book_id} has a title and will not be deleted")

            except Book.DoesNotExist:
                # 책이 존재하지 않는 경우
                print(f"Book with id {self.book_id} does not exist or already deleted")
        else:
            # 'book_id' 속성이 없는 경우
            print("No book to delete")

    # --------------------------------------------------------------------- 소켓 통신 (메세지)
    def receive(self, text_data):
        text_data_json = json.loads(text_data)  # data를 받음
        page_num = text_data_json.get('pageCnt')
        if text_data_json['type'] == 'start':
            user_info = self.extract_user_info(text_data_json)
            print('start 진입')
            try:
                user_id = text_data_json['userId']
                username = text_data_json['userName']
                fairytale = text_data_json['fairyTale']
                gender = text_data_json['gender']
                age = int(text_data_json['age'])
                print('try 진입')
                # 수정된 부분: user_id를 사용하여 User 모델의 인스턴스를 가져와서 할당
                user_instance = User.objects.get(user_id=user_id)
                book = self.save_book_to_db(user_instance, username, fairytale, gender, age)

                self.book_id = book.book_id
                # print(self.book_id)

            except KeyError as e:
                # text_data_json에서 필요한 키가 누락된 경우
                print(f"Missing key in text_data_json: {e}")

            except IntegrityError as e:
                print(f"Database Integrity Error: {e}")

            self.generate_start_gpt_responses(user_info)  # 시작때 초기 정보 받은거로 프롬프팅
            # 페이지 번호 증가 및 응답 반환
            page_num += 1
            self.send_response_to_client(page_num)

        elif text_data_json['type'] == 'ing':
            # 책 내용 가져온거 처리하기
            choice = text_data_json.get('choice')
            print("ing")
            ko_content = text_data_json.get('koContent')
            en_content = text_data_json.get('enContent')

            self.book_content.append(ko_content)  # 선택한 내용 저장

            # 이미지 저장
            image_uuid = str(uuid.uuid4())
            self.save_page_story_to_db(image_uuid, page_num, ko_content['content'],
                                       en_content['content'])  # db에 uuid 넣은 이미지 저장
            image = generate_dalle_image_async.delay(image_uuid, en_content['content'])  # 비동기로 해주었음 tasks.py ㄱ

            # 한국어 음성파일 비동기
            ko_tts_uuid = str(uuid.uuid4())
            ko_tts = gtts_async.delay(ko_tts_uuid, ko_content['content'], 'ko')
            # 영어 음성파일 비동기
            en_tts_uuid = str(uuid.uuid4())
            en_tts = gtts_async.delay(en_tts_uuid, en_content['content'], 'en')
            # 음성 파일 저장
            self.save_page_tts_to_db(ko_tts_uuid, en_tts_uuid, page_num)

            # 6번째 페이지 처리
            if page_num == 6:
                self.generate_last_ing_gpt_responses(choice)  # 끝
                page_num += 1
                self.send_response_to_client(page_num)
            else:  # 2~5번 페이지 처리
                self.generate_ing_gpt_responses(choice)  # 중간
                page_num += 1
                self.send_response_to_client(page_num)


        elif text_data_json['type'] == 'end':  # 마지막 선택 처리

            ko_content = text_data_json.get('koContent')
            en_content = text_data_json.get('enContent')
            image_uuid = str(uuid.uuid4())

            self.save_page_story_to_db(image_uuid, page_num, ko_content['content'], en_content['content'])

            # 비동기로 해주었음 tasks.py ㄱ
            image = generate_dalle_image_async.delay(image_uuid, en_content['content'])  # 리턴 값이 url임 -> 나중에 비동기

            # 한국어 음성파일 비동기
            ko_tts_uuid = str(uuid.uuid4())
            ko_tts = gtts_async.delay(ko_tts_uuid, ko_content['content'], 'ko')
            # 영어 음성파일 비동기
            en_tts_uuid = str(uuid.uuid4())
            en_tts = gtts_async.delay(en_tts_uuid, en_content['content'], 'en')
            # 음성 파일 저장
            self.save_page_tts_to_db(ko_tts_uuid, en_tts_uuid, page_num)

            self.send(text_data=json.dumps({"bookId": self.book_id}))

            # print(image)

    ######################## 함수들 ########################
    # --------------------------------------------------------------------- 이야기 만들 때 필요한 함수들
    # 자 이거 api 명세서에 유림님이 적어주신 카멜케이스 변수명 대로 수정 부탁드려요 (저는 하다가 말았어요~)
    def extract_user_info(self, data):
        user_info = {
            'userId': data.get('userId'),
            'userName': data.get('userName'),
            'gender': data.get('gender'),
            'age': data.get('age'),
            'language': data.get('language'),
            'fairyTale': data.get('fairyTale')
        }
        return user_info

    def generate_start_gpt_responses(self, user_info):
        # "role": "system",
        # "content": f"당신은 동화 작가 역할을 해주었으면 합니다."
        # f"<초기 정보>"
        # f"주인공 이름: {user_info['userName']}"
        # f"주인공 성별: {user_info['gender']}"
        # f"대상 연령: {user_info['age']}"
        # f"원작 동화: {user_info['fairyTale']}"
        # f"<초기 정보 끝>"
        # f"<초기 정보>를 기반으로, 저에게 두 가지의 서로 다른 이야기의 초반부를 한 문장씩 제시해주세요."
        # f"두 가지의 이야기 중 제가 하나의 이야기를 선택하기 전 까지 기다려주세요."
        # f"제가 선택을 한 후 제가 선택한 이야기에 이어서 저에게 두 가지의 서로 다른 이야기를 한 문장씩 제시해주세요."
        # f"문장마다 영어로도 번역 해주세요."
        # f"서로 다른 이야기지만, <초기 정보>를 기반으로 해야하는 것은 같습니다."
        # f"두 문장 이내로 대답해주세요."

        self.conversation = [
            {
                "role": "system",
                "content": f"You are asked to take on the role of a fairy tale writer."
                           f"<Initial Information> "
                           f"Main character's name:{user_info['userName']}, Main character's gender:{user_info['gender']}, Target age group:{user_info['age']}, Original fairy tale:{user_info['fairyTale']} "
                           f"<End of Initial Information>"
                           f"Based on the <Initial Information>, please present me with the beginnings of two different stories, each in one sentence. Wait for me to choose one of the stories before continuing. Once I have made my choice, continue with the story I selected by presenting me with two different story progressions, each in one sentence. Please also translate each sentence into English. Although the stories should be different, they must be based on the <Initial Information>. Please answer within two sentences.When the sentence is in Korean, please use formal language. 예시) '~했어요.'"
                           f"Please replace the existing protagonist with {user_info['userName']} of the <Initial Information>."
                           f"Please follow the format where the sentence comes right after '@' or '#' as below."
                           f"@korean"
                           f"@english"
                           f"#korean"
                           f"#english"
            }
        ]



    def generate_ing_gpt_responses(self, choice):
        # # 지피티씨 호출해서 만들고 반환하기. -> 내가 선택한 이야기로 진행해주고 계속 이어서 두가지로 해줘
        # "role": "system",
        # "content": f"당신은 동화 작가 역할을 해주었으면 합니다."
        # f"<이전 이야기 정보>"
        # f"{self.book_content}"
        # f"<이전 이야기 끝>"
        # f"<이전 이야기>에 이어지는 내용의 두 가지의 서로 다른 이야기를 한 문장씩 제시해주세요."
        # f"두 가지의 이야기 중 제가 하나의 이야기를 선택하기 전 까지 기다려주세요."
        # f"제가 선택을 한 후 제가 선택한 이야기에 이어서 저에게 두 가지의 서로 다른 이야기를 한 문장씩 제시해주세요."
        # f"문장마다 영어로도 번역 해주세요."
        # f"서로 다른 이야기지만, <이전 이야기 정보>를 기반으로 해야하는 것은 같습니다."
        self.conversation = [
            {
                "role": "system",
                "content": f"You are requested to take on the role of a fairy tale writer."
                           f"<Previous Story Information>"
                           f"{self.book_content}"
                           f"<End of Previous Story>"
                           f"Based on the <Previous Story>, please present me with the beginnings of two different stories, each in one sentence. Wait for me to choose one of the stories before continuing. After I make my choice, continue with the story I selected by presenting me with two different continuations, each in one sentence. Please also translate each sentence into English. Although the stories should be different, they must be based on the <Previous Story Information>.When the sentence is in Korean, please use formal language. 예시) '~했어요.'"
                           f"Please follow the format where the sentence comes right after '@' as below."
                           f"@korean"
                           f"@english"
                           f"#korean"
                           f"#english"
            },
        ]

    def generate_last_ing_gpt_responses(self, choice):
        # # 지피티씨 호출해서 만들고 반환하기. -> 내가 선택한 이야기로 이야기 마무리 엔딩 내줘
        # "role": "system",
        # "content": f"<이전 이야기 정보>"
        # f"{self.book_content}"
        # f"<이전 이야기 끝>"
        # f"<이전 이야기>에 이어지는 하나의 내용으로 동화 이야기를 결말까지 써주세요."
        self.conversation = [
            {
                "role": "system",
                "content": f"<Previous Story Information>"
                           f"{self.book_content}"
                           f"<End of Previous Story>"
                           f"Please write a fairy tale story to its conclusion, continuing from the <Previous Story> as a single narrative.When the sentence is in Korean, please use formal language. 예시) '~했어요.'"
                           f"Please follow the format where the sentence comes right after '@' as below."
                           f"@korean"
                           f"@english"
            },
        ]

    # -------------------------------------------------------------------- db 넣는 함수들
    # db에 page 저장

    def save_page_story_to_db(self, image_uuid, page_num, ko_content, en_content):
        try:
            book = Book.objects.get(book_id=self.book_id)
            imageUrl = get_secret("FILE_URL") + "/" + image_uuid + ".jpg"
            Page.objects.create(book_id_id=book.book_id, image_url=imageUrl, page_num=page_num, ko_content=ko_content,
                                en_content=en_content)
        except Book.DoesNotExist:
            print(f"Book with id {self.book_id} does not exist.")

    def save_page_tts_to_db(self, ko_uuid, en_uuid, page_num):
        try:
            book = Book.objects.get(book_id=self.book_id)
            page = Page.objects.get(book_id=book.book_id, page_num=page_num)
            page.ko_tts_url = get_secret("FILE_URL") + "/" + ko_uuid + ".mp3"
            page.en_tts_url = get_secret("FILE_URL") + "/" + en_uuid + ".mp3"

            page.save()

        except Book.DoesNotExist:
            print(f"Book with id {self.book_id} does not exist.")
        except Page.DoesNotExist:
            print(f"Page for book with id {self.book_id} does not exist.")

    def save_book_to_db(self, user_id, username, fairytale, gender, age):
        return Book.objects.create(user_id=user_id, fairytale=fairytale, username=username, gender=gender, age=age)

    def send_response_to_client(self, pageCnt):
        openai.api_key = get_secret("GPT_KEY")
        # GPT-3 스트리밍 API 호출
        for response in openai.ChatCompletion.create(
                model="gpt-4",
                # model="gpt-4",
                messages=self.conversation,
                temperature=0.5,
                stream=True
        ):
            # print(response)
            # 각 응답 조각 처리
            if 'delta' in response.choices[0] and 'content' in response.choices[0].delta:
                message = response.choices[0].delta["content"]
                # 클라이언트에게 실시간으로 메세지 전송
                self.send(text_data=json.dumps({"message": message}))
            else:
                # 'delta' 또는 'content' 키가 없는 경우에 대한 처리 추가
                print("Invalid response format: {}".format(response))

        # if 초기 생성 -> 초기 값을 서버가 받음 (n번 페이지) = 0 <start>
        # data json 형태니까 나눌 수 있겠지
        # 나이 성별 이름 동화 등을 가지고 gpt 함수를 부를거야
        # 답변이 생성되면 프론트로 디비 저장 않고, 다시 보내줘 -> 두개 다 반환 n++ 까지 하고 n 전달
        # elif 책 만들고 있는 경우 -> 선택한 스토리를 서버가 받음 (n번 페이지) <ing>
        # data json 형태니까 나눌 수 있겠지
        # 1. 받은 스토리(n번 페이지)를 db에 저장 -> 페이지 숫자랑 내용이랑 등등 + 이미지 UUID생성
        # 2. 받은 스토리(n번 페이지) 셀러리로 넘겨서 달리로 그림 생성 하기 + 위 이미지 UUiD전달
        # 3. if n+1번 페이지 제작 중 == 6 <- 분기 이유 : 프롬프팅 함수가 달라짐.
        # 3-1. 이전에 받은 값(n) 받아서 이야기 2개 생성
        # 3-2. 답변 생성되면 프론트로 다시 보내기 -> 두개다 반환 (영어버전 한글 버전 다) n++
        # 3. elif 마지막이 아니라면(2-5번 페이지 제작중)
        # 3-1. 이전에 받은 값(n) 받아서 이야기 2개 생성
        # 3-2. 답변 생성되면 프론트로 다시 보내기 -> 두개다 반환 (영어버전 한글 버전 다) n++
        # else 사용자의 마지막 선택 end / n이 7일때
        # 1. 받은 스토리(6번 페이지)를 db에 저장 -> 페이지 숫자랑 내용이랑 등등 + 이미지 UUID
        # 2. 받은 스토리(6번 페이지) 셀러리로 넘겨서 달리로 그림 생성 하기 + 위 이미지 UUiD

        # # 달리 이미지 생성
        # def generate_dalle_image(self, image_uuid, enContent):
        #     openai.api_key = get_secret("GPT_KEY")
        #     response = openai.Image.create(
        #         prompt=f"당신은 유능한 동화 그림 작가입니다. 말 없이 요청하는 사항에 대해서 그림만 그려주세요. {enContent}라는 내용의 그림 하나 만들어주세요.",
        #         n=1,
        #         size="1024x1024"
        #     )
        #     # url 추출
        #     imageUrl = response['data'][0]['url']
        #     # 이미지 다운로드
        #     image_data = requests.get(imageUrl).content
        #     # S3 클라이언트 생성
        #     try:
        #         # S3 버킷에 이미지 업로드
        #         get_file_url(image_uuid, image_data)
        #     except NoCredentialsError:
        #         print("AWS credentials not available.")
        #         return None
        # # 파일 S3 접근 및 업로드
        # def get_file_url(image_uuid, file):
        #     s3_client = boto3.client(
        #         's3',
        #         aws_access_key_id = get_secret("Access_key_ID"),
        #         aws_secret_access_key = get_secret("Secret_access_key"),
        #     )
        #     file_key = image_uuid + ".jpg"
        #     s3_client.put_object(Body=file, Bucket=get_secret("AWS_BUCKET_NAME"), Key=file_key)
        #     # 업로드된 파일의 URL을 구성
        #     url = get_secret("FILE_URL") + "/" + file_key
        #     # URL 문자열에서 공백을 "_"로 대체
        #     url = url.replace(" ", "_")
        #     return url
        # -------------------------------------------------------------------- 응답을 클라이언트한테 전송하는 함수
