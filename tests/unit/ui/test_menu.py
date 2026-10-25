"""
Pruebas del menú interactivo.
Se mockean la tienda, la consola de Rich y los prompts para no depender
de la entrada del usuario ni de la terminal.
"""

import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from rich.panel import Panel
from rich.table import Table

from ui.menu import MenuTienda
from services.tienda import TiendaMuebles
from models.concretos.silla import Silla


def textos_impresos(console):
    return [str(c.args[0]) for c in console.print.call_args_list if c.args]


def objetos_impresos(console, tipo):
    return [
        c.args[0]
        for c in console.print.call_args_list
        if c.args and isinstance(c.args[0], tipo)
    ]


@pytest.fixture(autouse=True)
def sin_esperas():
    with patch("ui.menu.time.sleep"):
        yield


@pytest.fixture(autouse=True)
def prompts():
    with (
        patch("ui.menu.Prompt") as prompt,
        patch("ui.menu.IntPrompt") as int_prompt,
        patch("ui.menu.Confirm") as confirm,
    ):
        yield SimpleNamespace(
            prompt=prompt.ask, int_prompt=int_prompt.ask, confirm=confirm.ask
        )


@pytest.fixture
def tienda_mock():
    tienda = Mock(spec=TiendaMuebles)
    tienda.nombre = "Tienda Test"
    tienda._inventario = []
    tienda._comedores = []
    return tienda


@pytest.fixture
def menu(tienda_mock):
    menu = MenuTienda(tienda_mock)
    menu.console = MagicMock()
    return menu


@pytest.fixture
def crear_mueble_mock():
    def _crear(nombre="Silla Mock", precio=100.0):
        mueble = Mock(spec=Silla)
        mueble.nombre = nombre
        mueble.material = "Madera"
        mueble.color = "Café"
        mueble.calcular_precio.return_value = precio
        mueble.obtener_descripcion.return_value = f"Descripción de {nombre}"
        return mueble

    return _crear


class TestInicializacion:
    def test_atributos(self, tienda_mock):
        menu = MenuTienda(tienda_mock)
        assert menu.tienda is tienda_mock
        assert menu.running is True
        assert menu.console is not None


class TestCatalogo:
    def test_catalogo_vacio(self, menu):
        menu.mostrar_catalogo_completo()
        assert "[yellow]No hay muebles en el inventario.[/yellow]" in textos_impresos(
            menu.console
        )

    def test_catalogo_con_muebles(self, menu, tienda_mock, crear_mueble_mock):
        tienda_mock._inventario = [crear_mueble_mock("A"), crear_mueble_mock("B")]

        menu.mostrar_catalogo_completo()

        tabla = objetos_impresos(menu.console, Table)[0]
        assert tabla.row_count == 2
        assert tabla.columns[1]._cells == ["A", "B"]
        assert tabla.columns[5]._cells == ["$100.00", "$100.00"]

    def test_catalogo_mueble_con_error_de_precio(
        self, menu, tienda_mock, crear_mueble_mock
    ):
        roto = crear_mueble_mock("Roto")
        roto.calcular_precio.side_effect = Exception("error")
        tienda_mock._inventario = [roto]

        menu.mostrar_catalogo_completo()

        tabla = objetos_impresos(menu.console, Table)[0]
        assert tabla.columns[2]._cells == ["Error"]
        assert tabla.columns[5]._cells == ["Error"]


