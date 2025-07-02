import argparse
import subprocess


def mostrar_historial_deployment(app_name):
    """
    Muestra el historial de revisiones de un deployment
    """
    try:
        deployment_name = f"{app_name}-deployment"
        print(f"\nHistorial de {deployment_name}:")
        resultado = subprocess.run([
            'kubectl', 'rollout', 'history',
            f'deployment/{deployment_name}'
        ], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(resultado.stdout)
            return True
        else:
            print("Error al intentar obtener historial:")
            print(resultado.stderr)
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def rollback_deployment(app_name, revision=None):
    """
    Realiza rollback de un deployment a la version anterior o especifica
    """
    try:
        deployment_name = f"{app_name}-deployment"
        if revision:
            print(f""" Haciendo rollback de {deployment_name}
            a revision {revision} """)
            cmd = ['kubectl', 'rollout', 'undo',
                   f'deployment/{deployment_name}',
                   f'--to-revision={revision}']
        else:
            print(f""" \nHaciendo rollback de {deployment_name}
                  a version anterior""")
            cmd = ['kubectl', 'rollout', 'undo',
                   f'deployment/{deployment_name}']
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print("Rollback iniciado correctamente")
            print(resultado.stdout)
            print("\nVerificando estado del rollback")
            status_result = subprocess.run([
                'kubectl', 'rollout', 'status',
                f'deployment/{deployment_name}'
            ], capture_output=True, text=True)
            if status_result.returncode == 0:
                print("Rollback completado exitosamente")
                subprocess.run([
                    'kubectl', 'get', 'pods', '-l',
                    f'app={app_name}'
                ])
                return True
            else:
                print("Rollback completado pero con advertencias")
                return False
        else:
            print("Error en rollback:")
            print(resultado.stderr)
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Historial de revisiones y rollback"
    )
    parser.add_argument(
        '--history',
        metavar='APP_NAME',
        help='Mostrar historial de deployment'
    )
    parser.add_argument(
        '--rollback',
        metavar='APP_NAME',
        help='Hacer rollback del deployment especificado'
    )
    parser.add_argument(
        '--rollback-revision',
        metavar='REVISION',
        type=int,
        help='Revision especifica para rollback'
    )
    args = parser.parse_args()
    if args.rollback:
        if not rollback_deployment(args.rollback, args.rollback_revision):
            return 1
    if args.history:
        if not mostrar_historial_deployment(args.history):
            return 1
    return 0


if __name__ == "__main__":
    exit(main())
