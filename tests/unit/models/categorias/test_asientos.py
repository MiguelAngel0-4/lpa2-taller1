import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento


class AsientoPrueba(Asiento):
    """Implementación mínima para probar los métodos concretos de Asiento."""

    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_comodidad()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_asiento()


class TestAsiento:
    @pytest.fixture
    def asiento(self):
        return AsientoPrueba("Banco", "Madera", "Café", 100.0, 2, True, "tela")

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Asiento("Banco", "Madera", "Café", 100.0, 2, True)

    def test_hereda_de_mueble(self, asiento):
        assert isinstance(asiento, Mueble)
        assert isinstance(asiento, Asiento)

    def test_instanciacion_correcta(self, asiento):
        assert asiento.nombre == "Banco"
        assert asiento.capacidad_personas == 2
        assert asiento.tiene_respaldo is True
        assert asiento.material_tapizado == "tela"

    def test_material_tapizado_opcional(self):
        asiento = AsientoPrueba("Banco", "Madera", "Café", 100.0, 1, False)
        assert asiento.material_tapizado is None

    @pytest.mark.parametrize(
        "capacidad,respaldo,tapizado,esperado",
        [
            (1, False, None, 1.0),
            (1, True, None, 1.1),
            (1, False, "tela", 1.1),
            (1, False, "Tela", 1.1),
            (1, False, "cuero", 1.2),
            (1, False, "CUERO", 1.2),
            (1, False, "lino", 1.0),
            (3, False, None, 1.1),
            (3, True, "cuero", 1.4),
        ],
    )
    def test_calcular_factor_comodidad(self, capacidad, respaldo, tapizado, esperado):
        asiento = AsientoPrueba(
            "Banco", "Madera", "Café", 100.0, capacidad, respaldo, tapizado
        )
        assert asiento.calcular_factor_comodidad() == pytest.approx(esperado)

    def test_obtener_info_asiento_con_tapizado(self, asiento):
        info = asiento.obtener_info_asiento()
        assert info == "Capacidad: 2 personas, Respaldo: Sí, Tapizado: tela"

    def test_obtener_info_asiento_sin_tapizado(self):
        asiento = AsientoPrueba("Banco", "Madera", "Café", 100.0, 1, False)
        info = asiento.obtener_info_asiento()
        assert info == "Capacidad: 1 personas, Respaldo: No"
        assert "Tapizado" not in info

    def test_setter_capacidad_valida(self, asiento):
        asiento.capacidad_personas = 5
        assert asiento.capacidad_personas == 5

    @pytest.mark.parametrize("capacidad", [0, -1])
    def test_setter_capacidad_invalida(self, asiento, capacidad):
        with pytest.raises(ValueError, match="mayor a 0"):
            asiento.capacidad_personas = capacidad

    def test_setter_respaldo_y_tapizado(self, asiento):
        asiento.tiene_respaldo = False
        asiento.material_tapizado = "cuero"
        assert asiento.tiene_respaldo is False
        assert asiento.material_tapizado == "cuero"