class TestBuscarMuebles:
    def test_termino_vacio(self, menu, tienda_mock, prompts):
        prompts.prompt.return_value = "   "

        menu.buscar_muebles_interactivo()

        tienda_mock.buscar_muebles_por_nombre.assert_not_called()
        assert "[red]Término de búsqueda vacío.[/red]" in textos_impresos(menu.console)

    def test_sin_resultados(self, menu, tienda_mock, prompts):
        prompts.prompt.return_value = "sofá"
        tienda_mock.buscar_muebles_por_nombre.return_value = []

        menu.buscar_muebles_interactivo()

        tienda_mock.buscar_muebles_por_nombre.assert_called_once_with("sofá")
        assert any("No se encontraron" in t for t in textos_impresos(menu.console))

    def test_con_resultados(self, menu, tienda_mock, prompts, crear_mueble_mock):
        prompts.prompt.return_value = "silla"
        resultados = [crear_mueble_mock()]
        tienda_mock.buscar_muebles_por_nombre.return_value = resultados

        with patch.object(menu, "_mostrar_lista_muebles") as mostrar_lista:
            menu.buscar_muebles_interactivo()

        mostrar_lista.assert_called_once_with(resultados)


class TestFiltrarPorPrecio:
    def test_minimo_mayor_que_maximo(self, menu, tienda_mock, prompts):
        prompts.int_prompt.side_effect = [500, 100]

        menu.filtrar_por_precio_interactivo()

        tienda_mock.filtrar_por_precio.assert_not_called()
        assert any("no puede ser mayor" in t for t in textos_impresos(menu.console))

    def test_maximo_cero_significa_sin_limite(self, menu, tienda_mock, prompts):
        prompts.int_prompt.side_effect = [0, 0]
        tienda_mock.filtrar_por_precio.return_value = []

        menu.filtrar_por_precio_interactivo()

        tienda_mock.filtrar_por_precio.assert_called_once_with(0, float("inf"))
        assert any("No hay muebles en el rango" in t for t in textos_impresos(menu.console))

    def test_con_resultados(self, menu, tienda_mock, prompts, crear_mueble_mock):
        prompts.int_prompt.side_effect = [100, 500]
        resultados = [crear_mueble_mock()]
        tienda_mock.filtrar_por_precio.return_value = resultados

        with patch.object(menu, "_mostrar_lista_muebles") as mostrar_lista:
            menu.filtrar_por_precio_interactivo()

        tienda_mock.filtrar_por_precio.assert_called_once_with(100, 500)
        mostrar_lista.assert_called_once_with(resultados)


class TestFiltrarPorMaterial:
    def test_material_vacio(self, menu, tienda_mock, prompts):
        prompts.prompt.return_value = ""

        menu.filtrar_por_material_interactivo()

        tienda_mock.filtrar_por_material.assert_not_called()
        assert "[red]Material no puede estar vacío.[/red]" in textos_impresos(
            menu.console
        )

    def test_sin_resultados(self, menu, tienda_mock, prompts):
        prompts.prompt.return_value = "vidrio"
        tienda_mock.filtrar_por_material.return_value = []

        menu.filtrar_por_material_interactivo()

        assert "[yellow]No hay muebles de material 'vidrio'.[/yellow]" in (
            textos_impresos(menu.console)
        )

    def test_con_resultados(self, menu, tienda_mock, prompts, crear_mueble_mock):
        prompts.prompt.return_value = "madera"
        resultados = [crear_mueble_mock()]
        tienda_mock.filtrar_por_material.return_value = resultados

        with patch.object(menu, "_mostrar_lista_muebles") as mostrar_lista:
            menu.filtrar_por_material_interactivo()

        tienda_mock.filtrar_por_material.assert_called_once_with("madera")
        mostrar_lista.assert_called_once_with(resultados)


class TestMostrarComedores:
    def test_sin_comedores(self, menu):
        menu.mostrar_comedores()
        assert "[yellow]No hay comedores disponibles.[/yellow]" in textos_impresos(
            menu.console
        )

    def test_con_comedores(self, menu, tienda_mock):
        comedores = [Mock(), Mock()]
        for i, comedor in enumerate(comedores, 1):
            comedor.obtener_descripcion_completa.return_value = f"Comedor {i}"
        tienda_mock._comedores = comedores

        menu.mostrar_comedores()

        paneles = objetos_impresos(menu.console, Panel)
        assert [p.title for p in paneles] == ["Comedor #1", "Comedor #2"]
        assert [p.renderable for p in paneles] == ["Comedor 1", "Comedor 2"]


