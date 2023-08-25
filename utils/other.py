# -*- coding: utf-8 -*-
"""
Filename: other.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 25.08.2023

Description:
This file contains several other stuff.
"""

import os


def is_heroku_environment():
    """
    Check current env - are we on Heroku or not

    Args:
    - None

    Returns:
    - bool: True is current environment is Heroku, otherwise - False.
    """
    return "DYNO" in os.environ and "PORT" in os.environ
