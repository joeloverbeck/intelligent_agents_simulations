"""This module handles operations related to API requests.

"""
# Run oobabooga server with: python server.py --model-menu --listen --no-stream --extensions api

import json
import requests
from defines import USE_GPT

from errors import UnableToConnectWithAiModelError
from logging_messages import log_debug_message


def try_to_get_a_response_from_gpt(prompt):
    """Tries to get a response from GPT

    Args:
        prompt (str): the prompt that will be sent to GPT

    Returns:
        str: either a valid response or None
    """
    # Read API key from file
    with open("api_key.txt", "r", encoding="utf8") as file:
        api_key = file.read().strip()

    api_endpoint = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    model = "gpt-3.5-turbo"
    temperature = 1
    max_tokens = None

    request = {
        "model": model,
        "messages": prompt,
        "temperature": temperature,
    }

    if max_tokens is not None:
        request["max_tokens"] = max_tokens

    response = requests.post(
        api_endpoint, headers=headers, data=json.dumps(request), timeout=25
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    if response.status_code == 400:
        log_debug_message(
            f"Request to '{model}' failed due to BadRequestError: {response.text}"
        )
    if response.status_code == 401:
        log_debug_message(
            f"Request to '{model}' failed due to UnauthorizedError: {response.text}"
        )
    if response.status_code == 403:
        log_debug_message(
            f"Request to '{model}' failed due to ForbiddenError: {response.text}"
        )
    if response.status_code == 404:
        log_debug_message(
            f"Request to '{model}' failed due to NotFoundError: {response.text}"
        )
    if response.status_code == 429:
        log_debug_message(
            f"Request to '{model}' failed due to NotFoundError: {response.text}"
        )
    if response.status_code == 502:
        log_debug_message(
            f"Request to '{model}' failed due to ModelOverloadedError: {response.text}"
        )

    return None


def try_to_get_a_response_from_oobabooga(prompt):
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

        return result.strip()

    return None


def request_response_from_ai_model(prompt):
    """Requests a response from the AI model.
    NOTE: it should be running locally already if you're not using USE_GPT = True

    Args:
        prompt (str): the request that will be sent to the AI model.

    Returns:
        str: the AI model's response
    """

    # If the define USE_GPT is set as True, we first try to get a response from
    # GPT through the OpenAI API key.

    if USE_GPT:
        response = try_to_get_a_response_from_gpt(prompt)

        if response is not None:
            return response

    return try_to_get_a_response_from_oobabooga(prompt)
