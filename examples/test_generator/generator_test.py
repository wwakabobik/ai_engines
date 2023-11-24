# -*- coding: utf-8 -*-
"""
Filename: generator_test.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 16.10.2023
Last Modified: 17.10.2023

Description:
This file contains testing procedures for ChatGPT experiments
"""

import json
import logging

import asyncio
from openai_python_api import ChatGPT

# pylint: disable=import-error
from examples.creds import oai_token, oai_organization  # type: ignore
from examples.test_generator.gpt_functions import gpt_functions, gpt_functions_dict
from examples.test_generator.pom_case_generator import PomTestCaseGenerator
from utils.logger_config import setup_logger

generator = PomTestCaseGenerator(url="https://www.saucedemo.com/")
# generator = PomTestCaseGenerator(url='https://automationintesting.com/selenium/testpage/')


SYSTEM_INSTRUCTIONS = """
You're bot responsible for QA automation testing. You tech stack is selenium + pytest. I will provide you url for testing.

1) You may obtain page code by calling "get_page_code" function. It will return you:
 raw HTML document, what needs to be tested (guarded by ```). And you need to respond with json in following format:
{
"page_objects": [
"@property\\n
    def calculate_button(self):\\n
        return WebDriverWait(self.driver, 10).until(\\n
            EC.presence_of_element_located((By.XPATH, '//button[.='''Calculate''']'))\\n
        )", <...>
],
"tests": ["def test_division_by_zero(page):\\n
    page.numbers_input.send_keys(1024)\\n
    page.divide_button.click()\\n
    page.calculator_input.send_keys('0')\\n
    page/calculate_button.click()\\n
    assert page.error.text() == 'Error: divide by zero'", <...>],
}
This means you need to create page objects for each object on the page using laconic and stable XPATH locators (as short and stables as you can, use only By.XPATH locators, not By.ID, not By.CSS_SELECTOR or By.CLASS name), and then create all possible test cases for them. It might be some filed filling tests (errors, border checks, positive and negative cases), clicking, content changing, etc. Please respect to use 'page' fixture for every test, it's predefined in code and opens page under test before it.
2) Then I may ask you to execute some tests. You can run demanded test via "get_tests_results" function, based on gathered content, you need to respond with json in following format:
results = {
    "passed": [],
    "failed": [],
    "error": [],
    "failure details": {}
}
where "failure details" - is dict with keys equal to test names (which you generated) and possible failures details. If you got an failures and errors, you need to respond as in 1 with fixed code (page objects and/or tests).
Answer only with JSON in format I mentioned in 1. Never add anything more than that (no explanations, no extra text, only json).
3) In addition to 1 and 2 i may pass you extra info what kind of test data might be used (i.e. for form filling), but in general you need to generate all possible scenarios (valid/invalid/border cases, always add what's not listed by user, but should be for best quality of testing coverage).
"""


def setup_gpt():
    """Setup GPT bot with appropriate functions and settings"""
    gpt = ChatGPT(auth_token=oai_token, organization=oai_organization, model="gpt-4-0613")
    gpt.logger = setup_logger("gpt", "gpt.log", logging.INFO)  # supress DEBUG output of the ChatGPT
    gpt.system_settings = ""
    gpt.function_dict = gpt_functions_dict
    gpt.function_call = "auto"
    gpt.functions = gpt_functions
    gpt.system_settings = SYSTEM_INSTRUCTIONS
    return gpt


async def main():
    """Main function for testing GPT bot"""
    print("===Setup GPT bot===")
    gpt = setup_gpt()
    print("===Get page code of https://www.saucedemo.com/ and generate POM and tests===")
    response = await anext(gpt.str_chat("Get page code of https://www.saucedemo.com/ and generate POM and tests"))
    print(response)
    response = response.replace("\n", "")
    generator.create_files_from_json(
        json.loads(response), pom_folder="examples/test_generator/pom", tests_folder="examples/test_generator/tests"
    )
    print("===Get tests results for examples/test_generator/tests/test_index.py==")
    response = await anext(gpt.str_chat("Get tests results for examples/test_generator/tests/test_index.py"))
    print(response)
    print("===If there are failures in code, please fix it by fixing POM and tests===")
    response = await anext(gpt.str_chat("If there are failures in code, please fix it by fixing POM and tests"))
    print(response)
    generator.create_files_from_json(
        json.loads(response), pom_folder="..pom", tests_folder="examples/test_generator/tests"
    )


asyncio.run(main())