class TestRealizarVenta:
    @pytest.fixture
    def venta(self):
        return {
            "mueble": "Silla Mock",
            "cliente": "Ana",
            "precio_original": 100.0,
            "descuento": 10.0,
            "precio_final": 90.0,
            "fecha": "2026-01-01 10:00:00",
        }

    def test_sin_inventario(self, menu, tienda_mock):
        menu.realizar_venta_interactiva()
        tienda_mock.realizar_venta.assert_not_called()
        assert "[red]No hay muebles disponibles para venta.[/red]" in (
            textos_impresos(menu.console)
        )

    def test_venta_exitosa(
        self, menu, tienda_mock, prompts, crear_mueble_mock, venta
    ):
        mueble = crear_mueble_mock()
        tienda_mock._inventario = [mueble]
        tienda_mock.realizar_venta.return_value = venta
        prompts.int_prompt.return_value = 1
        prompts.confirm.return_value = True
        prompts.prompt.return_value = "Ana"

        with patch.object(menu, "_mostrar_comprobante_venta") as comprobante:
            menu.realizar_venta_interactiva()

        tienda_mock.realizar_venta.assert_called_once_with(mueble, "Ana")
        comprobante.assert_called_once_with(venta)
        assert "Descripción de Silla Mock" in textos_impresos(menu.console)

    def test_venta_cancelada(self, menu, tienda_mock, prompts, crear_mueble_mock):
        tienda_mock._inventario = [crear_mueble_mock()]
        prompts.int_prompt.return_value = 1
        prompts.confirm.return_value = False

        menu.realizar_venta_interactiva()

        tienda_mock.realizar_venta.assert_not_called()
        assert "[yellow]Venta cancelada.[/yellow]" in textos_impresos(menu.console)

    def test_venta_con_error(self, menu, tienda_mock, prompts, crear_mueble_mock):
        tienda_mock._inventario = [crear_mueble_mock()]
        tienda_mock.realizar_venta.return_value = {"error": "No disponible"}
        prompts.int_prompt.return_value = 1
        prompts.confirm.return_value = True
        prompts.prompt.return_value = "Ana"

        with patch.object(menu, "_mostrar_comprobante_venta") as comprobante:
            menu.realizar_venta_interactiva()

        comprobante.assert_not_called()
        assert "[red]Error: No disponible[/red]" in textos_impresos(menu.console)

    @pytest.mark.parametrize("respuesta", [ValueError(), 5])
    def test_seleccion_invalida(
        self, menu, tienda_mock, prompts, crear_mueble_mock, respuesta
    ):
        # ValueError del prompt o índice fuera de rango (IndexError)
        tienda_mock._inventario = [crear_mueble_mock()]
        prompts.int_prompt.side_effect = [respuesta]

        menu.realizar_venta_interactiva()

        tienda_mock.realizar_venta.assert_not_called()
        assert "[red]Selección inválida.[/red]" in textos_impresos(menu.console)


class TestEstadisticas:
    def test_mostrar_estadisticas(self, menu, tienda_mock):
        tienda_mock.obtener_estadisticas.return_value = {
            "total_muebles": 3,
            "total_comedores": 1,
            "valor_inventario": 450.0,
            "tipos_muebles": {"Silla": 2, "Mesa": 1},
            "descuentos_activos": {},
            "ventas_realizadas": 0,
            "total_muebles_vendidos": 0,
            "valor_total_ventas": 0.0,
        }

        menu.mostrar_estadisticas()

        tabla = objetos_impresos(menu.console, Table)[0]
        assert tabla.row_count == 7
        assert tabla.columns[1]._cells[0] == "3"
        assert tabla.columns[1]._cells[2] == "$450.00"
        textos = textos_impresos(menu.console)
        assert "  • Silla: 2 unidades" in textos
        assert "  • Mesa: 1 unidades" in textos

    def test_estadisticas_invalidas_usan_valores_por_defecto(self, menu, tienda_mock):
        tienda_mock.obtener_estadisticas.return_value = None

        menu.mostrar_estadisticas()

        tabla = objetos_impresos(menu.console, Table)[0]
        assert tabla.columns[1]._cells[0] == "0"
        assert not any("Distribución" in t for t in textos_impresos(menu.console))


