import pytest

from models.concretos.armario import Armario


class TestArmario:
    @pytest.fixture
    def armario(self):
        return Armario("Armario Test", "Madera", "Blanco", 600)

    def test_instanciacion_correcta(self, armario):
        assert armario.nombre == "Armario Test"
        assert armario.material == "Madera"
        assert armario.color == "Blanco"
        assert armario.precio_base == 600

    def test_valores_por_defecto(self, armario):
        assert armario.num_puertas == 2
        assert armario.num_cajones == 0
        assert armario.tiene_espejos is False

    @pytest.mark.parametrize(
        "precio_base,esperado",
        [
            (600, 600),
            (600.7, 600),
            (None, 0),
        ],
    )
    def test_precio_base_se_convierte_a_entero(self, precio_base, esperado):
        armario = Armario("Armario", "Madera", "Blanco", precio_base)
        assert armario.precio_base == esperado

    def test_calcular_precio_basico(self, armario):
        # 600 + 2 puertas * 50
        assert armario.calcular_precio() == 700

    @pytest.mark.parametrize(
        "puertas,cajones,espejos,esperado",
        [
            (0, 0, False, 600),
            (4, 0, False, 800),
            (2, 3, False, 790),
            (2, 0, True, 800),
            (4, 2, True, 960),
        ],
    )
    def test_calcular_precio_segun_caracteristicas(
        self, puertas, cajones, espejos, esperado
    ):
        armario = Armario("Armario", "Madera", "Blanco", 600, puertas, cajones, espejos)
        assert armario.calcular_precio() == esperado

    def test_calcular_precio_retorna_entero(self, armario):
        assert isinstance(armario.calcular_precio(), int)

    def test_obtener_descripcion(self, armario):
        assert armario.obtener_descripcion() == (
            "Armario 'Armario Test': Material=Madera, Color=Blanco, "
            "Puertas=2, Cajones=0, Espejos=No, "
            "Precio base=$600"
        )

    def test_obtener_descripcion_con_espejos(self):
        armario = Armario("Armario", "Madera", "Blanco", 600, tiene_espejos=True)
        assert "Espejos=Sí" in armario.obtener_descripcion()
