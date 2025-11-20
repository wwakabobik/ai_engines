# -*- coding: utf-8 -*-
"""
Filename: import_new_chroma.py
Author: Iliya Vereshchagin
Copyright (c) 2025. All rights reserved.
Created: 20.11.2025
Last Modified: 20.11.2025
Description:
This script imports exported collections into the NEW langchain_chroma / ChromaDB 1.x
(using precomputed embeddings to avoid OpenAI API calls and token limits)
"""

#!/usr/bin/env python3

import argparse
import json
import os

from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings

class DummyEmbeddings(Embeddings):
    """A dummy embedding class that returns zero vectors."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Returns a list of zero vectors for the given texts.

        :param texts: The input texts to embed.
        :type texts: list[str]
        :return: A list of zero vectors.
        :rtype: list[list[float]]
        """
        return [[0.0]] * len(texts)
    def embed_query(self, text) -> list[float]:
        """
        Returns a zero vector for the given text.

        :param text: The input text to embed.
        :type text: str
        :return: A zero vector.
        :rtype: list[float]
        """
        _ = text  # Ignore input text
        return [0.0]

def import_new_chroma(new_path: str, input_file: str) -> None:
    """
    Import the exported collections into the new ChromaDB directory.

    :param new_path: Path to the new ChromaDB directory.
    :type new_path: str
    :param input_file: Path to the exported JSON file.
    :type input_file: str
    """
    print(f"[IMPORT] Connecting to NEW ChromaDB at {new_path}")
    os.makedirs(new_path, exist_ok=True)

    collection = Chroma(
        collection_name="memory_160120470",
        embedding_function=DummyEmbeddings(),
        persist_directory=new_path
    )

    with open(input_file, "r", encoding="utf-8") as f:
        export = json.load(f)

    for col_name, data in export.items():
        print(f"[IMPORT] Importing collection `{col_name}`")

        documents = data["documents"]
        metadatas = data["metadatas"]
        embeddings = data["embeddings"]
        ids = data["ids"]

        collection._collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids
        )

        print(f"[IMPORT] Imported {len(documents)} items for `{col_name}`")

    print("[IMPORT] Done!")

def main() -> None:
    """Main function to parse arguments and call the import function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-path", required=True, help="Path to new ChromaDB directory")
    parser.add_argument("--input", default="chroma_export.json", help="Exported JSON file")
    args = parser.parse_args()

    import_new_chroma(args.new_path, args.input)

if __name__ == "__main__":
    main()
