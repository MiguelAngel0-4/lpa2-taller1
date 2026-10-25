"""
Pruebas del punto de entrada src/main.py.
Se mockean print, input y el menú para que no haya interacción real.
"""

import pytest
from unittest.mock import Mock, patch

import main
from services.tienda import TiendaMuebles


def textos_impresos(mock_print):
    return [str(c.args[0]) for c in mock_print.call_args_list if c.args]


@pytest.fixture
def mock_print():
    with patch("builtins.print") as mock:
        yield mock


class TestDatosDeEjemplo:
    def test_crear_catalogo_inicial(self, tienda_vacia, mock_print):
        main.crear_catalogo_inicial(tienda_vacia)

        tipos = tienda_vacia.obtener_estadisticas()["tipos_muebles"]
        assert len(tienda_vacia._inventario) == 17
        assert tipos == {
            "Silla": 3,
            "Mesa": 3,
            "Sillon": 1,
            "Sofa": 2,
            "Armario": 1,
            "Cajonera": 2,
            "Cama": 2,
            "Escritorio": 2,
            "SofaCama": 1,
        }
        assert any("Catálogo inicial creado" in t for t in textos_impresos(mock_print))

    def test_crear_comedores_ejemplo(self, tienda_vacia, mock_print):
        main.crear_comedores_ejemplo(tienda_vacia)

        nombres = [comedor.nombre for comedor in tienda_vacia._comedores]
        assert nombres == ["Comedor Familiar Completo", "Comedor Moderno Premium"]
        assert [len(c.sillas) for c in tienda_vacia._comedores] == [6, 4]

    def test_aplicar_descuentos_ejemplo(self, tienda_vacia, mock_print):
        main.aplicar_descuentos_ejemplo(tienda_vacia)

        assert tienda_vacia._descuentos_activos == {
            "Silla": 0.1,
            "Mesa": 0.15,
            "Sofa": 0.2,
        }

    def test_mostrar_estadisticas_iniciales(self, mock_print):
        tienda = Mock(spec=TiendaMuebles)
        tienda.obtener_estadisticas.return_value = {
            "total_muebles": 5,
            "total_comedores": 1,
            "valor_inventario": 1234.5,
            "tipos_muebles": {"Silla": 2},
        }

        main.mostrar_estadisticas_iniciales(tienda)

        textos = textos_impresos(mock_print)
        assert any("Total de muebles: 5" in t for t in textos)
        assert any("Total de comedores: 1" in t for t in textos)
        assert any("$1,234.50" in t for t in textos)
        assert any("Ventas realizadas: 0" in t for t in textos)
        assert "    • Silla: 2 unidades" in textos


class TestMain:
    def test_main_inicia_el_menu(self, mock_print):
        with (
            patch("main.MenuTienda") as menu_cls,
            patch("builtins.input") as mock_input,
        ):
            main.main()

        tienda = menu_cls.call_args.args[0]
        assert isinstance(tienda, TiendaMuebles)
        assert tienda.nombre == "Mueblería Moderna OOP"
        assert len(tienda._inventario) == 17
        assert len(tienda._comedores) == 2
        mock_input.assert_called_once()
        menu_cls.return_value.ejecutar.assert_called_once()
        assert any("Programa finalizado" in t for t in textos_impresos(mock_print))

    def test_main_interrumpido_por_el_usuario(self, mock_print):
        with (
            patch("main.MenuTienda") as menu_cls,
            patch("builtins.input", side_effect=KeyboardInterrupt),
        ):
            main.main()

        menu_cls.return_value.ejecutar.assert_not_called()
        textos = textos_impresos(mock_print)
        assert any("Programa interrumpido por el usuario" in t for t in textos)
        assert any("Programa finalizado" in t for t in textos)

    def test_main_error_inesperado(self, mock_print):
        with (
            patch("main.MenuTienda", side_effect=RuntimeError("fallo")),
            patch("traceback.print_exc") as print_exc,
        ):
            main.main()

        print_exc.assert_called_once()
        textos = textos_impresos(mock_print)
        assert any("Error inesperado: fallo" in t for t in textos)
        assert any("Programa finalizado" in t for t in textos)
