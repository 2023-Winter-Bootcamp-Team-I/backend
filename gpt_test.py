import openai
from backend.settings import get_secret

openai.api_key = get_secret("GPT_KEY")

# 대화 데이터 정의
conversation = [
    {
        "role": "system",
        "content": f"You are a skilled children's story writer. We will create a fairy tale together. You are fluent in both Korean and English. Do not react at all, and never ask questions. Please write in a friendly manner, like a woman in her twenties."
                   f"------<초기 정보>------"
                   f"주인공 이름: 김진용"
                   f"주인공 성별: 남자"
                   f"대상 연령: 7세"
                   f"원작 동화: 아기돼지 삼형제"
                   f"---------------------"
                   f"<초기 정보> 안에 있는 정보들로 동화를 써주세요. "
                   f"2가지의 문장을 제시하는 방식으로 동화를 써주세요. "
                   f" 2개의 문장은 서로 다른 이야기가 되어야 합니다."
                   f"제가 2개 문장 중 하나를 선택하면 다음 페이지로 넘어가세요."
                   f"6페이지를 써주고, 페이지당 1문장의 이야기 구성이 되게 해주세요."
    },{
        "role": "user",
        "content": f"동화를 시작해주세요. 당신은 동화의 이야기가 끝날 때 까지 '--------------' 아래와 같은 방식으로 응답 해주시길 바랍니다"
                   f"---------------------------"
                   f"1.(한국어 내용1)"
                   f"2.(한국어 내용2)"
                   f"1.(영어 내용1)"
                   f"2.(영어 내용2)"
    }

]


while True:
    # 대화를 사용하여 GPT-3 모델에 요청
    messages = conversation
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True)

    for line in completion:
        chunk = line['choices'][0].get('delta', {}).get('content', '')
        if chunk:
            print(chunk, end='')
    user_content = input("user : ")


