# -*- coding: utf-8 -*-
"""
Filename: migrate_chroma_test.py
Author: Iliya Vereshchagin
Copyright (c) 2025. All rights reserved.

Created: 20.11.2025
Last Modified: 20.11.2025

Description:
This file is a test script for migrating ChromaDB data from an old format to a new format.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "../../utils/chromadb_migration"
)))

from utils.chromadb_migration.migrate_chroma import main


main([
    "--old-path", "./chroma_OLD",
    "--new-path", "./chroma_NEW",
    "--output", "./chroma_export.json"
])
