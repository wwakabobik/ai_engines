# -*- coding: utf-8 -*-
"""
Filename: __gpt_functions__.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 16.10.2023
Last Modified: 16.10.2023

Description:
This file contains testing procedures for ChatGPt experiments
"""

from examples.test_generator.pytest_runner import run_tests
from utils.page_retriever import PageRetriever

doc_engine = PageRetriever()
gpt_functions = [
    {
        "name": "get_page_code",
        "description": "Get page code to generate locators and tests",
        "parameters": {
            "type": "object",
            "properties": {"url": {"type": "string", "description": "The URL of the page to get the code from"}},
            "required": [],
        },
    },
    {
        "name": "get_tests_results",
        "description": "Get the results of the tests",
        "parameters": {
            "type": "object",
            "properties": {
                "test_files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The list of test files to run",
                }
            },
            "required": [],
        },
    },
]

gpt_functions_dict = {
    "get_page_code": doc_engine.get_body_without_scripts,
    "get_tests_results": run_tests,
}
