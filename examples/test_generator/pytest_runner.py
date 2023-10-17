"""This module runs pytest and returns the results in JSON format."""
import io
from os import remove

import json
import pytest

from utils.page_retriever import PageRetriever


def run_tests(test_files, add_failed_html=True, add_failure_reasons=True, count_of_htmls=1):
    """
    Run tests and return results in JSON format.

    Args:
        test_files: list with test files.
        add_failed_html: boolean to add html report.
        add_failure_reasons: boolean to add failure reasons.
        count_of_htmls: count of htmls to add. Doesn't recommend to use more than 1.

    Returns:
        JSON with results.

    """
    pytest.main(["-q", "--json-report", "--json-report-file=test_report.json", "-n=4", "-rfEx --tb=none -p no:warnings -p no:logging"] + test_files)

    with open('test_report.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    results = {
        "passed": [],
        "failed": [],
        "error": [],
        "failure details": {},
        "failed_pages": {}
    }

    for test in data['tests']:
        node_name = test['nodeid'].split('::')[1]
        if test['outcome'] == 'passed':
            results["passed"].append(node_name)
        elif test['outcome'] == 'failed' or test['outcome'] == 'error':
            results[test['outcome']].append(node_name)
            if add_failure_reasons:
                results["failure details"][node_name] = {node_name: test['call']['crash']}
            if add_failed_html:
                if len(results["failed_pages"]) < count_of_htmls:
                    results["failed_pages"][node_name] = {node_name: parse_error_page(node_name)}

    json_results = json.dumps(results)

    return json_results


def parse_error_page(node_name):
    """
    Parse error page.

    Args:
        node_name: name of the node.

    Returns:
        string with parsed page.
    """
    parser = PageRetriever()
    try:
        formatted_content = ''
        file_name = f"{node_name}.html"
        with open(file_name, "r", encoding="utf-8") as file:
            formatted_content = parser.remove_script_tags(parser.extract_body_content(file))
        remove(file_name)
        return formatted_content
    except io.UnsupportedOperation:
        return "No page available."
