import pytest

from models.concretos.sillon import Sillon


class TestSillon:
    @pytest.fixture
    def sillon(self):
        return Sillon("Sillón Test", "Cuero", "Marrón", 500)

    def test_instanciacion_correcta(self, sillon):
        assert sillon.nombre == "Sillón Test"
        assert sillon.material == "Cuero"
        assert sillon.color == "Marrón"
        assert sillon.precio_base == 500

    def test_valores_por_defecto(self, sillon):
        assert sillon.capacidad_personas == 2
        assert sillon.tiene_respaldo is True
        assert sillon.material_tapizado is None
        assert sillon.tiene_brazos is True
        assert sillon.es_reclinable is False
        assert sillon.tiene_reposapiés is False

    @pytest.mark.parametrize(
        "precio_base,esperado",
        [
            (500, 500),
            (499.9, 499),
            ("300", 300),
            (None, 0),
        ],
    )
    def test_precio_base_se_convierte_a_entero(self, precio_base, esperado):
        sillon = Sillon("Sillón", "Cuero", "Marrón", precio_base)
        assert sillon.precio_base == esperado
        assert isinstance(sillon.precio_base, int)

    def test_calcular_precio_basico(self, sillon):
        # 500 + 100 (brazos por defecto)
        assert sillon.calcular_precio() == 600

    @pytest.mark.parametrize(
        "kwargs,esperado",
        [
            ({"tiene_brazos": False}, 500),
            ({"tiene_brazos": False, "material_tapizado": "cuero"}, 700),
            ({"tiene_brazos": False, "es_reclinable": True}, 750),
            ({"tiene_brazos": False, "tiene_reposapiés": True}, 580),
        ],
    )
    def test_calcular_precio_segun_extras(self, kwargs, esperado):
        sillon = Sillon("Sillón", "Cuero", "Marrón", 500, **kwargs)
        assert sillon.calcular_precio() == esperado

    def test_calcular_precio_completo(self):
        sillon = Sillon(
            "Sillón Lujo",
            "Cuero",
            "Marrón",
            500,
            material_tapizado="cuero",
            es_reclinable=True,
            tiene_reposapiés=True,
        )
        # 500 + 200 + 100 + 250 + 80
        assert sillon.calcular_precio() == 1130

    def test_calcular_precio_retorna_entero(self, sillon):
        assert isinstance(sillon.calcular_precio(), int)

    def test_obtener_descripcion(self, sillon):
        assert sillon.obtener_descripcion() == (
            "Sillón 'Sillón Test': Material=Cuero, Color=Marrón, "
            "Capacidad=2 personas, Tapizado=N/A, "
            "Brazos=Sí, Reclinable=No, "
            "Reposapiés=No, Precio base=$500"
        )

    def test_obtener_descripcion_con_extras(self):
        sillon = Sillon(
            "Sillón",
            "Cuero",
            "Marrón",
            500,
            material_tapizado="terciopelo",
            tiene_brazos=False,
            es_reclinable=True,
            tiene_reposapiés=True,
        )
        descripcion = sillon.obtener_descripcion()
        assert "Tapizado=terciopelo" in descripcion
        assert "Brazos=No" in descripcion
        assert "Reclinable=Sí" in descripcion
        assert "Reposapiés=Sí" in descripcion
