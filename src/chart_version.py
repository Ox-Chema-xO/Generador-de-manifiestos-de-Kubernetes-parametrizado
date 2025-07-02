#!/usr/bin/env python3
"""
Sistema simple de versionado para templates de Kubernetes
Permite guardar y recuperar versiones de templates existentes
"""
import os
import json
import sys

TEMPLATE_DIR = "templates"
VERSIONS_DIR = "templates_versions"
INDEX_FILE = os.path.join(VERSIONS_DIR, "index.json")


def save_all_templates(version):
    """
    Guarda todos los templates y values en una version
    """
    version_dir = os.path.join(VERSIONS_DIR, version)
    os.makedirs(version_dir, exist_ok=True)

    saved = False
    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith((".template", ".yaml")):
            src_path = os.path.join(TEMPLATE_DIR, filename)
            dest_path = os.path.join(version_dir, filename)

            with open(src_path, 'rb') as src, open(dest_path, 'wb') as dst:
                dst.write(src.read())

            _update_index(filename, version)
            saved = True
            print(f"Guardado: {filename} en version {version}")

    if not saved:
        print("No se encontro ningun .template o .yaml en templates/")

def _update_index(filename, version):
    """
    Actualiza indice de versiones por archivo
    """
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r') as f:
            index = json.load(f)
    else:
        index = {}

    if filename not in index:
        index[filename] = []

    if version not in index[filename]:
        index[filename].append(version)

    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)

if __name__ == "__main__":
    """
    Uso:
       python3 src/chart_versions.py save-all <version>
    """

    command = sys.argv[1]

    if command == "save-all" and len(sys.argv) == 3:
        save_all_templates(sys.argv[2])
    else:
        print("Comando invalido")

