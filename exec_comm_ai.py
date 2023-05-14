from api_requests import request_response_from_ai_model
from defines import (
    INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING,
    INSTRUCT_WIZARDLM_PROMPT_HEADER,
)


def main():
    # For reverse-proxied streaming, the remote will likely host with ssl - https://
    # URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'

    prompt = f"{INSTRUCT_WIZARDLM_PROMPT_HEADER}What is the capital of France?{INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING}:"

    response = request_response_from_ai_model(prompt)

    print(response)


if __name__ == "__main__":
    main()