class TestReporte:
    def test_reporte_sin_guardar(self, menu, tienda_mock, prompts):
        tienda_mock.generar_reporte_inventario.return_value = "REPORTE"
        prompts.confirm.return_value = False

        menu.generar_reporte_interactivo()

        panel = objetos_impresos(menu.console, Panel)[0]
        assert panel.renderable == "REPORTE"
        prompts.prompt.assert_not_called()

    def test_reporte_guardado_en_archivo(self, menu, tienda_mock, prompts, tmp_path):
        archivo = tmp_path / "reporte.txt"
        tienda_mock.generar_reporte_inventario.return_value = "REPORTE"
        prompts.confirm.return_value = True
        prompts.prompt.return_value = str(archivo)

        menu.generar_reporte_interactivo()

        assert archivo.read_text(encoding="utf-8") == "REPORTE"
        assert f"[green]Reporte guardado en {archivo}[/green]" in textos_impresos(
            menu.console
        )

    def test_reporte_error_al_guardar(self, menu, tienda_mock, prompts, tmp_path):
        tienda_mock.generar_reporte_inventario.return_value = "REPORTE"
        prompts.confirm.return_value = True
        prompts.prompt.return_value = str(tmp_path)  # Un directorio no se puede abrir

        menu.generar_reporte_interactivo()

        assert any(
            t.startswith("[red]Error al guardar:") for t in textos_impresos(menu.console)
        )


class TestAplicarDescuentos:
    @pytest.mark.parametrize(
        "indice,categoria",
        [
            (1, "silla"),
            (2, "mesa"),
            (6, "escritorio"),
        ],
    )
    def test_aplicar_descuento(self, menu, tienda_mock, prompts, indice, categoria):
        prompts.int_prompt.side_effect = [indice, 15]
        tienda_mock.aplicar_descuento.return_value = "Descuento aplicado"

        menu.aplicar_descuentos_interactivo()

        tienda_mock.aplicar_descuento.assert_called_once_with(categoria, 15)
        assert "[green]Descuento aplicado[/green]" in textos_impresos(menu.console)

    def test_seleccion_invalida(self, menu, tienda_mock, prompts):
        prompts.int_prompt.side_effect = ValueError()

        menu.aplicar_descuentos_interactivo()

        tienda_mock.aplicar_descuento.assert_not_called()
        assert "[red]Selección inválida.[/red]" in textos_impresos(menu.console)


class TestMetodosAuxiliares:
    def test_lista_muebles_sin_numerar(self, menu, crear_mueble_mock):
        menu._mostrar_lista_muebles([crear_mueble_mock("A")])

        tabla = objetos_impresos(menu.console, Table)[0]
        assert len(tabla.columns) == 4
        assert tabla.columns[0]._cells == ["A"]
        assert tabla.columns[3]._cells == ["$100.00"]

    def test_lista_muebles_numerada(self, menu, crear_mueble_mock):
        menu._mostrar_lista_muebles(
            [crear_mueble_mock("A"), crear_mueble_mock("B")], numerada=True
        )

        tabla = objetos_impresos(menu.console, Table)[0]
        assert len(tabla.columns) == 5
        assert tabla.columns[0]._cells == ["1", "2"]

    @pytest.mark.parametrize("numerada,columna_tipo", [(False, 1), (True, 2)])
    def test_lista_muebles_con_error_de_precio(
        self, menu, crear_mueble_mock, numerada, columna_tipo
    ):
        roto = crear_mueble_mock("Roto")
        roto.calcular_precio.side_effect = Exception("error")

        menu._mostrar_lista_muebles([roto], numerada=numerada)

        tabla = objetos_impresos(menu.console, Table)[0]
        assert tabla.columns[columna_tipo]._cells == ["Error"]

    def test_mostrar_comprobante_venta(self, menu):
        venta = {
            "mueble": "Silla Mock",
            "cliente": "Ana",
            "precio_original": 100.0,
            "descuento": 10.0,
            "precio_final": 90.0,
        }

        menu._mostrar_comprobante_venta(venta)

        panel = objetos_impresos(menu.console, Panel)[0]
        assert panel.title == "Venta Exitosa"
        assert "Cliente: Ana" in panel.renderable
        assert "Producto: Silla Mock" in panel.renderable
        assert "Precio original: $100.00" in panel.renderable
        assert "Descuento aplicado: 10.0%" in panel.renderable
        assert "PRECIO FINAL: $90.00" in panel.renderable

    def test_mostrar_banner(self, menu):
        menu.mostrar_banner()

        panel = objetos_impresos(menu.console, Panel)[0]
        assert panel.title == "Bienvenido"
        assert "Tienda Test" in panel.renderable.plain


