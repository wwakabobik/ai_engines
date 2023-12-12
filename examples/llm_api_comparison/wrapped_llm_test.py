# -*- coding: utf-8 -*-
"""
Filename: wrapped_llm_test.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 21.11.2023
Last Modified: 21.11.2023

Description:
This file contains benchmarks for wrapped LLMs models.
"""

from ablt_python_api import ABLTApi

# pylint: disable=import-error
from examples.creds import ablt_token  # type: ignore
from examples.llm_api_comparison.ablt_models import unique_models  # type: ignore
from examples.llm_api_comparison.csv_saver import save_to_csv
from examples.llm_api_comparison.llm_questions import llm_questions
from utils.llm_timer_wrapper import TimeMetricsWrapperSync

# Initialize LLM with tokens
ablt = ABLTApi(ablt_token)


@TimeMetricsWrapperSync
def check_chat_ablt_response(prompt, model):
    """
    Check chat response from ABLT API.

    :param prompt: The prompt to use for the function.
    :type prompt: str
    :param model: The model to use for the function.
    :type model: str
    :return: The metrics of the function.
    :rtype: dict
    """
    return ablt.chat(bot_slug=model, prompt=prompt, max_words=None, stream=False).__next__()


def main():
    """Main function for benchmarking LLMs"""
    error_counter = 5
    for prompt in llm_questions:
        for model in unique_models:
            while True:
                try:
                    response = check_chat_ablt_response(prompt, model)
                    save_to_csv(file_name="llm_wrapped.csv", model_name=model, question=prompt, metrics=response)
                    error_counter = 5
                    break
                except Exception as error:  # pylint: disable=broad-except
                    if error_counter == 0:
                        print("Broken API? Skipping...")
                        break
                    print(f"Ooops, something went wrong: '{error}'. Retrying {5 - error_counter}/5...")
                    error_counter -= 1


main()
