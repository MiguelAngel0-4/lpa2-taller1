import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from services.tienda import TiendaMuebles
from models.concretos.silla import Silla
from models.concretos.mesa import Mesa


@pytest.fixture
def crear_mueble_mock():
    def _crear(nombre="Silla Mock", precio=75.0, material="Madera"):
        mueble = Mock(spec=Silla)
        mueble.nombre = nombre
        mueble.material = material
        mueble.calcular_precio.return_value = precio
        return mueble

    return _crear


@pytest.fixture
def silla_mock(crear_mueble_mock):
    return crear_mueble_mock()


@pytest.fixture
def tienda_con_muebles(tienda_vacia, crear_mueble_mock):
    tienda_vacia.agregar_mueble(crear_mueble_mock("Silla Roble", 100.0, "Madera"))
    tienda_vacia.agregar_mueble(crear_mueble_mock("Silla Metálica", 150.0, "Metal"))
    tienda_vacia.agregar_mueble(crear_mueble_mock("Mesa Roble", 400.0, "Madera"))
    return tienda_vacia


class TestTiendaInicializacion:
    def test_nombre_personalizado(self, tienda_vacia):
        assert tienda_vacia.nombre == "Tienda Test"

    def test_nombre_por_defecto(self):
        assert TiendaMuebles().nombre == "Mueblería OOP"

    def test_inicia_vacia(self, tienda_vacia):
        assert tienda_vacia._inventario == []
        assert tienda_vacia._comedores == []
        assert tienda_vacia._ventas_realizadas == []
        assert tienda_vacia._descuentos_activos == {}


class TestAgregarMueble:
    def test_agregar_mueble(self, tienda_vacia, silla_mock):
        resultado = tienda_vacia.agregar_mueble(silla_mock)

        assert resultado == "Mueble Silla Mock agregado exitosamente al inventario"
        assert len(tienda_vacia._inventario) == 1
        assert tienda_vacia._inventario[0] == silla_mock
        silla_mock.calcular_precio.assert_called_once()

    def test_agregar_mueble_none(self, tienda_vacia):
        resultado = tienda_vacia.agregar_mueble(None)
        assert resultado == "Error: El mueble no puede ser None"
        assert tienda_vacia._inventario == []

    @pytest.mark.parametrize("precio", [0, -10.0])
    def test_agregar_mueble_precio_invalido(self, tienda_vacia, crear_mueble_mock, precio):
        resultado = tienda_vacia.agregar_mueble(crear_mueble_mock(precio=precio))
        assert resultado == "Error: El mueble debe tener un precio válido mayor a 0"
        assert tienda_vacia._inventario == []

    def test_agregar_mueble_error_al_calcular_precio(self, tienda_vacia, silla_mock):
        silla_mock.calcular_precio.side_effect = ValueError("precio roto")
        resultado = tienda_vacia.agregar_mueble(silla_mock)
        assert resultado == "Error al calcular precio del mueble: precio roto"
        assert tienda_vacia._inventario == []

    def test_agregar_mueble_real(self, tienda_vacia, silla_basica):
        resultado = tienda_vacia.agregar_mueble(silla_basica)
        assert "Silla Básica" in resultado
        assert silla_basica in tienda_vacia._inventario


class TestAgregarComedor:
    def test_agregar_comedor(self, tienda_vacia, comedor_completo):
        resultado = tienda_vacia.agregar_comedor(comedor_completo)
        assert resultado == "Comedor Comedor Familiar agregado exitosamente"
        assert tienda_vacia._comedores == [comedor_completo]

    def test_agregar_comedor_none(self, tienda_vacia):
        resultado = tienda_vacia.agregar_comedor(None)
        assert resultado == "Error: El comedor no puede ser None"
        assert tienda_vacia._comedores == []


