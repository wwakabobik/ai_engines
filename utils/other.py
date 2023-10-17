# -*- coding: utf-8 -*-
"""
Filename: other.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 17.10.2023

Description:
This file contains several other stuff.
"""

import os


def is_heroku_environment():
    """
    Check current env - are we on Heroku or not

    :return: True if we are on Heroku, False otherwise
    """
    return "DYNO" in os.environ and "PORT" in os.environ
