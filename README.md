# AI agents for simulations (LLM-based)
A Python project that uses LLMs to simulate intelligence in virtual agents.

## Instructions
**1)** Install the requirements of the repository:

```
pip install -r requirements.txt
```

**2)** Go through the trouble of installing the [text generation webui](https://github.com/oobabooga/text-generation-webui), download a local LLM of your choice (I'm using *4bit_WizardLM-13B-Uncensored-4bit-128g*). Run oobabooga's server. I'm using the following command:

```
python server.py --model-menu --listen --no-stream --extensions api
```

**3)** In the *defines.py* file you will find the following constant:

```python
USE_GPT = False
```

If you set it to true, you'll need to have a file called *api_key.txt* that contains only your OpenAI API key, so it can send requests to gpt-3.5-turbo. Obviously you need a paid subscription to do this.

## Tests
You can run the unit tests with the following command:

```
python -m unittest discover
```

Note that the tests require at least access to the local LLM running on oobabooga's server.