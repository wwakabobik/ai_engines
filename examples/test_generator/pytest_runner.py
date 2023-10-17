"""This module runs pytest and returns the results in JSON format."""
import io
import json
from os import remove

import pytest

from utils.page_retriever import PageRetriever


def run_tests(test_files, add_failed_html=True, add_failure_reasons=True, count_of_htmls=1):
    """
    Run tests and return results in JSON format.

    :param test_files: (list) list with test files.
    :param add_failed_html: (bool) boolean to add html report.
    :param add_failure_reasons: (bool) boolean to add failure reasons.
    :param count_of_htmls: (int) count of htmls to add. Doesn't recommend to use more than 1.

    :return: JSON with results.
    """
    pytest.main(
        [
            "-q",
            "--json-report",
            "--json-report-file=test_report.json",
            "-n=4",
            "-rfEx --tb=none -p no:warnings -p no:logging",
        ]
        + test_files
    )

    with open("test_report.json", encoding="utf-8") as json_file:
        data = json.load(json_file)

    results = {"passed": [], "failed": [], "error": [], "failure details": {}, "failed_pages": {}}

    for test in data["tests"]:
        node_name = test["nodeid"].split("::")[1]
        if test["outcome"] == "passed":
            results["passed"].append(node_name)
        elif test["outcome"] == "failed" or test["outcome"] == "error":
            results[test["outcome"]].append(node_name)
            if add_failure_reasons:
                results["failure details"][node_name] = {node_name: test["call"]["crash"]}
            if add_failed_html:
                if len(results["failed_pages"]) < count_of_htmls:
                    results["failed_pages"][node_name] = {node_name: parse_error_page(node_name)}

    json_results = json.dumps(results)

    return json_results


def parse_error_page(node_name):
    """
    Parse error page.

    :param node_name: (str) name of the node.

    :return: (str) formatted content of the page.
    """
    parser = PageRetriever()
    try:
        file_name = f"{node_name}.html"
        with open(file_name, "r", encoding="utf-8") as file:
            formatted_content = parser.remove_script_tags(parser.extract_body_content(file))
        remove(file_name)
        return formatted_content
    except io.UnsupportedOperation:
        return "No page available."
