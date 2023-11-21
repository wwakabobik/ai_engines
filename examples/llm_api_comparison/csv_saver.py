# -*- coding: utf-8 -*-
"""
Filename: csv_saver.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 21.11.2023
Last Modified: 21.11.2023

Description:
This file contains the function for saving metrics to csv file.
"""

import csv
import os


def save_to_csv(file_name, model_name, question, metrics):
    """
    Save metrics to csv file.

    :param file_name: The name of the file to save to.
    :type file_name: str
    :param model_name: The name of the model.
    :type model_name: str
    :param question: The question to save.
    :type question: str
    :param metrics: The metrics to save.
    :type metrics: dict
    """
    file_exists = os.path.isfile(file_name)

    with open(file_name, "a", newline="") as csvfile:
        fieldnames = [
            "Model",
            "Question",
            "Elapsed Time",
            "Words",
            "Chars",
            "Tokens",
            "Word Speed",
            "Char Speed",
            "Token Speed",
            "Results",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "Model": model_name,
                "Question": question,
                "Elapsed Time": metrics["elapsed_time"],
                "Words": metrics["words"],
                "Chars": metrics["chars"],
                "Tokens": metrics["tokens"],
                "Word Speed": metrics["word_speed"],
                "Char Speed": metrics["char_speed"],
                "Token Speed": metrics["token_speed"],
                "Results": metrics["results"],
            }
        )