class TestMenuPrincipal:
    def test_retorna_opcion_elegida(self, menu, prompts):
        prompts.int_prompt.return_value = 3
        assert menu.mostrar_menu_principal() == 3

    def test_reintenta_si_opcion_invalida(self, menu, prompts):
        prompts.int_prompt.side_effect = [ValueError(), 5]

        assert menu.mostrar_menu_principal() == 5
        assert "[red]Opción inválida. Intenta de nuevo.[/red]" in textos_impresos(
            menu.console
        )


class TestEjecutar:
    @pytest.mark.parametrize(
        "opcion,metodo",
        [
            (1, "mostrar_catalogo_completo"),
            (2, "buscar_muebles_interactivo"),
            (3, "filtrar_por_precio_interactivo"),
            (4, "filtrar_por_material_interactivo"),
            (5, "mostrar_comedores"),
            (6, "realizar_venta_interactiva"),
            (7, "mostrar_estadisticas"),
            (8, "generar_reporte_interactivo"),
            (9, "aplicar_descuentos_interactivo"),
        ],
    )
    def test_cada_opcion_llama_a_su_metodo(self, menu, opcion, metodo):
        with (
            patch.object(menu, "mostrar_banner"),
            patch.object(menu, "mostrar_menu_principal", side_effect=[opcion, 0]),
            patch.object(menu, metodo) as accion,
            patch("builtins.input") as mock_input,
        ):
            menu.ejecutar()

        accion.assert_called_once()
        mock_input.assert_called_once()
        assert menu.running is False

    def test_opcion_salir(self, menu):
        with (
            patch.object(menu, "mostrar_banner") as banner,
            patch.object(menu, "mostrar_menu_principal", return_value=0),
            patch("builtins.input") as mock_input,
        ):
            menu.ejecutar()

        banner.assert_called_once()
        mock_input.assert_not_called()
        assert menu.running is False
        assert "[red]¡Hasta luego! 👋[/red]" in textos_impresos(menu.console)

    def test_keyboard_interrupt_detiene_el_menu(self, menu):
        with (
            patch.object(menu, "mostrar_banner"),
            patch.object(
                menu, "mostrar_menu_principal", side_effect=KeyboardInterrupt
            ),
        ):
            menu.ejecutar()

        assert menu.running is False
        assert "\n[red]Operación cancelada por el usuario.[/red]" in textos_impresos(
            menu.console
        )

    def test_error_inesperado_continua_el_bucle(self, menu):
        with (
            patch.object(menu, "mostrar_banner"),
            patch.object(
                menu,
                "mostrar_menu_principal",
                side_effect=[RuntimeError("boom"), 0],
            ),
            patch("builtins.input") as mock_input,
        ):
            menu.ejecutar()

        assert "[red]Error inesperado: boom[/red]" in textos_impresos(menu.console)
        mock_input.assert_called_once_with("Presiona Enter para continuar...")
        assert menu.running is False
