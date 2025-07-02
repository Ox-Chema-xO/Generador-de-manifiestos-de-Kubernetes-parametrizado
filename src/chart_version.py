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
    Guardar todo los templatees y values en version especifica
    """
    version_dir = os.path.join(VERSIONS_DIR, version)
    os.makedirs(version_dir, exist_ok=True)

    saved = False
    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith((".template", ".yaml")):
            src_path = os.path.join(TEMPLATE_DIR, filename)
            dest_path = os.path.join(version_dir, filename)

            with open(src_path, 'r') as src, open(dest_path, 'w') as dest:
                dest.write(src.read())

            update_index(filename, version)
            saved = True
            print(f"Guardado: {filename} en version {version}")
    
    if not saved:
        print(f"No se encontro ningun archivo .template ni .yaml en templates/")            


def load_all_templates(version):
    """
    Restaura todos los templates y values desde una version
    """
    version_dir = os.path.join(VERSIONS_DIR, version)
    if not os.path.exists(version_dir):
        print(f"Version {version} no existe")
        return

    restored = False
    for filename in os.listdir(version_dir):
        src_path = os.path.join(version_dir, filename)
        dest_path = os.path.join(TEMPLATE_DIR, filename)

        with open(src_path, 'rb') as src, open(dest_path, 'wb') as dst:
            dst.write(src.read())

        restored = True
        print(f"Restaurado: {filename} desde version {version}")

    if not restored:
        print(f"No hay archivos en la version {version}")


def list_template_versions():
    """
    Lista todas las versiones guardadas
    """
    if not os.path.exists(INDEX_FILE):
        print("No hay versiones guardadas")
        return

    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)

    print("Versiones disponibles:")
    for filename, versions in index.items():
        print(f"  {filename}: {', '.join(sorted(versions))}")

def update_index(filename, version):
    """
    Actualizar los index de versiones en el index.json
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
       python3 src/chart_versions.py load-all <version>
       python3 src/chart_versions.py list
    """

    command = sys.argv[1]
    
    if command == "save-all" and len(sys.argv) == 3:
        save_all_templates(sys.argv[2])
    elif command == "load-all" and len(sys.argv) == 3:
        load_all_templates(sys.argv[2])
    elif command == "list":
        list_template_versions()
    else:
        print("Comando invalido")
