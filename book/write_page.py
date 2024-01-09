from channels.generic.websocket import WebsocketConsumer

import page


class WritePage(WebsocketConsumer):
    def connect(self):
        self.accept()
        #대화 기록 저장 리스트 라는데용

    def disconnect(self, closed_code):
        # 만약에 중간에 끊킨 경우, book_id와 관련된 것 전부 삭제
        book_object = page.objects.get(id=self.book_id)
        pages = page.objects.filter(book_id=book_object)
        question_numbers = pages.count()

        # if question_numbers != self.question_number:
        #     Question.objects.filter(form_id=self.form_id).delete()
        #
        # for question in questions:
        #     try:
        #         answer = question.answer
        #         print(answer)
        #     except:
        #         Question.objects.filter(form_id=self.form_id).delete()
        # pass