class TestBusquedasYFiltros:
    @pytest.mark.parametrize(
        "termino,cantidad",
        [
            ("silla", 2),
            ("SILLA", 2),
            ("  roble  ", 2),
            ("Mesa", 1),
            ("sofá", 0),
        ],
    )
    def test_buscar_muebles_por_nombre(self, tienda_con_muebles, termino, cantidad):
        resultados = tienda_con_muebles.buscar_muebles_por_nombre(termino)
        assert len(resultados) == cantidad

    @pytest.mark.parametrize("termino", ["", "   ", None])
    def test_buscar_muebles_termino_vacio(self, tienda_con_muebles, termino):
        assert tienda_con_muebles.buscar_muebles_por_nombre(termino) == []

    @pytest.mark.parametrize(
        "minimo,maximo,nombres",
        [
            (0, float("inf"), {"Silla Roble", "Silla Metálica", "Mesa Roble"}),
            (100, 150, {"Silla Roble", "Silla Metálica"}),
            (101, 399, {"Silla Metálica"}),
            (500, 1000, set()),
            (-50, 100, {"Silla Roble"}),
        ],
    )
    def test_filtrar_por_precio(self, tienda_con_muebles, minimo, maximo, nombres):
        resultados = tienda_con_muebles.filtrar_por_precio(minimo, maximo)
        assert {mueble.nombre for mueble in resultados} == nombres

    def test_filtrar_por_precio_sin_argumentos(self, tienda_con_muebles):
        assert len(tienda_con_muebles.filtrar_por_precio()) == 3

    def test_filtrar_por_precio_ignora_muebles_con_error(
        self, tienda_con_muebles, crear_mueble_mock
    ):
        roto = crear_mueble_mock("Roto")
        tienda_con_muebles.agregar_mueble(roto)
        roto.calcular_precio.side_effect = Exception("error")

        resultados = tienda_con_muebles.filtrar_por_precio()

        assert roto not in resultados
        assert len(resultados) == 3

    @pytest.mark.parametrize(
        "material,cantidad",
        [
            ("madera", 2),
            ("MADERA", 2),
            ("  metal ", 1),
            ("vidrio", 0),
        ],
    )
    def test_filtrar_por_material(self, tienda_con_muebles, material, cantidad):
        assert len(tienda_con_muebles.filtrar_por_material(material)) == cantidad

    @pytest.mark.parametrize("material", ["", "  ", None])
    def test_filtrar_por_material_vacio(self, tienda_con_muebles, material):
        assert tienda_con_muebles.filtrar_por_material(material) == []

    def test_filtrar_por_material_ignora_muebles_sin_material_valido(
        self, tienda_vacia, crear_mueble_mock
    ):
        sin_material = crear_mueble_mock("Sin material", material=None)
        material_invalido = crear_mueble_mock("Material raro", material=123)
        valido = crear_mueble_mock("Válido", material="Madera")
        for mueble in (sin_material, material_invalido, valido):
            tienda_vacia.agregar_mueble(mueble)

        assert tienda_vacia.filtrar_por_material("madera") == [valido]


class TestDescuentos:
    @pytest.mark.parametrize(
        "categoria,clave",
        [
            ("silla", "Silla"),
            ("sillas", "Silla"),
            ("  Mesas ", "Mesa"),
            ("SOFA", "Sofa"),
            ("armarios", "Armario"),
        ],
    )
    def test_aplicar_descuento_normaliza_categoria(self, tienda_vacia, categoria, clave):
        resultado = tienda_vacia.aplicar_descuento(categoria, 10)
        assert resultado == f"Descuento del 10% aplicado a la categoría '{clave}'"
        assert tienda_vacia._descuentos_activos == {clave: 0.1}

    @pytest.mark.parametrize("porcentaje", [1, 50, 100])
    def test_aplicar_descuento_limites_validos(self, tienda_vacia, porcentaje):
        tienda_vacia.aplicar_descuento("silla", porcentaje)
        assert tienda_vacia._descuentos_activos["Silla"] == pytest.approx(
            porcentaje / 100
        )

    @pytest.mark.parametrize("porcentaje", [0, -5, 101])
    def test_aplicar_descuento_porcentaje_invalido(self, tienda_vacia, porcentaje):
        resultado = tienda_vacia.aplicar_descuento("silla", porcentaje)
        assert resultado == "Error: El porcentaje debe estar entre 1 y 100"
        assert tienda_vacia._descuentos_activos == {}


