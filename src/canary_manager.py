#!/usr/bin/env python3
import argparse
import subprocess


def desplegar_canary(app_name, nueva_imagen):
    """
    Despliega version canary con nueva imagen
    """
    print(f"Desplegando canary: {nueva_imagen}")
    try:
        comandos = [
            (
                f"kubectl create deployment {app_name}-canary "
                f"--image={nueva_imagen}"
            ),
            (
                f"kubectl label deployment {app_name}-canary "
                f"app={app_name}-canary"
            ),
            (
                f"kubectl expose deployment {app_name}-canary --port=80 "
                f"--name={app_name}-canary-service"
            )
        ]
        for cmd in comandos:
            result = subprocess.run(
                cmd.split(), capture_output=True, text=True, check=False
            )
            if result.returncode != 0:
                print(f"Error: {result.stderr.strip()}")
                return False
        print("Canary desplegado")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def promover_canary(app_name, nueva_imagen):
    """
    Promueve canary a stable
    """
    print("Promoviendo canary a stable")
    try:
        result = subprocess.run(
            [
                "kubectl", "set", "image",
                f"deployment/{app_name}-deployment",
                f"{app_name}={nueva_imagen}"
            ],
            capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            return False
        subprocess.run(
            ["kubectl", "delete", "deployment", f"{app_name}-canary"],
            capture_output=True
        )
        subprocess.run(
            ["kubectl", "delete", "service", f"{app_name}-canary-service"],
            capture_output=True
        )
        print("Canary promovido")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def limpiar_canary(app_name):
    """
    Se limipia canary
    """
    print("Eliminando canary")
    try:
        subprocess.run(
            ["kubectl", "delete", "deployment", f"{app_name}-canary"],
            capture_output=True
        )
        subprocess.run(
            ["kubectl", "delete", "service", f"{app_name}-canary-service"],
            capture_output=True
        )
        print("Canary eliminado")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Gestor de canary releases"
    )
    parser.add_argument(
        '--app',
        metavar='APP_NAME',
        required=True,
        help='Nombre de la app'
    )
    parser.add_argument(
        '--deploy',
        metavar='IMAGEN',
        help='Desplegar canary release con la imagen proporcionada'
    )
    parser.add_argument(
        '--promote',
        metavar='IMAGEN',
        help='Promover el canary a produccion con la imagen especificada'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Eliminar el canary release de la app'
    )
    args = parser.parse_args()
    if args.deploy:
        if not desplegar_canary(args.app, args.deploy):
            return 1
        return 0
    if args.promote:
        if not promover_canary(args.app, args.promote):
            return 1
        return 0
    if args.clean:
        if not limpiar_canary(args.app):
            return 1
        return 0


if __name__ == "__main__":
    exit(main())
