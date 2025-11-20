# -*- coding: utf-8 -*-
"""
Filename: export_old_chroma.py
Author: Iliya Vereshchagin
Copyright (c) 2025. All rights reserved.
Created: 20.11.2025
Last Modified: 20.11.2025
Description:
This script exports a Chroma collection from an old ChromaDB (version < 0.7.0)
to a JSON file for migration purposes.
Сщmpatible with ChromaDB 0.6.x / langchain_chroma wrapper.
"""

#!/usr/bin/env python3

import json
import argparse
from langchain_chroma import Chroma
import os

def export_old_chroma(old_path: str, output_file: str, collection_name: str) -> None:
    """
    Export the Chroma collection from the old ChromaDB directory to a JSON file.

    :param old_path: Path to the old ChromaDB directory.
    :type old_path: str
    :param output_file: Path to the output JSON file.
    :type output_file: str
    :param collection_name: Name of the Chroma collection to export.
    :type collection_name: str
    """
    print(f"[EXPORT] Connecting to old ChromaDB at {old_path}")

    original_cwd = os.getcwd()
    os.chdir(old_path)

    try:
        collection = Chroma(
            collection_name=collection_name,
            persist_directory=old_path
        )

        data = collection.get(include=["documents", "embeddings", "metadatas"])

        embeddings = [e.tolist() if hasattr(e, "tolist") else e for e in data.get("embeddings", [])]

        export_data = {
            collection_name: {
                "ids": [m.get("id") for m in data.get("metadatas", [])],
                "documents": data.get("documents", []),
                "embeddings": embeddings,
                "metadatas": data.get("metadatas", []),
            }
        }

        print(f"[EXPORT] Exported {len(export_data[collection_name]['ids'])} entries from `{collection_name}`")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"[EXPORT] Completed. Saved to {output_file}")

    finally:
        os.chdir(original_cwd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection-name", default="memory", help="Name of the Chroma collection to export")
    parser.add_argument("--old-path", required=True, help="Path to old ChromaDB directory")
    parser.add_argument("--output", default="chroma_export.json", help="Path to output JSON file")
    args = parser.parse_args()

    export_old_chroma(args.old_path, args.output, args.collection_name)


if __name__ == "__main__":
    main()
