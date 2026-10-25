import pytest

from models.concretos.cajonera import Cajonera


class TestCajonera:
    @pytest.fixture
    def cajonera(self):
        return Cajonera("Cajonera Test", "Madera", "Vintage", 300)

    def test_instanciacion_correcta(self, cajonera):
        assert cajonera.nombre == "Cajonera Test"
        assert cajonera.material == "Madera"
        assert cajonera.color == "Vintage"
        assert cajonera.precio_base == 300

    def test_valores_por_defecto(self, cajonera):
        assert cajonera.num_cajones == 3
        assert cajonera.tiene_ruedas is False

    @pytest.mark.parametrize(
        "precio_base,esperado",
        [
            (300, 300),
            (180.9, 180),
            (None, 0),
        ],
    )
    def test_precio_base_se_convierte_a_entero(self, precio_base, esperado):
        cajonera = Cajonera("Cajonera", "Madera", "Vintage", precio_base)
        assert cajonera.precio_base == esperado

    def test_calcular_precio_basico(self, cajonera):
        # 300 + 3 cajones * 20
        assert cajonera.calcular_precio() == 360

    @pytest.mark.parametrize(
        "cajones,ruedas,esperado",
        [
            (0, False, 300),
            (5, False, 400),
            (3, True, 390),
            (5, True, 430),
        ],
    )
    def test_calcular_precio_segun_caracteristicas(self, cajones, ruedas, esperado):
        cajonera = Cajonera("Cajonera", "Madera", "Vintage", 300, cajones, ruedas)
        assert cajonera.calcular_precio() == esperado

    def test_calcular_precio_retorna_entero(self, cajonera):
        assert isinstance(cajonera.calcular_precio(), int)

    def test_obtener_descripcion(self, cajonera):
        assert cajonera.obtener_descripcion() == (
            "Cajonera 'Cajonera Test': Material=Madera, Color=Vintage, "
            "Cajones=3, Ruedas=No, "
            "Precio base=$300"
        )

    def test_obtener_descripcion_con_ruedas(self):
        cajonera = Cajonera("Cajonera", "Metal", "Gris", 180, tiene_ruedas=True)
        assert "Ruedas=Sí" in cajonera.obtener_descripcion()
