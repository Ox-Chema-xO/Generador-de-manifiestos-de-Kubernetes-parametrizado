#!/usr/bin/env python3
"""
Generador de manifiestos k8s a partir de templates y values
"""
import yaml
import argparse
import os
import jsonschema
import subprocess
import tempfile
from jinja2 import Template


esquema = {
    "type": "object",
    "properties": {
        "app_name": {"type": "string"},
        "protocol": {"type": "string"},
        "image": {"type": "string",
                  "pattern": "^[a-zA-Z0-9/_-]+(:[a-zA-Z0-9_.-]+)?$"
                  },
        "replicas": {"type": "integer", "minimum": 1},
        "container_port": {"type": "integer", "minimum": 1, "maximum": 65535},
        "service_port": {"type": "integer", "minimum": 1, "maximum": 65535}
    },
    "required": ["app_name", "protocol", "image",
                 "replicas", "container_port", "service_port"]
}


def validar_values(values):
    """
    Se valida que los values cumplan el esquema
    """
    try:
        jsonschema.validate(values, esquema)
        return True
    except jsonschema.ValidationError as e:
        print(f"Error de validacion: {e.message}")
        return False


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


def validar_manifiesto_k8s(contenido_manifiesto, nombre_archivo=""):
    """
    Valida manifiesto usando kubectl dry-run
    """
    try:
        # Crear archivo temporal con el manifiesto
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False
        ) as f:
            f.write(contenido_manifiesto)
            temp_file = f.name
        # Ejecutar kubectl dry-run --validate
        resultado = subprocess.run([
            'kubectl',
            'apply',
            '--dry-run=client',
            '--validate=true',
            '-f',
            temp_file
        ], capture_output=True, text=True)
        # Limpiar archivo temporal
        os.unlink(temp_file)
        if resultado.returncode == 0:
            print(f"Manifiesto {nombre_archivo} válido")
            return True
        else:
            print(f"Error en manifiesto {nombre_archivo}:")
            print(resultado.stderr)
            return False
    except FileNotFoundError:
        print("Error: kubectl no encontrado. Instala kubectl para validación.")
        return False
    except Exception as e:
        print(f"Error en validación: {e}")
        return False


def desplegar_manifiestos(directorio_output):
    """
    Despliega manifiestos generados usando kubectl apply
    """
    try:
        print(f"\nDesplegando manifiestos desde: {directorio_output}")
        # Ejecutar kubectl apply en el directorio
        resultado = subprocess.run([
            'kubectl', 'apply', '-f', directorio_output
        ], capture_output=True, text=True)

        if resultado.returncode == 0:
            print("Despliegue exitoso!")
            print(resultado.stdout)
            # Mostrar pods desplegados
            print("\nRecursos desplegados:")
            subprocess.run(['kubectl', 'get', 'pods,svc'],
                           capture_output=False)
            return True
        else:
            print("Error en despliegue:")
            print(resultado.stderr)
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generador de manifiestos de kubernetes"
    )
    parser.add_argument(
        '--templates', '-t',
        nargs='+',
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
    parser.add_argument(
        '--deploy', '-d',
        action='store_true',
        help='Desplegar manifiestos despues de generarlos'
    )
    args = parser.parse_args()

    values = cargar_values(args.values)
    if not values:
        return 1
    if not validar_values(values):
        return 1
    for template_path in args.templates:
        contenido_template = cargar_template(template_path)
        if not contenido_template:
            return 1
        print(f"{'='*50}")
        manifiesto = generar_manifiesto(contenido_template, values)
        if not manifiesto:
            return 1
        print(f"\n{'*'*6} Manifiesto generado:")
        print(f"{os.path.basename(template_path)} {'*'*6}")
        print(manifiesto)

        # Validar manifiesto antes de mostrar o guardar
        nombre_template = os.path.basename(template_path)
        if not validar_manifiesto_k8s(manifiesto, nombre_template):
            print(
                "\nEl manifiesto generado NO es válido para Kubernetes. "
                "No se guardará el archivo."
            )
            return 1
        # Guardar en archivo solo si se especifica el output
        if args.output:
            nombre_base = os.path.basename(template_path)
            nombre_archivo = os.path.splitext(nombre_base)[0]
            ruta_output = os.path.join(args.output, nombre_archivo)
            guardar_manifiesto(manifiesto, ruta_output)
        print(f"{'='*50}")
    if args.deploy and args.output:
        print(f"\n{'='*50}")
        if desplegar_manifiestos(args.output):
            print("Generacion y despliegue completados")
        else:
            print("Fallo el despliegue")
            return 1
    elif args.deploy and not args.output:
        print("Error: Para desplegar necesitas especificar --output")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
