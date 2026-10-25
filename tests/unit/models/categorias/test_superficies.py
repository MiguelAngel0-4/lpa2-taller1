import pytest

from models.mueble import Mueble
from models.categorias.superficies import Superficie


class SuperficiePrueba(Superficie):
    """Implementación mínima para probar los métodos concretos de Superficie."""

    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_tamaño()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_superficie()


class TestSuperficie:
    @pytest.fixture
    def superficie(self):
        return SuperficiePrueba("Tablero", "Madera", "Café", 100.0, 100, 50, 75)

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Superficie("Tablero", "Madera", "Café", 100.0, 100, 50, 75)

    def test_hereda_de_mueble(self, superficie):
        assert isinstance(superficie, Mueble)

    def test_instanciacion_correcta(self, superficie):
        assert superficie.largo == 100
        assert superficie.ancho == 50
        assert superficie.altura == 75

    def test_calcular_area(self, superficie):
        assert superficie.calcular_area() == 5000

    @pytest.mark.parametrize(
        "largo,ancho,esperado",
        [
            (100, 50, 1.025),
            (100, 100, 1.05),
            (200, 100, 1.1),
        ],
    )
    def test_calcular_factor_tamaño(self, largo, ancho, esperado):
        superficie = SuperficiePrueba(
            "Tablero", "Madera", "Café", 100.0, largo, ancho, 75
        )
        assert superficie.calcular_factor_tamaño() == pytest.approx(esperado)

    def test_obtener_info_superficie(self, superficie):
        info = superficie.obtener_info_superficie()
        assert info == "Dimensiones: 100x50x75cm (Área: 5000cm²)"

    def test_setters_validos(self, superficie):
        superficie.largo = 150
        superficie.ancho = 60
        superficie.altura = 80
        assert superficie.calcular_area() == 9000
        assert superficie.altura == 80

    @pytest.mark.parametrize("atributo", ["largo", "ancho", "altura"])
    @pytest.mark.parametrize("valor", [0, -5])
    def test_setter_dimension_invalida(self, superficie, atributo, valor):
        with pytest.raises(ValueError, match="mayor a 0"):
            setattr(superficie, atributo, valor)
