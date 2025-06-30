from src.manifest_generator import validar_values


def test_validar_values_campo_faltante():
    values = {
        "app_name": "mi-app",
        "protocol": "TCP",
        "image": "nginx:latest",
        "container_port": 8080,
        "service_port": 80
    }
    assert validar_values(values) is False


def test_validar_values_puerto_fuera_rango():
    values = {
        "app_name": "mi-app",
        "protocol": "TCP",
        "image": "nginx:latest",
        "replicas": 2,
        "container_port": 898989,
        "service_port": 80
    }
    assert validar_values(values) is False


def test_validar_values_tipo_invalido():
    values = {
        "app_name": "mi-app",
        "protocol": "TCP",
        "image": "nginx:latest",
        "replicas": "tres",
        "container_port": 8080,
        "service_port": 80
    }
    assert validar_values(values) is False


def test_validar_values_imagen_invalida():
    values = {
        "app_name": "mi-app",
        "protocol": "TCP",
        "image": "nginx!@",
        "replicas": 1,
        "container_port": 8080,
        "service_port": 80
    }
    assert validar_values(values) is False


def test_validar_values_valido():
    values = {
        "app_name": "mi-app",
        "protocol": "TCP",
        "image": "nginx",
        "replicas": 3,
        "container_port": 8080,
        "service_port": 80
    }
    assert validar_values(values) is True
