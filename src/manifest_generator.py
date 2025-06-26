#!/usr/bin/env python3
"""
Generador de manifiestos k8s a partir de templates y values
"""
import yaml
import argparse
import os
from jinja2 import Template


def cargar_values(ruta_values):
    """
    Carga valores desde values.yaml
    """
    try:
        with open(ruta_values, 'r', encoding='utf-8') as f:
            values = yaml.safe_load(f)
        return values
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {ruta_values}")
        return None
    except yaml.YAMLError as e:
        print(f"Error al leer values.yaml: {e}")
        return None


def cargar_template(ruta_template):
    """
    Carga el contenido de template
    """
    try:
        with open(ruta_template, 'r', encoding='utf-8') as f:
            contenido_template = f.read()
        return contenido_template
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {ruta_template}")
        return None


def generar_manifiesto(contenido_template, values):
    """
    Genera manifiesto procesando template con values
    """
    try:
        # Se crea objeto template de jinja2
        template = Template(contenido_template)
        # Remplaza placeholders con values
        manifiesto = template.render(**values)
        print("Manifiesto generado exitosamente")
        return manifiesto
    except Exception as e:
        print(f"Error al generar manifiesto: {e}")
        return None


def guardar_manifiesto(contenido_manifiesto, ruta_output):
    """
    Guarda el manifiesto en un archivo
    """
    try:
        directorio_output = os.path.dirname(ruta_output)
        if directorio_output:
            os.makedirs(directorio_output, exist_ok=True)
        with open(ruta_output, 'w', encoding='utf-8') as f:
            f.write(contenido_manifiesto)
        print(f"Manifiesto guardado en: {ruta_output}")
    except Exception as e:
        print(f"Error al guardar archivo: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generador de manifiestos de kubernetes"
    )
    parser.add_argument(
        '--template', '-t',
        required=True,
        help='Ruta al archivo de template (.template)'
    )
    parser.add_argument(
        '--values', '-v',
        required=True,
        help='Ruta al archivo de values (.yaml)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Ruta del archivo de output (opcional)'
    )
    args = parser.parse_args()

    values = cargar_values(args.values)
    if not values:
        return 1
    contenido_template = cargar_template(args.template)
    if not contenido_template:
        return 1
    manifiesto = generar_manifiesto(contenido_template, values)
    if not manifiesto:
        return 1
    print("\nManifiesto generado:")
    print("-" * 30)
    print(manifiesto)
    # Guardar en archivo solo si se especifica el output
    if args.output:
        guardar_manifiesto(manifiesto, args.output)
    return 0


if __name__ == "__main__":
    exit(main())
