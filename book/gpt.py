import openai

openai.api_key = "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"

# 대화 데이터 정의
conversation = [
    {"role": "user",
     "content": "이야기의 시작부터 2개의 선택지를 제안해 주세요. 답변에 따라 이야기가 흘러갑니다. 제가 선택을 하기 전까지 기다려 주세요."
                " 선택을 하면, 이야기를 계속 이어나가 주세요. 원작내용을 따라가지 않고 결말이 다르게 해주세요. 이 단계를 반복하며, 7번의 전환 후에 해피엔딩으로 이야기를 마무리합니다."
                " 주제: 백설공주 "
                "주인공: 김진용. "
                "아래의 요구사항도 꼭 지켜주시기 바랍니다."
                "피노키오의 원래 주인공인 '피노키오'를 '김진용'으로 바꿔주세요. "
                "이것은 한국과 미국의 5-7세 아이를 위한 한국어&영어 교육용입니다."
                " 한국어로 반환 해주셨으면, 그 다음에 영어로도 반환 해주세요. "
                "각 이야기는 약 50단어 길이입니다. 기본 300 단어만 사용합니다."
                "## ----- 아래의 형식으로만 반환해주세요"

                "1. 내용1(한국어로)"
                "2. 내용2(한국어로)"

                "@@@@@"

                "1. content(영어로)"
                "2. content(영어로)"
     },
]

messages = []
while True:
    user_content = input("user : ")
    messages.append({"role": "user", "content": f"{user_content}"})

    # 대화를 사용하여 GPT-3 모델에 요청
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    assistant_content = completion.choices[0].message["content"].strip()

    messages.append({"role": "assistant", "content": f"{assistant_content}"})

    # 모델의 응답 확인
    print(assistant_content)