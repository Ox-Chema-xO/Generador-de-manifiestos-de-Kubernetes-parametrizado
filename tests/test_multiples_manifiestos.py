import src.manifest_generator as manifest_generator


# Datos de prueba
values = {
    "app_name": "test-app",
    "protocol": "TCP",
    "image": "nginx:latest",
    "replicas": 2,
    "container_port": 80,
    "service_port": 8080
}

deployment_template = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ app_name }}-deployment
spec:
  replicas: {{ replicas }}
  selector:
    matchLabels:
      app: {{ app_name }}
  template:
    metadata:
      labels:
        app: {{ app_name }}
    spec:
      containers:
      - name: {{ app_name }}
        image: {{ image }}
        ports:
        - containerPort: {{ container_port }}
"""

service_template = """
apiVersion: v1
kind: Service
metadata:
  name: {{ app_name }}-service
spec:
  selector:
    app: {{ app_name }}
  ports:
  - protocol: {{ protocol }}
    port: {{ service_port }}
    targetPort: {{ container_port }}
"""


def test_generar_deployment_manifiesto():
    """
    Test que se genere correctamente un manifiesto de deployment
    """
    resultado = manifest_generator.generar_manifiesto(deployment_template, values)

    assert resultado is not None
    assert "test-app-deployment" in resultado
    assert "replicas: 2" in resultado
    assert "nginx:latest" in resultado
    assert "containerPort: 80" in resultado


def test_generar_service_manifiesto():
    """
    Test que se genere correctamente un manifiesto de service
    """
    resultado = manifest_generator.generar_manifiesto(service_template, values)

    assert resultado is not None
    assert "test-app-service" in resultado
    assert "TCP" in resultado
    assert "port: 8080" in resultado
    assert "targetPort: 80" in resultado


def test_generar_multiples_manifiestos_mismo_values():
    """
    Test generar multiples manifiestos con los mismos values
    """
    # Generar ambos manifiestos
    deployment = manifest_generator.generar_manifiesto(deployment_template, values)
    service = manifest_generator.generar_manifiesto(service_template, values)

    # Verificar que ambos se generaron
    assert deployment is not None
    assert "test-app-deployment" in deployment
    assert "replicas: 2" in deployment
    assert "nginx:latest" in deployment
    assert "containerPort: 80" in deployment

    assert service is not None
    assert "test-app-service" in service
    assert "TCP" in service
    assert "port: 8080" in service
    assert "targetPort: 80" in service


def test_validacion_values_true():
    """
    Test de la validacion de values funcione y devuelva true
    """
    # Values validos deben pasar
    assert manifest_generator.validar_values(values) is True


def test_validacion_values_false():
    """
    Test de la validacion de values funcione y devuelva false
    """
    # Values invalidos deben fallar
    values_malos = values.copy()
    values_malos['replicas'] = 'invalido'  # string en lugar de int
    assert manifest_generator.validar_values(values_malos) is False


def test_template_inexistente():
    """
    Test manejo de archivo template que no existe
    """
    resultado = manifest_generator.cargar_template('/archivo/que/no/existe.template')
    assert resultado is None


def test_values_inexistente():
    """
    Test manejo de archivo values que no existe
    """
    resultado = manifest_generator.cargar_values('/archivo/que/no/existe.yaml')
    assert resultado is None