class TestRealizarVenta:
    def test_vender_producto_existente(self, tienda_vacia, silla_basica):
        tienda_vacia.agregar_mueble(silla_basica)

        venta = tienda_vacia.realizar_venta(silla_basica, "Ana")

        assert venta["mueble"] == "Silla Básica"
        assert venta["cliente"] == "Ana"
        assert venta["precio_original"] == 50.0
        assert venta["descuento"] == 0
        assert venta["precio_final"] == 50.0
        assert silla_basica not in tienda_vacia._inventario

    def test_vender_producto_inexistente(self, tienda_vacia, silla_basica):
        resultado = tienda_vacia.realizar_venta(silla_basica)
        assert resultado == {"error": "El mueble no está disponible en inventario"}

    def test_cliente_por_defecto(self, tienda_vacia, silla_basica):
        tienda_vacia.agregar_mueble(silla_basica)
        venta = tienda_vacia.realizar_venta(silla_basica)
        assert venta["cliente"] == "Cliente Anónimo"

    def test_fecha_con_formato_correcto(self, tienda_vacia, silla_basica):
        tienda_vacia.agregar_mueble(silla_basica)
        venta = tienda_vacia.realizar_venta(silla_basica)
        # Lanza ValueError si el formato no coincide
        datetime.strptime(venta["fecha"], "%Y-%m-%d %H:%M:%S")

    def test_venta_aplica_descuento_de_su_categoria(self, tienda_vacia, silla_basica):
        tienda_vacia.agregar_mueble(silla_basica)
        tienda_vacia.aplicar_descuento("sillas", 10)

        venta = tienda_vacia.realizar_venta(silla_basica)

        assert venta["descuento"] == pytest.approx(10.0)
        assert venta["precio_final"] == pytest.approx(45.0)

    def test_venta_ignora_descuento_de_otra_categoria(self, tienda_vacia, silla_basica):
        tienda_vacia.agregar_mueble(silla_basica)
        tienda_vacia.aplicar_descuento("mesas", 30)

        venta = tienda_vacia.realizar_venta(silla_basica)

        assert venta["descuento"] == 0
        assert venta["precio_final"] == 50.0

    def test_venta_actualiza_acumulados(self, tienda_vacia, crear_mueble_mock):
        muebles = [crear_mueble_mock(f"Mueble {i}", 100.0) for i in range(3)]
        for mueble in muebles:
            tienda_vacia.agregar_mueble(mueble)

        tienda_vacia.realizar_venta(muebles[0])
        tienda_vacia.realizar_venta(muebles[1])

        assert len(tienda_vacia._ventas_realizadas) == 2
        assert tienda_vacia._total_muebles_vendidos == 2
        assert tienda_vacia._valor_total_ventas == pytest.approx(200.0)
        assert tienda_vacia._inventario == [muebles[2]]

    def test_venta_mueble_sin_nombre_usa_tipo(self, tienda_vacia, crear_mueble_mock):
        mueble = crear_mueble_mock(nombre="")
        tienda_vacia.agregar_mueble(mueble)

        venta = tienda_vacia.realizar_venta(mueble)

        assert venta["mueble"] == type(mueble).__name__

    def test_venta_error_al_calcular_precio(self, tienda_vacia, silla_mock):
        # El primer cálculo (al agregar) funciona; el segundo (al vender) falla
        silla_mock.calcular_precio.side_effect = [75.0, Exception("sin precio")]
        tienda_vacia.agregar_mueble(silla_mock)

        resultado = tienda_vacia.realizar_venta(silla_mock)

        assert resultado == {"error": "Error al procesar la venta: sin precio"}
        assert silla_mock in tienda_vacia._inventario
        assert tienda_vacia._total_muebles_vendidos == 0


@pytest.mark.parametrize("metodo", ["obtener_estadisticas", "estadisticas"])
class TestEstadisticas:
    def test_estadisticas_tienda_vacia(self, tienda_vacia, metodo):
        stats = getattr(tienda_vacia, metodo)()
        assert stats == {
            "total_muebles": 0,
            "total_comedores": 0,
            "valor_inventario": 0,
            "tipos_muebles": {},
            "descuentos_activos": {},
            "ventas_realizadas": 0,
            "total_muebles_vendidos": 0,
            "valor_total_ventas": 0.0,
        }

    def test_estadisticas_con_datos(
        self, tienda_vacia, silla_basica, mesa_comedor, comedor_completo, metodo
    ):
        otra_silla = Silla("Otra", "Madera", "Café", 100.0, tiene_respaldo=False)
        for mueble in (silla_basica, otra_silla, mesa_comedor):
            tienda_vacia.agregar_mueble(mueble)
        tienda_vacia.agregar_comedor(comedor_completo)
        tienda_vacia.aplicar_descuento("mesa", 20)
        tienda_vacia.realizar_venta(otra_silla)

        stats = getattr(tienda_vacia, metodo)()

        assert stats["total_muebles"] == 2
        assert stats["total_comedores"] == 1
        assert stats["valor_inventario"] == pytest.approx(50.0 + 260.0)
        assert stats["tipos_muebles"] == {"Silla": 1, "Mesa": 1}
        assert stats["descuentos_activos"] == {"Mesa": 0.2}
        assert stats["ventas_realizadas"] == 1
        assert stats["total_muebles_vendidos"] == 1
        assert stats["valor_total_ventas"] == pytest.approx(100.0)

    def test_estadisticas_descuentos_es_una_copia(self, tienda_vacia, metodo):
        tienda_vacia.aplicar_descuento("silla", 10)
        stats = getattr(tienda_vacia, metodo)()
        stats["descuentos_activos"].clear()
        assert tienda_vacia._descuentos_activos == {"Silla": 0.1}

    def test_estadisticas_ignora_precios_con_error(
        self, tienda_vacia, crear_mueble_mock, metodo
    ):
        bueno = crear_mueble_mock("Bueno", 100.0)
        roto = crear_mueble_mock("Roto", 50.0)
        tienda_vacia.agregar_mueble(bueno)
        tienda_vacia.agregar_mueble(roto)
        roto.calcular_precio.side_effect = Exception("error")

        stats = getattr(tienda_vacia, metodo)()

        assert stats["total_muebles"] == 2
        assert stats["valor_inventario"] == 100.0

    def test_estadisticas_estado_corrupto_retorna_valores_por_defecto(
        self, tienda_vacia, metodo
    ):
        tienda_vacia._inventario = None  # len(None) lanza TypeError

        stats = getattr(tienda_vacia, metodo)()

        assert stats["total_muebles"] == 0
        assert stats["valor_inventario"] == 0.0
        assert stats["tipos_muebles"] == {}


