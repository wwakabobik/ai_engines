# -*- coding: utf-8 -*-
"""
Filename: migrate_chroma.py
Author: Iliya Vereshchagin
Copyright (c) 2025. All rights reserved.
Created: 20.11.2025
Last Modified: 20.11.2025
Description:
This file contains a migration script that transfers data from an old ChromaDB format to a new format.
Migration script that runs entirely inside the CURRENT environment.

Steps:
1. pip install -r requirements_old.txt
2. run export_old_chroma.py
3. pip install -r requirements_new.txt
4. run import_new_chroma.py
"""

#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys


def run(cmd: list[str]) -> None:
    """
    Run a command in a subprocess and print it.

    :param cmd: Command to run as a list of strings.
    :type cmd: list[str]
    """
    print("[CMD]", " ".join(cmd))
    subprocess.check_call(cmd)


def pip_install_requirements(file_path: str) -> None:
    """
    Install packages from a requirements file using pip.

    :param file_path: Path to the requirements file.
    :type file_path: str
    """
    print(f"[PIP] Installing from {file_path}")
    run([sys.executable, "-m", "pip", "install", "-r", file_path])


def main(args_list=None) -> None:
    """
    Main function to handle the migration process.

    :param args_list: List of command-line arguments. If None, uses sys.argv.
    :type args_list: list[str] | None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-path", required=True)
    parser.add_argument("--new-path", required=True)
    parser.add_argument("--export-script", default=None)
    parser.add_argument("--import-script", default=None)
    parser.add_argument("--output", default="chroma_export.json")
    parser.add_argument("--requirements-old", default="requirements_old.txt")
    parser.add_argument("--requirements-new", default="requirements_new.txt")

    args = parser.parse_args(args_list)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    export_script = os.path.abspath(args.export_script) if args.export_script else os.path.join(base_dir, "export_old_chroma.py")
    import_script = os.path.abspath(args.import_script) if args.import_script else os.path.join(base_dir, "import_new_chroma.py")
    output_json = os.path.abspath(args.output)

    # 1) Install OLD dependencies
    pip_install_requirements(args.requirements_old)

    # 2) Export old DB
    print("[MIGRATE] Exporting old ChromaDB...")
    run([
        sys.executable,
        export_script,
        "--old-path", args.old_path,
        "--output", output_json
    ])

    # 3) Install NEW dependencies
    pip_install_requirements(args.requirements_new)

    # 4) Import into new DB
    print("[MIGRATE] Importing into new ChromaDB...")
    run([
        sys.executable,
        import_script,
        "--new-path", args.new_path,
        "--input", output_json
    ])

    print("===================================================")
    print("[MIGRATE] Migration complete!")
    print("===================================================")


if __name__ == "__main__":
    main()
