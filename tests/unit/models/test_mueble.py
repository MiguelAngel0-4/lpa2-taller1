import pytest
from abc import ABC

from models.mueble import Mueble


class MuebleConcreto(Mueble):
    """Implementación mínima para poder probar los métodos concretos de Mueble."""

    def calcular_precio(self) -> float:
        return self.precio_base

    def obtener_descripcion(self) -> str:
        return f"Mueble concreto {self.nombre}"


class TestMueble:
    @pytest.fixture
    def mueble(self):
        return MuebleConcreto("Mesa", "Madera", "Café", 100.0)

    def test_es_clase_abstracta(self):
        # Verificar que Mueble es abstracta
        assert issubclass(Mueble, ABC)
        with pytest.raises(TypeError):
            Mueble("Mesa", "Madera", "Café", 100.0)

    def test_tiene_metodos_abstractos(self):
        # Verificar que tiene métodos abstractos
        assert hasattr(Mueble, "calcular_precio")
        assert hasattr(Mueble, "obtener_descripcion")

        # Verificar que son abstractos
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__

    def test_subclase_incompleta_no_se_puede_instanciar(self):
        class MuebleIncompleto(Mueble):
            def calcular_precio(self) -> float:
                return 0.0

        with pytest.raises(TypeError):
            MuebleIncompleto("Mesa", "Madera", "Café", 100.0)

    def test_instanciacion_subclase_concreta(self, mueble):
        assert mueble.nombre == "Mesa"
        assert mueble.material == "Madera"
        assert mueble.color == "Café"
        assert mueble.precio_base == 100.0

    def test_metodos_implementados_en_subclase(self, mueble):
        assert mueble.calcular_precio() == 100.0
        assert mueble.obtener_descripcion() == "Mueble concreto Mesa"

    @pytest.mark.parametrize("atributo", ["nombre", "material", "color"])
    def test_setter_texto_elimina_espacios(self, mueble, atributo):
        setattr(mueble, atributo, "  Nuevo valor  ")
        assert getattr(mueble, atributo) == "Nuevo valor"

    @pytest.mark.parametrize("atributo", ["nombre", "material", "color"])
    @pytest.mark.parametrize("valor_invalido", ["", "   ", None])
    def test_setter_texto_vacio_lanza_error(self, mueble, atributo, valor_invalido):
        with pytest.raises(ValueError):
            setattr(mueble, atributo, valor_invalido)

    @pytest.mark.parametrize("precio", [0, 0.0, 150.5])
    def test_setter_precio_base_valido(self, mueble, precio):
        mueble.precio_base = precio
        assert mueble.precio_base == precio

    def test_setter_precio_base_negativo_lanza_error(self, mueble):
        with pytest.raises(ValueError, match="no puede ser negativo"):
            mueble.precio_base = -1

    def test_str(self, mueble):
        assert str(mueble) == "Mesa de Madera en color Café"

    def test_repr(self, mueble):
        assert repr(mueble) == (
            "Mueble(nombre='Mesa', material='Madera', color='Café', precio_base=100.0)"
        )
