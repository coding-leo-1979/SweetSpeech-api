import os
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

AZURE_CLS_ENDPOINT = os.getenv("AZURE_CLS_ENDPOINT")
AZURE_CLS_KEY = os.getenv("AZURE_CLS_KEY")


def is_impolite_middleware(comment_text: str) -> tuple[bool, bool]:
    """
    댓글이 악플인지 여부(is_impolite)와, 수동 검토 필요 여부(needs_review)를
    Azure Classification 서비스로부터 판별한다.

    :param comment_text: 판별할 댓글 문자열
    :return: (is_impolite, needs_review)
    """
    if not AZURE_CLS_ENDPOINT or not AZURE_CLS_KEY:
        print("Azure Classification Endpoint나 Key가 설정되지 않았습니다.")
        return False, False

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AZURE_CLS_KEY}"
        }
        input_data = {
            "data": [comment_text]
        }

        response = requests.post(AZURE_CLS_ENDPOINT, headers=headers, json=input_data)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                # 결과에서 prediction, prob_hate 추출
                prediction = result[0].get("prediction", 0)
                prob_hate = result[0].get("prob_hate", 0.0)

                is_impolite = prediction == 1

                # needs_review 기준 (모호한 경우만 True)
                needs_review = 0.5 <= prob_hate < 0.9

                return is_impolite, needs_review
            else:
                print("예상치 못한 응답 형식:", result)
                return False, False
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False, False

    except Exception as ex:
        print(f"Error in is_impolite_middleware: {ex}")
        return False, False