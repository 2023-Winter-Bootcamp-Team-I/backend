import json

from channels.generic.websocket import WebsocketConsumer

import page

class WritePage(WebsocketConsumer):
    def connect(self):
        self.accept()
        #책-페이지 저장 리스트 아래 작성

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

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))