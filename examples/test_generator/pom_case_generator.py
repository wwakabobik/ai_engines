""" Module for generating test files and page objects from json data."""
import os

from urllib.parse import urlparse, unquote


class PomTestCaseGenerator:
    """Class for generating test files and page objects from json data"""

    def __init__(self, url=""):
        """
        General init.

        :param url: (str) URL of the page.
        """
        self.url = url

    def set_url(self, url):
        """
        Set the url.

        :param url: (str) URL of the page.
        """
        self.url = url

    def ___create_pom_file(self, file_name, page_objects, url="", pom_folder="pom"):
        """
        Create page object model file.

        :param file_name: (str) Name of the file.
        :param page_objects: (list) List of page objects.
        :param url: (str) URL of the page.
        :param pom_folder: (str) Folder for page object model files.
        """
        if not url:
            url = self.url
        if not os.path.exists(pom_folder):
            os.makedirs(pom_folder)
        with open(f"{pom_folder}/page_{file_name}.py", "w", encoding="utf-8") as pom_file:
            pom_file.write("from selenium.webdriver.common.by import By\n")
            pom_file.write("from selenium.webdriver.support.ui import WebDriverWait\n")
            pom_file.write("from selenium.webdriver.support import expected_conditions as EC\n\n\n")
            pom_file.write(f'class Page{"".join(word.capitalize() for word in file_name.split("_"))}:\n')
            pom_file.write("    def __init__(self, driver):\n")
            pom_file.write(f'        self.url = "{url}"\n')
            pom_file.write("        self.driver = driver\n\n")
            for method in page_objects:
                pom_file.write(f"    {method}\n\n")

    @staticmethod
    def ___create_test_file(file_name, tests, pom_folder="pom", tests_folder="tests"):
        """
        Create test file.

        :param file_name: (str) Name of the file.
        :param tests: (list) List of tests.
        :param pom_folder: (str) Folder for page object model files.
        :param tests_folder: (str) Folder for test files.
        """
        with open(f"{tests_folder}/test_{file_name}.py", "w", encoding="utf-8") as test_file:
            test_file.write("import pytest\n\n")
            test_file.write(
                f'from {pom_folder}.{os.path.splitext(f"page_{file_name}")[0]} import Page'
                f'{"".join(word.capitalize() for word in file_name.split("_"))}\n\n\n'
            )
            test_file.write('@pytest.fixture(scope="function")\n')
            test_file.write("def page(driver):\n")
            test_file.write(
                f'    page_under_test = Page{"".join(word.capitalize() for word in file_name.split("_"))}(driver)\n'
            )
            test_file.write("    driver.get(page_under_test.url)\n")
            test_file.write("    return page_under_test\n\n\n")
            for test in tests:
                test_file.write(f"{test}\n\n\n")

    def create_files_from_json(self, json_data, url="", pom_folder="pom", tests_folder="tests"):
        """
        Create test and page object model files from json data.

        :param json_data: (str) JSON data.
        :param url: (str) URL of the page.
        :param pom_folder: (str) Folder for page object model files.
        :param tests_folder: (str) Folder for test files.
        """
        if not url:
            url = self.url
        parsed_url = urlparse(unquote(url))
        file_name = parsed_url.path.strip("/").replace("/", "_") or "index"
        self.___create_test_file(file_name, json_data["tests"], pom_folder="..pom", tests_folder=tests_folder)
        self.___create_pom_file(file_name, json_data["page_objects"], url, pom_folder=pom_folder)
