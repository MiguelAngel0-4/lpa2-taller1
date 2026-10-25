import pytest

from models.concretos.escritorio import Escritorio


class TestEscritorio:
    @pytest.fixture
    def escritorio(self):
        return Escritorio("Escritorio Test", "Madera", "Caoba", 500)

    def test_instanciacion_correcta(self, escritorio):
        assert escritorio.nombre == "Escritorio Test"
        assert escritorio.material == "Madera"
        assert escritorio.color == "Caoba"
        assert escritorio.precio_base == 500

    def test_valores_por_defecto(self, escritorio):
        assert escritorio.forma == "rectangular"
        assert escritorio.tiene_cajones is False
        assert escritorio.num_cajones == 0
        assert escritorio.largo == 1.2
        assert escritorio.tiene_iluminacion is False

    @pytest.mark.parametrize(
        "precio_base,esperado",
        [
            (500, 500),
            (750.5, 750),
            (None, 0),
        ],
    )
    def test_precio_base_se_convierte_a_entero(self, precio_base, esperado):
        escritorio = Escritorio("Escritorio", "Madera", "Caoba", precio_base)
        assert escritorio.precio_base == esperado

    def test_calcular_precio_basico(self, escritorio):
        assert escritorio.calcular_precio() == 500

    @pytest.mark.parametrize(
        "kwargs,esperado",
        [
            ({"tiene_cajones": True, "num_cajones": 4}, 600),
            ({"tiene_cajones": False, "num_cajones": 4}, 500),
            ({"largo": 1.5}, 500),
            ({"largo": 1.6}, 550),
            ({"tiene_iluminacion": True}, 540),
            ({"forma": "L"}, 530),
        ],
    )
    def test_calcular_precio_segun_caracteristicas(self, kwargs, esperado):
        escritorio = Escritorio("Escritorio", "Madera", "Caoba", 500, **kwargs)
        assert escritorio.calcular_precio() == esperado

    def test_calcular_precio_completo(self):
        escritorio = Escritorio(
            "Escritorio Ejecutivo L-Shape",
            "Madera",
            "Caoba",
            750,
            forma="L",
            tiene_cajones=True,
            num_cajones=4,
        )
        # 750 + 4 * 25 (cajones) + 30 (forma)
        assert escritorio.calcular_precio() == 880

    def test_calcular_precio_retorna_entero(self, escritorio):
        assert isinstance(escritorio.calcular_precio(), int)

    def test_obtener_descripcion(self, escritorio):
        assert escritorio.obtener_descripcion() == (
            "Escritorio 'Escritorio Test': Material=Madera, Color=Caoba, "
            "Forma=rectangular, Cajones=0, "
            "Largo=1.2m, Iluminación=No, "
            "Precio base=$500"
        )

    def test_obtener_descripcion_cajones_solo_si_tiene_cajones(self):
        sin_cajones = Escritorio("E", "Madera", "Caoba", 500, num_cajones=3)
        con_cajones = Escritorio(
            "E", "Madera", "Caoba", 500, tiene_cajones=True, num_cajones=3
        )
        assert "Cajones=0" in sin_cajones.obtener_descripcion()
        assert "Cajones=3" in con_cajones.obtener_descripcion()

    def test_obtener_descripcion_con_iluminacion(self):
        escritorio = Escritorio("E", "Metal", "Negro", 500, tiene_iluminacion=True)
        assert "Iluminación=Sí" in escritorio.obtener_descripcion()
