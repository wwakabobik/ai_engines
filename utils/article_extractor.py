# -*- coding: utf-8 -*-
"""
Filename: article_extractor.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 17.10.2023

Description:
This file contains implementation for Article Extractor from internet page
"""

import requests
from readability import Document


# FIXME: This is a temporary solution. We need to find a better way to extract


def get_content(url):
    """
    This function extracts content from internet page.

    :param url: The URL of the page to extract content from.

    :return: The content of the page.
    """
    session = requests.Session()
    response = session.get(url)
    doc = Document(response.text)
    content = doc.summary()
    return content
