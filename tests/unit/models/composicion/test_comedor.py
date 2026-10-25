import pytest
from types import SimpleNamespace
from unittest.mock import Mock

from models.composicion.comedor import Comedor
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.concretos.sofa import Sofa


def crear_sillas(cantidad, **kwargs):
    return [
        Silla(f"Silla Comedor {i}", "Madera", "Roble", 50.0, tiene_respaldo=False, **kwargs)
        for i in range(1, cantidad + 1)
    ]


class TestComedor:
    # mesa_comedor, sillas_comedor y comedor_completo vienen de tests/unit/conftest.py
    # La mesa cuesta 260.0 (200 * 1.05 + 50 por 6 personas) y cada silla 50.0

    def test_composicion_correcta(self, comedor_completo):
        assert comedor_completo.nombre == "Comedor Familiar"
        assert comedor_completo.mesa is not None
        assert len(comedor_completo.sillas) == 6
        assert isinstance(comedor_completo.mesa, Mesa)
        assert all(isinstance(silla, Silla) for silla in comedor_completo.sillas)

    def test_instanciacion_sin_sillas(self, mesa_comedor):
        comedor = Comedor("Comedor Vacío", mesa_comedor)
        assert comedor.sillas == []

    def test_sillas_retorna_una_copia(self, comedor_completo):
        sillas = comedor_completo.sillas
        sillas.clear()
        assert len(comedor_completo.sillas) == 6

    def test_componentes_existen_independientemente(self, mesa_comedor):
        comedor = Comedor("Comedor", mesa_comedor, crear_sillas(2))
        del comedor
        # La mesa sigue existiendo aunque el comedor se elimine (agregación)
        assert mesa_comedor.nombre == "Mesa Comedor"

    def test_calcular_precio_total(self, comedor_completo):
        # 6 sillas => 5% de descuento por set completo
        precio_total = comedor_completo.calcular_precio_total()
        precio_esperado = (260.0 + (6 * 50.0)) * 0.95
        assert precio_total == pytest.approx(precio_esperado)

    def test_calcular_precio_total_coincide_con_componentes(self, comedor_completo):
        suma = comedor_completo.mesa.calcular_precio() + sum(
            silla.calcular_precio() for silla in comedor_completo.sillas
        )
        assert comedor_completo.calcular_precio_total() == round(suma * 0.95, 2)

    @pytest.mark.parametrize(
        "cantidad,esperado",
        [
            (0, 260.0),
            (3, 410.0),
            (4, 437.0),
            (5, 484.5),
        ],
    )
    def test_descuento_a_partir_de_cuatro_sillas(self, mesa_comedor, cantidad, esperado):
        comedor = Comedor("Comedor", mesa_comedor, crear_sillas(cantidad))
        assert comedor.calcular_precio_total() == pytest.approx(esperado)

    def test_calcular_precio_total_con_mocks(self):
        mesa = Mock()
        mesa.calcular_precio.return_value = 100.0
        sillas = [Mock() for _ in range(2)]
        for silla in sillas:
            silla.calcular_precio.return_value = 25.0

        comedor = Comedor("Comedor Mock", mesa, sillas)

        assert comedor.calcular_precio_total() == 150.0
        mesa.calcular_precio.assert_called_once()
        for silla in sillas:
            silla.calcular_precio.assert_called_once()

    def test_agregar_silla(self, mesa_comedor):
        comedor = Comedor("Comedor", mesa_comedor, crear_sillas(2))
        nueva = Silla("Silla Nueva", "Madera", "Roble", 50.0)

        resultado = comedor.agregar_silla(nueva)

        assert resultado == "Silla Silla Nueva agregada exitosamente al comedor"
        assert len(comedor.sillas) == 3

    def test_agregar_silla_a_comedor_vacio(self, mesa_comedor):
        comedor = Comedor("Comedor", mesa_comedor)
        resultado = comedor.agregar_silla(Silla("Primera", "Madera", "Roble", 50.0))
        assert "agregada exitosamente" in resultado
        assert len(comedor.sillas) == 1

    def test_agregar_objeto_que_no_es_silla(self, mesa_comedor):
        comedor = Comedor("Comedor", mesa_comedor, crear_sillas(2))
        sofa = Sofa("Sofá", "Tela", "Gris", 1000.0)

        resultado = comedor.agregar_silla(sofa)

        assert resultado == "Error: Solo se pueden agregar objetos de tipo Silla"
        assert len(comedor.sillas) == 2

    def test_agregar_silla_supera_capacidad_mesa(self, comedor_completo):
        # La mesa del fixture tiene capacidad para 6 personas
        resultado = comedor_completo.agregar_silla(
            Silla("Silla Extra", "Madera", "Roble", 50.0)
        )
        assert resultado == "No se pueden agregar más sillas. Capacidad máxima: 6"
        assert len(comedor_completo.sillas) == 6

    def test_capacidad_por_defecto_si_mesa_no_la_define(self):
        mesa = SimpleNamespace(calcular_precio=lambda: 100.0)
        comedor = Comedor("Comedor", mesa, crear_sillas(6))

        resultado = comedor.agregar_silla(Silla("Silla 7", "Madera", "Roble", 50.0))

        assert resultado == "No se pueden agregar más sillas. Capacidad máxima: 6"

    def test_quitar_ultima_silla(self, comedor_completo):
        resultado = comedor_completo.quitar_silla()
        assert resultado == "Silla Silla Comedor 6 removida del comedor"
        assert len(comedor_completo.sillas) == 5

    def test_quitar_silla_por_indice(self, comedor_completo):
        resultado = comedor_completo.quitar_silla(0)
        assert resultado == "Silla Silla Comedor 1 removida del comedor"
        assert len(comedor_completo.sillas) == 5

    def test_quitar_silla_indice_invalido(self, comedor_completo):
        resultado = comedor_completo.quitar_silla(10)
        assert resultado == "Índice de silla inválido"
        assert len(comedor_completo.sillas) == 6

    def test_quitar_silla_sin_sillas(self, mesa_comedor):
        comedor = Comedor("Comedor", mesa_comedor)
        assert comedor.quitar_silla() == "No hay sillas para quitar"

    def test_obtener_descripcion_completa(self, comedor_completo):
        descripcion = comedor_completo.obtener_descripcion_completa()
        assert "=== COMEDOR COMEDOR FAMILIAR ===" in descripcion
        assert "MESA:" in descripcion
        assert "Mesa: Mesa Comedor" in descripcion
        assert "SILLAS (6 unidades):" in descripcion
        assert "1. Silla: Silla Comedor 1" in descripcion
        assert "--- PRECIO TOTAL: $532.00 ---" in descripcion
        assert "(Incluye 5% de descuento por set completo)" in descripcion

    def test_obtener_descripcion_completa_sin_sillas(self, mesa_comedor):
        comedor = Comedor("Comedor", mesa_comedor)
        descripcion = comedor.obtener_descripcion_completa()
        assert "SILLAS: Ninguna incluida" in descripcion
        assert "descuento" not in descripcion

    def test_obtener_resumen(self, comedor_completo):
        resumen = comedor_completo.obtener_resumen()
        assert resumen["nombre"] == "Comedor Familiar"
        assert resumen["total_muebles"] == 7
        assert resumen["precio_mesa"] == pytest.approx(260.0)
        assert resumen["precio_sillas"] == pytest.approx(300.0)
        assert resumen["precio_total"] == pytest.approx(532.0)
        assert resumen["capacidad_personas"] == 6
        assert resumen["materiales_utilizados"] == ["Madera"]

    def test_materiales_incluyen_tapizado(self, mesa_comedor):
        sillas = [
            Silla("Silla", "Metal", "Negro", 50.0, material_tapizado="cuero"),
            Silla("Silla", "Metal", "Negro", 50.0),
        ]
        comedor = Comedor("Comedor", mesa_comedor, sillas)

        materiales = comedor.obtener_resumen()["materiales_utilizados"]

        assert sorted(materiales) == ["Madera", "Metal", "cuero"]

    def test_str(self, comedor_completo):
        assert str(comedor_completo) == "Comedor Comedor Familiar: Mesa + 6 sillas"

    def test_len(self, comedor_completo, mesa_comedor):
        assert len(comedor_completo) == 7
        assert len(Comedor("Vacío", mesa_comedor)) == 1
