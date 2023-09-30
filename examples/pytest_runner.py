import json
import pytest
from pytest_jsonreport.plugin import JSONReport


def run_tests(test_files):
    pytest.main(["-q", "--json-report", "--json-report-file=test_report.json"] + test_files)

    with open('test_report.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Форматируем результаты
    results = {
        "passed": [],
        "failed": [],
        "error": [],
        "failure details": {}
    }

    for test in data['tests']:
        if test['outcome'] == 'passed':
            results["passed"].append(test['nodeid'])
        elif test['outcome'] == 'failed':
            results["failed"].append(test['nodeid'])
            results["failure details"][test['nodeid']] = test['longrepr']
            page_html = next((prop[1] for prop in test['user_properties'] if prop[0] == 'page_html'), None)
            results["failed_pages"][test['nodeid']] = page_html
        elif test['outcome'] == 'error':
            results["error"].append(test['nodeid'])
            results["failure details"][test['nodeid']] = test['longrepr']
            page_html = next((prop[1] for prop in test['user_properties'] if prop[0] == 'page_html'), None)
            results["failed_pages"][test['nodeid']] = page_html

    json_results = json.dumps(results)

    return json_results
