# -*- coding: utf-8 -*-
"""
Filename: page_retriever.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 30.09.2023
Last Modified: 17.10.2023

Description:
This module contains implementation for PageRetriever
"""
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class PageRetriever:
    """The PageRetriever class is for managing an instance of the PageRetriever."""

    def __init__(self, url=""):
        """
        General init.

        :param url: (str) URL of the page.
        """
        options = Options()
        options.add_argument("--headless")
        options.headless = True
        path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(service=ChromeService(executable_path=path), options=options)
        self.url = url

    def set_url(self, url):
        """
        Set the url.

        :param url: (str) URL of the page.
        """
        self.url = url

    def get_page(self, url=None):
        """
        Get the page content from the url.

        :param url: (str) URL of the page.
        :return: (str) HTML content of the page.
        """
        if url:
            self.set_url(url)
        return self.get_page_content(self.url)

    def get_body(self, url=None):
        """
        Get the body content of the page.

        :param url: (str) URL of the page.
        :return: (str) Body content of the page.
        """
        if url:
            self.set_url(url)
        return self.extract_body_content(self.get_page())

    def get_body_without_scripts(self, url=None):
        """
        Get the body content of the page without <script>...</script> tags.

        :param url: (str) URL of the page.

        :return: (str) Body content of the page without <script>...</script> tags.
        """
        if url:
            self.set_url(url)
        return self.remove_script_tags(self.get_body())

    def get_page_content(self, url):
        """
        Get the page content from the url.

        :param url: (str) URL of the page.

        :return: (str) HTML content of the page.
        """
        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        start_time = time.time()
        while True:
            network_activity = self.driver.execute_script(
                "return window.performance.getEntriesByType('resource').filter(item => "
                "item.initiatorType == 'xmlhttprequest' && item.duration == 0)"
            )
            if not network_activity or time.time() - start_time > 30:
                break

        content = self.driver.page_source
        self.driver.close()
        self.driver.quit()

        return content

    @staticmethod
    def extract_body_content(html_content):
        """
        Extract the body content from the html_content.

        :param html_content: (str) HTML content of the page.

        :return: (str) Body content of the page.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body

        return str(body_content)

    @staticmethod
    def remove_script_tags(input_content):
        """
        Remove all <script>...</script> tags from the input_content.

        :param input_content: (str) HTML content of the page.

        :return: (str) Body content of the page without <script>...</script> tags.
        """
        pattern_1 = re.compile(r"<script.*?>.*?</script>", re.DOTALL)
        pattern_2 = re.compile(r"<path.*?>.*?</path>", re.DOTALL)
        output = re.sub(pattern_1, "", input_content)
        output = re.sub(pattern_2, "", output)
        return output
