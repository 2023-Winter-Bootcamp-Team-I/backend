import openai

openai.api_key = "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"

# 대화 데이터 정의
conversation = [
    {"role": "system",
     "content": "당신은 동화 작가입니다. 다른 설명 없이 그저 이야기만 써주세요."
                "피노키오 동화의 배경, 등장인물이 나오게 해주세요"
                "처음부터 저에게 간단하고 서로 다른 2가지 내용의 이야기를 제시해주세요."
                "제가 1번과 2번 둘 중 하나의 답변을 고르면 골랐던 이야기의 내용으로 이어지게 해주세요."
                "답변에 따라 이야기가 바뀝니다."
                "제가 선택을 하기 전까지 기다려 주세요."
                "제가 선택을 할 때 마다 그 선택 내용에 맞는 그림을 그려주세요."
                "이 단계를 반복하며, 7번의 전환 후에 해피엔딩으로 마무리 합니다."
                "한국어로 반환 해주셨으면, 그 다음 영어로도 반환해주세요."
     }
]


while True:
    user_content = input("user : ")
    conversation.append({"role": "user", "content" : f"{user_content}"})
    # 대화를 사용하여 GPT-3 모델에 요청
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)

    assistant_content = response['choices'][0]['message']['content'].strip()

    conversation.append({"role": "assistant", "content" : f"{assistant_content}"})

    # 모델의 응답 확인
    print(assistant_content)
