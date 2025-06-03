import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Azure OpenAI client 초기화
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

client = AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version="2024-05-01-preview"
)

def polite_comment_middleware(comment_text: str) -> str:
    """
    댓글 내용을 Azure OpenAI로 정중하게 순화하는 함수.
    """
    try:
        system_message = (
            "당신은 사용자의 발화를 정중하고 공손한 표현으로 순화해주는 언어 도우미입니다. "
            "사용자가 어떤 문장을 입력하든, 그 의미는 그대로 유지하면서 상대방에게 불쾌감을 주지 않는 방식으로 표현을 바꿔주세요. "
            "말투(존댓말, 반말 등)는 절대 바꾸지 말고, 사용자의 원래 말투를 그대로 유지하세요. "
            "답변은 순화된 문장 하나만 출력하고, 그 외의 설명은 생략하세요."
        )

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": comment_text}
        ]

        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.3,
            top_p=0.7,
            max_tokens=1000,
            messages=messages
        )

        polite_comment = response.choices[0].message.content.strip()
        return polite_comment
    
    except Exception as e:
        # 문자열 형태로 에러 메시지를 추출
        error_str = str(e)

        # 콘텐츠 필터 코드 포함 여부 확인
        if "content_filter" in error_str or "ResponsibleAIPolicyViolation" in error_str:
            return "순화할 수 없는 댓글입니다."
        elif "404" in error_str:
            return "순화할 수 없는 댓글입니다."
        elif "500" in error_str:
            return "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        else:
            print(f"Unhandled error: {error_str}")
            return "시스템 오류가 발생했습니다. 잠시 후 다시 시도해주세요."