class TestReporteInventario:
    def test_reporte_tienda_vacia(self, tienda_vacia):
        reporte = tienda_vacia.generar_reporte_inventario()
        assert "=== REPORTE DE INVENTARIO - Tienda Test ===" in reporte
        assert "Total de muebles: 0" in reporte
        assert "Total de comedores: 0" in reporte
        assert "Valor total del inventario: $0.00" in reporte
        assert "DISTRIBUCIÓN POR TIPOS:" in reporte
        assert "DESCUENTOS ACTIVOS" not in reporte

    def test_reporte_con_muebles_y_descuentos(self, tienda_vacia, silla_basica):
        tienda_vacia.agregar_mueble(silla_basica)
        tienda_vacia.aplicar_descuento("sillas", 15)

        reporte = tienda_vacia.generar_reporte_inventario()

        assert "Total de muebles: 1" in reporte
        assert "Valor total del inventario: $50.00" in reporte
        assert "- Silla: 1 unidades" in reporte
        assert "DESCUENTOS ACTIVOS:" in reporte
        assert "- Silla: 15.0%" in reporte

    @pytest.mark.parametrize("estadisticas_invalidas", [None, "no es un dict", []])
    def test_reporte_con_estadisticas_invalidas(
        self, tienda_vacia, estadisticas_invalidas
    ):
        with patch.object(
            tienda_vacia, "obtener_estadisticas", return_value=estadisticas_invalidas
        ):
            reporte = tienda_vacia.generar_reporte_inventario()

        assert "Total de muebles: 0" in reporte
        assert "Valor total del inventario: $0.00" in reporte


class TestTiendaPendientesTDD:
    """
    TDD - fase RED: estos métodos tienen un TODO en src/services/tienda.py
    y hoy retornan None. Cuando se implementen, las pruebas pasarán (XPASS)
    y, al ser strict=True, pytest avisará para quitar el marcador xfail.
    """

    @pytest.mark.xfail(reason="TDD: obtener_muebles_por_tipo sin implementar", strict=True)
    def test_obtener_muebles_por_tipo(self, tienda_vacia, silla_basica, mesa_comedor):
        tienda_vacia.agregar_mueble(silla_basica)
        tienda_vacia.agregar_mueble(mesa_comedor)

        assert tienda_vacia.obtener_muebles_por_tipo(Silla) == [silla_basica]
        assert tienda_vacia.obtener_muebles_por_tipo(Mesa) == [mesa_comedor]

    @pytest.mark.xfail(reason="TDD: calcular_valor_inventario sin implementar", strict=True)
    def test_calcular_valor_inventario(
        self, tienda_vacia, silla_basica, mesa_comedor, comedor_completo
    ):
        tienda_vacia.agregar_mueble(silla_basica)
        tienda_vacia.agregar_mueble(mesa_comedor)
        tienda_vacia.agregar_comedor(comedor_completo)

        # 50 (silla) + 260 (mesa) + 532 (comedor con descuento)
        assert tienda_vacia.calcular_valor_inventario() == pytest.approx(842.0)

    @pytest.mark.xfail(reason="TDD: _contar_tipos_muebles sin implementar", strict=True)
    def test_contar_tipos_muebles(self, tienda_vacia, silla_basica, mesa_comedor):
        tienda_vacia.agregar_mueble(silla_basica)
        tienda_vacia.agregar_mueble(Silla("Otra", "Metal", "Negro", 80.0))
        tienda_vacia.agregar_mueble(mesa_comedor)

        assert tienda_vacia._contar_tipos_muebles() == {"Silla": 2, "Mesa": 1}
