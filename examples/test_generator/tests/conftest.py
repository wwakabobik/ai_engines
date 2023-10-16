from time import sleep

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def pytest_runtest_makereport(item, call):
    if "driver" in item.fixturenames:
        web_driver = item.funcargs["driver"]
        if call.when == "call" and call.excinfo is not None:
            with open(f"{item.nodeid.split('::')[1]}.html", "w", encoding="utf-8") as file:
                file.write(web_driver.page_source)


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--headless")
    options.headless = True
    path = ChromeDriverManager().install()
    _driver = webdriver.Chrome(service=ChromeService(executable_path=path, options=options), options=options)

    yield _driver

    _driver.close()
    _driver.quit()
