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
        """E2E: Usuario ejecuta generador y obtiene aplicación funcionando"""
        
        # Ejecutar comando completo
        result = subprocess.run([
            'python', 'src/manifest_generator.py',
            '-t', 'templates/deployment.yaml.template', 'templates/service.yaml.template',
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


