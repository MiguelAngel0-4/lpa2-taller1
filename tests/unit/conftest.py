"""
Fixtures compartidas por todas las pruebas unitarias.
"""

import pytest

from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.sofa import Sofa
from models.concretos.cama import Cama
from models.composicion.comedor import Comedor
from services.tienda import TiendaMuebles
from tests.fixtures.datos_muebles import (
    SILLA_BASICA,
    SILLA_OFICINA,
    MESA_COMEDOR,
    SOFA_BASICO,
    CAMA_BASICA,
)


@pytest.fixture
def silla_basica():
    # Sin respaldo ni tapizado: el precio final es igual al precio base
    return Silla(**SILLA_BASICA, tiene_respaldo=False)


@pytest.fixture
def silla_oficina():
    return Silla(**SILLA_OFICINA)


@pytest.fixture
def mesa_comedor():
    return Mesa(**MESA_COMEDOR)


@pytest.fixture
def sofa_basico():
    return Sofa(**SOFA_BASICO)


@pytest.fixture
def cama_basica():
    return Cama(**CAMA_BASICA)


@pytest.fixture
def sillas_comedor():
    return [
        Silla(f"Silla Comedor {i}", "Madera", "Roble", 50.0, tiene_respaldo=False)
        for i in range(1, 7)
    ]


@pytest.fixture
def comedor_completo(mesa_comedor, sillas_comedor):
    return Comedor("Comedor Familiar", mesa_comedor, sillas_comedor)


@pytest.fixture
def tienda_vacia():
    return TiendaMuebles("Tienda Test")
