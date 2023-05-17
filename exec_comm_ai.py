import requests
from defines import (
    INSTRUCT_VICUNA_1_1_PROMPT_ANSWER_OPENING,
    INSTRUCT_VICUNA_1_1_PROMPT_HEADER,
)
from errors import UnableToConnectWithAiModelError
from regular_expression_utils import remove_end_tag_from_ai_response


def try_to_get_a_test_response_from_oobabooga(prompt):
    """Tries to get a response from the oobabooga server.

    Args:
        prompt (str): the prompt that will be sent to the oobabooga server.

    Raises:
        UnableToConnectWithAiModelError: if the function is unable to retrieve a valid response from the server.

    Returns:
        str: either a valid response from the oobabooga server, or None
    """
    host = "localhost:5000"
    uri = f"http://{host}/api/v1/generate"

    request_for_oobabooga = {
        "prompt": prompt,
        "max_new_tokens": 2000,
        "do_sample": True,
        "temperature": 0.7,
        "top_p": 0.5,
        "typical_p": 1,
        "repetition_penalty": 1.2,
        "top_k": 40,
        "min_length": 0,
        "no_repeat_ngram_size": 0,
        "num_beams": 1,
        "penalty_alpha": 0,
        "length_penalty": 1,
        "early_stopping": False,
        "seed": -1,
        "add_bos_token": True,
        "truncation_length": 2048,
        "ban_eos_token": False,
        "skip_special_tokens": True,
        "stopping_strings": [],
    }

    try:
        response = requests.post(uri, json=request_for_oobabooga, timeout=25)
    except requests.exceptions.ConnectionError as exception:
        error_message = "I was unable to connect with the AI model to request a "
        error_message += (
            f"response. Are you sure it's running properly? Error: {exception}"
        )
        raise UnableToConnectWithAiModelError(error_message) from exception

    if response.status_code == 200:
        result = response.json()["results"][0]["text"]

        return prompt, result.strip()

    return prompt, None


def main():
    # For reverse-proxied streaming, the remote will likely host with ssl - https://
    # URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'

    prompt = input("Prompt: ")

    prompt = f"{INSTRUCT_VICUNA_1_1_PROMPT_HEADER}{prompt}{INSTRUCT_VICUNA_1_1_PROMPT_ANSWER_OPENING}"

    prompt, response = try_to_get_a_test_response_from_oobabooga(prompt)

    print(
        f"\nRESULTS:\nPrompt: {prompt}\nResponse: {remove_end_tag_from_ai_response(response)}"
    )


if __name__ == "__main__":
    main()
