"""This module handles operations related to API requests.

"""
# Run oobabooga server with: python server.py --model-menu --listen --wbits=4 --groupsize=128 --no-stream --extensions api

import requests

from errors import UnableToConnectWithAiModelError


def request_response_from_ai_model(prompt):
    """Requests a response from the AI model. NOTE: it should be running locally already.

    Args:
        prompt (str): the request that will be sent to the AI model.

    Returns:
        str: the AI model's response
    """

    host = "localhost:5000"
    uri = f"http://{host}/api/v1/generate"

    request = {
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
        response = requests.post(uri, json=request, timeout=25)
    except requests.exceptions.ConnectionError as exception:
        raise UnableToConnectWithAiModelError("I was unable to connect with the AI model to request a response. Are you sure it's running properly? Error: {exception}") from exception

    if response.status_code == 200:
        result = response.json()["results"][0]["text"]

        return result.strip()

    return None
