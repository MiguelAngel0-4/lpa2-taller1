"""
Ejemplo de TDD del README: nueva funcionalidad de descuentos por material.

Fase GREEN: aplicar_descuento_material ya está implementado en TiendaMuebles,
por eso las pruebas originales (antes xfail) ahora pasan.
"""

import pytest

from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from services.tienda import TiendaMuebles


@pytest.fixture
def tienda():
    return TiendaMuebles()


def test_aplicar_descuento_por_material(tienda):
    silla = Silla("Silla", "Roble", "Café", 100.0)

    tienda.agregar_mueble(silla)
    tienda.aplicar_descuento_material("Roble", 0.1)  # 10% descuento

    assert silla.precio_base == 90.0


def test_descuento_por_material_no_afecta_otros_materiales(tienda):
    silla_roble = Silla("Silla Roble", "Roble", "Café", 100.0)
    silla_metal = Silla("Silla Metal", "Metal", "Negro", 100.0)
    tienda.agregar_mueble(silla_roble)
    tienda.agregar_mueble(silla_metal)

    tienda.aplicar_descuento_material("roble", 0.2)

    assert silla_roble.precio_base == 80.0
    assert silla_metal.precio_base == 100.0


def test_descuento_afecta_distintos_tipos_del_mismo_material(tienda):
    silla = Silla("Silla", "Roble", "Café", 100.0)
    mesa = Mesa("Mesa", "Roble", "Café", 200.0)
    tienda.agregar_mueble(silla)
    tienda.agregar_mueble(mesa)

    tienda.aplicar_descuento_material("Roble", 0.5)

    assert silla.precio_base == 50.0
    assert mesa.precio_base == 100.0


def test_mensaje_indica_cantidad_de_muebles(tienda):
    tienda.agregar_mueble(Silla("Silla 1", "Roble", "Café", 100.0))
    tienda.agregar_mueble(Silla("Silla 2", "Roble", "Café", 100.0))

    mensaje = tienda.aplicar_descuento_material("Roble", 0.1)

    assert "10%" in mensaje
    assert "2 mueble(s)" in mensaje


def test_material_sin_coincidencias(tienda):
    silla = Silla("Silla", "Metal", "Negro", 100.0)
    tienda.agregar_mueble(silla)

    mensaje = tienda.aplicar_descuento_material("Roble", 0.1)

    assert "0 mueble(s)" in mensaje
    assert silla.precio_base == 100.0


def test_redondea_precio_a_dos_decimales(tienda):
    silla = Silla("Silla", "Roble", "Café", 99.99)
    tienda.agregar_mueble(silla)

    tienda.aplicar_descuento_material("Roble", 0.15)

    assert silla.precio_base == round(99.99 * 0.85, 2)


@pytest.mark.parametrize("porcentaje", [0, -0.1, 1, 1.5, 10])
def test_porcentaje_invalido_no_modifica_precios(tienda, porcentaje):
    silla = Silla("Silla", "Roble", "Café", 100.0)
    tienda.agregar_mueble(silla)

    mensaje = tienda.aplicar_descuento_material("Roble", porcentaje)

    assert mensaje.startswith("Error")
    assert silla.precio_base == 100.0
