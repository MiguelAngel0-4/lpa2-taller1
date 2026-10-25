"""
Pruebas del Comedor simple de models/concretos/comedor.py.
Se usan mocks para aislar al comedor de la lógica de Mesa y Silla.
"""

import pytest
from unittest.mock import Mock

from models.concretos.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla


@pytest.fixture
def mesa_mock():
    mesa = Mock(spec=Mesa)
    mesa.calcular_precio.return_value = 200.0
    mesa.obtener_descripcion.return_value = "Mesa Mock"
    return mesa


@pytest.fixture
def crear_silla_mock():
    def _crear(precio=50.0, descripcion="Silla Mock"):
        silla = Mock(spec=Silla)
        silla.calcular_precio.return_value = precio
        silla.obtener_descripcion.return_value = descripcion
        return silla

    return _crear


class TestComedorConcreto:
    def test_instanciacion_sin_sillas(self, mesa_mock):
        comedor = Comedor(mesa_mock)
        assert comedor.mesa is mesa_mock
        assert comedor.sillas == []
        assert comedor.cantidad_sillas() == 0

    def test_instanciacion_con_sillas(self, mesa_mock, crear_silla_mock):
        sillas = [crear_silla_mock() for _ in range(4)]
        comedor = Comedor(mesa_mock, sillas)
        assert comedor.cantidad_sillas() == 4

    def test_calcular_precio_total(self, mesa_mock, crear_silla_mock):
        sillas = [crear_silla_mock(50.0) for _ in range(6)]
        comedor = Comedor(mesa_mock, sillas)
        assert comedor.calcular_precio_total() == 200.0 + (6 * 50.0)

    def test_calcular_precio_total_sin_sillas(self, mesa_mock):
        comedor = Comedor(mesa_mock)
        assert comedor.calcular_precio_total() == 200.0
        mesa_mock.calcular_precio.assert_called_once()

    def test_agregar_silla(self, mesa_mock, crear_silla_mock):
        comedor = Comedor(mesa_mock)
        silla = crear_silla_mock()
        comedor.agregar_silla(silla)
        assert comedor.cantidad_sillas() == 1
        assert silla in comedor.sillas

    def test_quitar_silla_existente(self, mesa_mock, crear_silla_mock):
        silla = crear_silla_mock()
        comedor = Comedor(mesa_mock, [silla])
        comedor.quitar_silla(silla)
        assert comedor.cantidad_sillas() == 0

    def test_quitar_silla_inexistente_no_hace_nada(self, mesa_mock, crear_silla_mock):
        comedor = Comedor(mesa_mock, [crear_silla_mock()])
        comedor.quitar_silla(crear_silla_mock())
        assert comedor.cantidad_sillas() == 1

    def test_descripcion(self, mesa_mock, crear_silla_mock):
        sillas = [crear_silla_mock(descripcion=f"Silla {i}") for i in (1, 2)]
        comedor = Comedor(mesa_mock, sillas)
        descripcion = comedor.descripcion()
        assert "Comedor con mesa: Mesa Mock" in descripcion
        assert "y 2 sillas:" in descripcion
        assert "1. Silla 1" in descripcion
        assert "2. Silla 2" in descripcion
