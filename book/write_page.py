import json
from channels.generic.websocket import WebsocketConsumer
import page

class WritePage(WebsocketConsumer):

    #소켓 통신 연결
    def connect(self):
        self.accept()
        #책-페이지 저장 리스트 아래 작성
        self.book_content = [] #전체 컨텐츠 저장
        self.book_image = [] #이미지 저장
        self.book_content_ko = []
        self.book_content_en = []

    # 소켓 통신 연결 해제
    def disconnect(self, closed_code):
        # 만약에 중간에 끊킨 경우, book_id와 관련된 것 전부 삭제
        book_object = page.objects.get(id=self.book_id)
        pages = page.objects.filter(book_id=book_object)
        page_num = pages.count()

        # 가져온 페이지의 수와 예상 페이지 수가 다르면 삭제
        if page_num != self.page_num:
            page.objects.filter(book_id=self.book_id).delete()

        for pages in pages:
            try:
                # 해당 페이지의 한국어 내용과 영어 내용을 가져와 출력
                ko_content = pages.ko_content
                en_content = pages.en_content
                print(ko_content, en_content)
            except:
                page.objects.filter(book_id=self.book_id).delete()
        pass

    # 소켓 통신 (메세지)
    def receive(self, text_data):
        text_data_json = json.loads(text_data) #data를 받음
        # if 초기 생성 -> 초기 값을 서버가 받음

            # data json 형태니까 나눌 수 있겠지

            # 나이 성별 이름 동화 등을 가지고 gpt 함수를 부를거야

            # 답변이 생성되면 프론트로 디비 저장 않고, 다시 보내줘 -> 두개 다 반환


        # else 책 만들고 있는 경우 -> 산택한 스토리를 서버가 받음

            # data json 형태니까 나눌 수 있겠지

            # 1. 받은 스토리를 db에 저장 -> 페이지 숫자랑 내용이랑 등등 + 이미지 UUID

            # 2. 받은 스토리 셀러리로 넘겨서 달리로 그림 생성 하기 + 위 이미지 UUiD

            # 3. 이전에 받은 값 받아서 이야기 2개 생성 -> 마지막 페이지 생성 이후에 재 진입시 3번은 하지 않음 -> 페이지 수 카운트 ㄱㄱ

            # 3-1. 답변 생성되면 프론트로 다시 보내기 -> 두개다 반환 (영어버전 한글 버전 다)

