# -*- coding: utf-8 -*-
"""
Filename: conftest.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 15.10.2023
Last Modified: 17.10.2023

Description:
This file contains pytest fixtures for tests
"""
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def pytest_runtest_makereport(item, call):
    """
    Pytest hook for saving html page on test failure

    :param item: pytest item
    :param call: pytest call
    """
    if "driver" in item.fixturenames:
        web_driver = item.funcargs["driver"]
        if call.when == "call" and call.excinfo is not None:
            with open(f"{item.nodeid.split('::')[1]}.html", "w", encoding="utf-8") as file:
                file.write(web_driver.page_source)


@pytest.fixture
def driver():
    """
    Pytest fixture for selenium webdriver

    :return: webdriver
    """
    options = Options()
    options.add_argument("--headless")
    options.headless = True
    path = ChromeDriverManager().install()
    _driver = webdriver.Chrome(service=ChromeService(executable_path=path, options=options), options=options)

    yield _driver

    _driver.close()
    _driver.quit()
