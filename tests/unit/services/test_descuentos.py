"""
Ejemplo de TDD del README: nueva funcionalidad de descuentos por material.

Fase RED: TiendaMuebles todavía no tiene aplicar_descuento_material, por eso
las pruebas están marcadas como xfail. Al implementar el método (fase GREEN)
hay que quitar el marcador.
"""

import pytest

from services.tienda import TiendaMuebles
from models.concretos.silla import Silla


@pytest.fixture
def tienda():
    return TiendaMuebles()


@pytest.mark.xfail(reason="TDD: aplicar_descuento_material sin implementar", strict=True)
def test_aplicar_descuento_por_material(tienda):
    silla = Silla("Silla", "Roble", "Café", 100.0)

    tienda.agregar_mueble(silla)
    tienda.aplicar_descuento_material("Roble", 0.1)  # 10% descuento

    assert silla.precio_base == 90.0


@pytest.mark.xfail(reason="TDD: aplicar_descuento_material sin implementar", strict=True)
def test_descuento_por_material_no_afecta_otros_materiales(tienda):
    silla_roble = Silla("Silla Roble", "Roble", "Café", 100.0)
    silla_metal = Silla("Silla Metal", "Metal", "Negro", 100.0)
    tienda.agregar_mueble(silla_roble)
    tienda.agregar_mueble(silla_metal)

    tienda.aplicar_descuento_material("roble", 0.2)

    assert silla_roble.precio_base == 80.0
    assert silla_metal.precio_base == 100.0
