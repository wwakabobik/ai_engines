import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--headless")
    _driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def save_page_source_on_failure():
        if request.node.rep_call.failed or request.node.rep_call.error:
            page_html = _driver.page_source
            request.node.user_properties.append(("page_html", page_html))

    request.addfinalizer(save_page_source_on_failure)

    return _driver
