"""
Pruebas de integración: objetos reales de models/ trabajando con services/.
Sin mocks, para verificar que los módulos encajan entre sí.
"""

import pytest
from unittest.mock import patch

import main
from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.mesa import Mesa
from models.concretos.sofa import Sofa
from models.concretos.sofacama import SofaCama
from models.composicion.comedor import Comedor

pytestmark = pytest.mark.integration


@pytest.fixture
def tienda():
    return TiendaMuebles("Tienda Integración")


@pytest.fixture
def tienda_con_catalogo(tienda):
    with patch("builtins.print"):
        main.crear_catalogo_inicial(tienda)
        main.crear_comedores_ejemplo(tienda)
    return tienda


def test_flujo_completo_de_venta_con_descuento(tienda):
    silla = Silla("Silla Roble", "Roble", "Café", 100.0, tiene_respaldo=False)
    mesa = Mesa("Mesa Roble", "Roble", "Café", 200.0, largo=100, ancho=100)
    tienda.agregar_mueble(silla)
    tienda.agregar_mueble(mesa)
    tienda.aplicar_descuento("sillas", 10)

    venta = tienda.realizar_venta(silla, "Ana")

    assert venta["precio_original"] == 100.0
    assert venta["precio_final"] == pytest.approx(90.0)
    stats = tienda.obtener_estadisticas()
    assert stats["total_muebles"] == 1
    assert stats["ventas_realizadas"] == 1
    assert stats["valor_total_ventas"] == pytest.approx(90.0)
    assert stats["valor_inventario"] == pytest.approx(mesa.calcular_precio())


def test_vender_el_mismo_mueble_dos_veces(tienda):
    silla = Silla("Silla", "Madera", "Café", 100.0)
    tienda.agregar_mueble(silla)

    primera = tienda.realizar_venta(silla)
    segunda = tienda.realizar_venta(silla)

    assert "error" not in primera
    assert segunda == {"error": "El mueble no está disponible en inventario"}
    assert tienda._total_muebles_vendidos == 1


def test_comedor_en_tienda_y_reporte(tienda):
    mesa = Mesa("Mesa Comedor", "Madera", "Roble", 200.0, capacidad_personas=4)
    sillas = [Silla(f"Silla {i}", "Madera", "Roble", 50.0) for i in range(4)]
    comedor = Comedor("Comedor Integración", mesa, sillas)
    tienda.agregar_comedor(comedor)
    tienda.agregar_mueble(Sofa("Sofá", "Tela", "Gris", 1000.0))

    reporte = tienda.generar_reporte_inventario()

    assert "Total de comedores: 1" in reporte
    assert "Total de muebles: 1" in reporte
    assert "- Sofa: 1 unidades" in reporte
    assert "No se pueden agregar más sillas" in comedor.agregar_silla(
        Silla("Extra", "Madera", "Roble", 50.0)
    )


def test_polimorfismo_en_inventario(tienda):
    muebles = [
        Silla("Silla", "Madera", "Café", 100.0),
        Mesa("Mesa", "Madera", "Café", 200.0),
        Sofa("Sofá", "Tela", "Gris", 1000.0),
        SofaCama("Sofá Cama", "Tela", "Beige", 1000.0),
    ]
    for mueble in muebles:
        tienda.agregar_mueble(mueble)

    total = sum(m.calcular_precio() for m in muebles)

    assert tienda.obtener_estadisticas()["valor_inventario"] == pytest.approx(total)
    assert tienda.filtrar_por_precio(0, float("inf")) == muebles


@pytest.mark.slow
def test_catalogo_inicial_busquedas_y_filtros(tienda_con_catalogo):
    tienda = tienda_con_catalogo

    assert len(tienda.buscar_muebles_por_nombre("silla")) == 3
    assert len(tienda.filtrar_por_material("madera")) == 6
    assert len(tienda._comedores) == 2
    for mueble in tienda.filtrar_por_precio(500, 1000):
        assert 500 <= mueble.calcular_precio() <= 1000


@pytest.mark.slow
def test_catalogo_inicial_vender_todo(tienda_con_catalogo):
    tienda = tienda_con_catalogo
    valor_inventario = tienda.obtener_estadisticas()["valor_inventario"]

    for mueble in list(tienda._inventario):
        venta = tienda.realizar_venta(mueble)
        assert "error" not in venta

    stats = tienda.obtener_estadisticas()
    assert stats["total_muebles"] == 0
    assert stats["total_muebles_vendidos"] == 17
    assert stats["valor_total_ventas"] == pytest.approx(valor_inventario, abs=0.1)
