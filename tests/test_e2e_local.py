import subprocess
import time
import requests
import pytest
import yaml
import os
from contextlib import contextmanager


@contextmanager
def port_forward_context(service_name, local_port=8080, service_port=80):
    """Context manager para port-forward temporal"""
    process = None
    try:
        # Iniciar port-forward
        process = subprocess.Popen([
            'kubectl', 'port-forward', f'service/{service_name}',
            f'{local_port}:{service_port}'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Dar tiempo para que se establezca
        time.sleep(3)
        yield f'http://localhost:{local_port}'
    finally:
        if process:
            process.terminate()
            process.wait()


class TestE2EManifestGenerator:
    """Pruebas End-to-End que simulan flujos completos de usuario"""

    def test_e2e_usuario_despliega_app_completa(self):
        """E2E: Ejecuta generador y obtiene aplicación funcionando"""
        # Ejecutar comando completo
        result = subprocess.run([
            'python', 'src/manifest_generator.py',
            '-t', 'templates/deployment.yaml.template',
            'templates/service.yaml.template',
            '-v', 'templates/values.yaml',
            '-o', 'test-output',
            '--deploy'
        ], capture_output=True, text=True)
        # Verificar que el comando fue exitoso
        assert result.returncode == 0
        # Esperar un tiempo razonable
        time.sleep(15)
        # Cargar configuración para saber qué verificar
        with open('templates/values.yaml', 'r') as f:
            values = yaml.safe_load(f)
        app_name = values['app_name']
        service_name = f"{app_name}-service"
        # Verificar que el pod está corriendo
        result = subprocess.run([
            'kubectl', 'get', 'pods', '-l', f'app={app_name}',
            '-o', 'jsonpath={.items[0].status.phase}'
        ], capture_output=True, text=True)
        assert result.returncode == 0
        assert 'Running' in result.stdout
        # Verificar que el service es accesible
        with port_forward_context(service_name) as url:
            try:
                response = requests.get(url, timeout=10)
                assert response.status_code == 200
            except requests.RequestException as e:
                pytest.fail(f"Service no accesible: {e}")

    def test_e2e_usuario_redespliega_app_actualizada(self):
        """E2E: Ejecuta generador, actualiza configuración y redespliega"""
        # Despliegue inicial
        subprocess.run([
            'python', 'src/manifest_generator.py',
            '-t', 'templates/deployment.yaml.template',
            'templates/service.yaml.template',
            '-v', 'templates/values.yaml',
            '-o', 'test-output',
            '--deploy'
        ], capture_output=True)
        # Esperar despliegue inicial
        time.sleep(10)
        # Modificar valores de configuración
        with open('templates/values.yaml', 'r') as f:
            values = yaml.safe_load(f)
        # Cambiar número de réplicas
        original_replicas = values['replicas']
        values['replicas'] = original_replicas + 1
        # Guardar configuración temporal
        with open('test-values-updated.yaml', 'w') as f:
            yaml.dump(values, f)
        # Redespliegue con nueva configuración
        result = subprocess.run([
            'python', 'src/manifest_generator.py',
            '-t', 'templates/deployment.yaml.template',
            'templates/service.yaml.template',
            '-v', 'test-values-updated.yaml',
            '-o', 'test-output',
            '--deploy'
        ], capture_output=True, text=True)
        assert result.returncode == 0
        # Esperar actualización
        time.sleep(15)
        app_name = values['app_name']
        result = subprocess.run([
            'kubectl', 'get', 'deployment', f'{app_name}-deployment',
            '-o', 'jsonpath={.spec.replicas}'
        ], capture_output=True, text=True)
        actual_replicas = int(result.stdout.strip())
        assert actual_replicas == values['replicas']
        # Verificar que la app sigue funcionando
        service_name = f"{app_name}-service"
        with port_forward_context(service_name) as url:
            response = requests.get(url, timeout=10)
            assert response.status_code == 200
        # Cleanup archivo temporal
        os.remove('test-values-updated.yaml')
