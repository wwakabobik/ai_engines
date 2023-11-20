# AI Engines

This is playground and utils libraries for AI stuff.

It is not a framework, but a collection of useful tools and examples. It's not a pinned repo, not a featured and supported, and in general violates all the best practices of software development. But it's a good place to start. At the beginning and the end of all, this repo contains stuff that I mentioned in my articles, thus, refer to [my blog](https://wwakabobik.github.io/) posts first.

## What you can find here

- [x] [**examples**](/examples) - a collection of examples of AI projects, including:
  - [x] [image_generation](/examples/image_generation) - a simple example of image generation using DALLE and Leonardo
  - [x] [speak_and_hear](/examples/speak_and_hear) - see [article](https://wwakabobik.github.io/2023/09/ai_learning_to_hear_and_speak/) first, this is LLM speech recognition and TTS example
  - [x] [test_generator](/examples/test_generator) - see [article](https://wwakabobik.github.io/2023/10/qa_ai_practices_used_for_qa/) first, this is QA automatic tests generator
  - [x] [llm_api_comparison](/examples/llm_api_comparison) - TBD
- [x] [**utils**](/utils) - a collection of useful tools for AI development, in general them all of them used in example projects:
  - [x] [article_extractor](/utils/article_extractor.py) - limbo for article extraction from web pages
  - [x] [audio_recorder](/utils/audio_recorder.py) - a simple audio recorder, used in speech recognition / TTS examples
  - [x] [logger_config](/utils/logger_config.py) - general logger
  - [x] [other](/utils/other.py) - all that doesn't fit in other files, i.e. env checkers
  - [x] [page_retriever](/utils/page_retriever.py) - web page retriever and parser
  - [x] [transcriptors](/utils/transcriptors.py) - custom transcriptors wrappers for speech recognition
  - [x] [translators](/utils/translators.py) - custom translators for text translation wrappers
  - [x] [tts](/utils/tts.py) - custom TTS engines wrappers

## Running up that hill

Once again, refer to [my blog](https://wwakabobik.github.io/) posts first. If you do so, you may try exec some top-level scripts from parent directory:
    
```bash
git clone git@github.com:wwakabobik/ai_engines.git  # clone this repo
cd ai_engines  # go to repo directory
# It's highly recommended to use python 3.11+ and venv
python -m venv venv  # create virtual environment
source venv/bin/activate  # activate virtual environment
pip install -r requirements.txt  # install dependencies
# then you may run some top-level script, like:
PYTHONPATH=. python -m examples.test_generator.generator_test
PYTHONPATH=. python -m examples.speak_and_hear.test_gpt 
```

Well, in most cases you need to create cred file to run examples, so, create `creds.py` under `examples` directory and fill it with your credentials, like:

```python
# -*- coding: utf-8 -*-
"""Creds file"""
oai_token = "alksjdlksajlkdjlajiouoieuoqijnc"
oai_organization = "slkahkdjshakjhfkjafs"
cohere_token = "saklljlkdjsaldjljasldjlsak"
llama_token="asiuoiduaosudouasosuoduoqoihicdhzch"
ablt_token="sadhsakhdajskhaskdkja"
claude_token="dkshjjsdhkjdshkjhskj"
openweathermap_appid = "salkdjaslkjldasjlkdasl"
midjourney_cookie="skjaklshkldfhkjsahjhfkjbkfsa"
```

GL&HF!
