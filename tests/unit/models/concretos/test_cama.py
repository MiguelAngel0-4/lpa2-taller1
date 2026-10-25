import pytest

from models.mueble import Mueble
from models.concretos.cama import Cama


class TestCama:
    def test_instanciacion_correcta(self, cama_basica):
        assert cama_basica.nombre == "Cama Básica"
        assert cama_basica.material == "Madera"
        assert cama_basica.color == "Nogal"
        assert cama_basica.precio_base == 500.0

    def test_valores_por_defecto(self, cama_basica):
        assert cama_basica.tamaño == "individual"
        assert cama_basica.incluye_colchon is False
        assert cama_basica.tiene_cabecera is False

    def test_hereda_de_mueble(self, cama_basica):
        assert isinstance(cama_basica, Mueble)

    def test_calcular_precio_basico(self, cama_basica):
        assert cama_basica.calcular_precio() == 500.0

    @pytest.mark.parametrize(
        "tamaño,esperado",
        [
            ("individual", 500.0),
            ("matrimonial", 700.0),
            ("queen", 900.0),
            ("king", 1100.0),
            ("desconocido", 500.0),
        ],
    )
    def test_calcular_precio_por_tamaño(self, tamaño, esperado):
        cama = Cama("Cama", "Madera", "Nogal", 500.0, tamaño=tamaño)
        assert cama.calcular_precio() == esperado

    def test_calcular_precio_con_extras(self):
        cama = Cama(
            "Cama",
            "Madera",
            "Nogal",
            500.0,
            incluye_colchon=True,
            tiene_cabecera=True,
        )
        # 500 + 300 (colchón) + 100 (cabecera)
        assert cama.calcular_precio() == 900.0

    def test_calcular_precio_completa(self):
        cama = Cama("Cama", "Madera", "Nogal", 1000.0, "king", True, True)
        assert cama.calcular_precio() == 2000.0

    def test_obtener_descripcion(self, cama_basica):
        descripcion = cama_basica.obtener_descripcion()
        assert "Cama: Cama Básica" in descripcion
        assert "Material: Madera" in descripcion
        assert "Color: Nogal" in descripcion
        assert "Tamaño: individual" in descripcion
        assert "Incluye colchón: No" in descripcion
        assert "Cabecera: No" in descripcion
        assert "Precio final: $500.0" in descripcion

    def test_obtener_descripcion_con_extras(self):
        cama = Cama("Cama", "Madera", "Nogal", 500.0, "queen", True, True)
        descripcion = cama.obtener_descripcion()
        assert "Tamaño: queen" in descripcion
        assert "Incluye colchón: Sí" in descripcion
        assert "Cabecera: Sí" in descripcion

    @pytest.mark.parametrize("tamaño", ["individual", "matrimonial", "queen", "king"])
    def test_setter_tamaño_valido(self, cama_basica, tamaño):
        cama_basica.tamaño = tamaño
        assert cama_basica.tamaño == tamaño

    @pytest.mark.parametrize("tamaño", ["full", "King", ""])
    def test_setter_tamaño_invalido(self, cama_basica, tamaño):
        with pytest.raises(ValueError, match="Tamaño debe ser uno de"):
            cama_basica.tamaño = tamaño
