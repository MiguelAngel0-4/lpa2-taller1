import pytest

from models.mueble import Mueble
from models.categorias.almacenamiento import Almacenamiento


class AlmacenamientoPrueba(Almacenamiento):
    """Implementación mínima para probar los métodos concretos de Almacenamiento."""

    def calcular_precio(self) -> float:
        return self.precio_base * self.calcular_factor_almacenamiento()

    def obtener_descripcion(self) -> str:
        return self.obtener_info_almacenamiento()


class TestAlmacenamiento:
    @pytest.fixture
    def almacenamiento(self):
        return AlmacenamientoPrueba("Baúl", "Madera", "Café", 100.0, 3, 200)

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Almacenamiento("Baúl", "Madera", "Café", 100.0, 3, 200)

    def test_hereda_de_mueble(self, almacenamiento):
        assert isinstance(almacenamiento, Mueble)

    def test_instanciacion_correcta(self, almacenamiento):
        assert almacenamiento.num_compartimentos == 3
        assert almacenamiento.capacidad_litros == 200

    @pytest.mark.parametrize(
        "compartimentos,litros,esperado",
        [
            (1, 0, 1.0),
            (3, 0, 1.1),
            (1, 100, 1.02),
            (3, 200, 1.14),
        ],
    )
    def test_calcular_factor_almacenamiento(self, compartimentos, litros, esperado):
        mueble = AlmacenamientoPrueba(
            "Baúl", "Madera", "Café", 100.0, compartimentos, litros
        )
        assert mueble.calcular_factor_almacenamiento() == pytest.approx(esperado)

    def test_obtener_info_almacenamiento(self, almacenamiento):
        info = almacenamiento.obtener_info_almacenamiento()
        assert info == "Compartimentos: 3, Capacidad: 200L"

    def test_setters_validos(self, almacenamiento):
        almacenamiento.num_compartimentos = 5
        almacenamiento.capacidad_litros = 350.5
        assert almacenamiento.num_compartimentos == 5
        assert almacenamiento.capacidad_litros == 350.5

    @pytest.mark.parametrize("valor", [0, -2])
    def test_setter_compartimentos_invalido(self, almacenamiento, valor):
        with pytest.raises(ValueError, match="compartimentos"):
            almacenamiento.num_compartimentos = valor

    @pytest.mark.parametrize("valor", [0, -10.0])
    def test_setter_capacidad_invalida(self, almacenamiento, valor):
        with pytest.raises(ValueError, match="capacidad"):
            almacenamiento.capacidad_litros = valor
