import pytest
import os
from unittest import mock
from src.manifest_generator import validar_manifiesto_k8s

def test_validar_manifiesto_k8s_valido():
    manifiesto = "apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod\nspec:\n  containers:\n  - name: test\n    image: nginx\n"
    mock_result = mock.Mock()
    mock_result.returncode = 0
    with mock.patch('subprocess.run', return_value=mock_result):
        assert validar_manifiesto_k8s(manifiesto, "test-pod.yaml") is True

def test_validar_manifiesto_k8s_invalido():
    manifiesto = "apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod\nspec:\n  containers: []\n"
    mock_result = mock.Mock()
    mock_result.returncode = 1
    mock_result.stderr = "error: invalid manifest"
    with mock.patch('subprocess.run', return_value=mock_result):
        assert validar_manifiesto_k8s(manifiesto, "test-pod.yaml") is False

def test_validar_manifiesto_k8s_kubectl_no_encontrado():
    manifiesto = "apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod\nspec:\n  containers:\n  - name: test\n    image: nginx\n"
    with mock.patch('subprocess.run', side_effect=FileNotFoundError):
        assert validar_manifiesto_k8s(manifiesto, "test-pod.yaml") is False

def test_validar_manifiesto_k8s_exception():
    manifiesto = "apiVersion: v1\nkind: Pod\nmetadata:\n  name: test-pod\nspec:\n  containers:\n  - name: test\n    image: nginx\n"
    with mock.patch('subprocess.run', side_effect=Exception("otro error")):
        assert validar_manifiesto_k8s(manifiesto, "test-pod.yaml") is False
