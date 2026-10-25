import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from models.concretos.sofa import Sofa


class TestSofa:
    def test_instanciacion_correcta(self, sofa_basico):
        assert sofa_basico.nombre == "Sofá Básico"
        assert sofa_basico.material == "Tela"
        assert sofa_basico.precio_base == 1000.0

    def test_valores_por_defecto(self, sofa_basico):
        assert sofa_basico.capacidad_personas == 3
        assert sofa_basico.tiene_respaldo is True
        assert sofa_basico.material_tapizado is None
        assert sofa_basico.tiene_brazos is True
        assert sofa_basico.es_modular is False
        assert sofa_basico.incluye_cojines is False

    def test_jerarquia_de_herencia(self, sofa_basico):
        assert isinstance(sofa_basico, Asiento)
        assert isinstance(sofa_basico, Mueble)

    def test_calcular_precio_basico(self, sofa_basico):
        # 1000 * 1.2 (respaldo + 3 personas) + 150 (brazos)
        assert sofa_basico.calcular_precio() == pytest.approx(1350.0)

    @pytest.mark.parametrize(
        "kwargs,esperado",
        [
            ({"tiene_brazos": False}, 1200.0),
            ({"material_tapizado": "cuero"}, 1550.0),
            ({"material_tapizado": "tela"}, 1450.0),
            ({"es_modular": True}, 1550.0),
            ({"incluye_cojines": True}, 1400.0),
            ({"capacidad_personas": 1, "tiene_brazos": False}, 1100.0),
            (
                {
                    "tiene_respaldo": False,
                    "capacidad_personas": 1,
                    "tiene_brazos": False,
                },
                1000.0,
            ),
        ],
    )
    def test_calcular_precio_segun_caracteristicas(self, kwargs, esperado):
        sofa = Sofa("Sofá", "Tela", "Gris", 1000.0, **kwargs)
        assert sofa.calcular_precio() == pytest.approx(esperado)

    def test_obtener_descripcion(self, sofa_basico):
        descripcion = sofa_basico.obtener_descripcion()
        assert "Sofá: Sofá Básico" in descripcion
        assert "Material: Tela" in descripcion
        assert "Color: Gris" in descripcion
        assert "Capacidad: 3 personas" in descripcion
        assert "Brazos: Sí" in descripcion
        assert "Modular: No" in descripcion
        assert "Incluye cojines: No" in descripcion
        assert "Precio final: $1350.0" in descripcion

    def test_obtener_descripcion_con_extras(self):
        sofa = Sofa(
            "Sofá",
            "Tela",
            "Gris",
            1000.0,
            tiene_brazos=False,
            es_modular=True,
            incluye_cojines=True,
        )
        descripcion = sofa.obtener_descripcion()
        assert "Brazos: No" in descripcion
        assert "Modular: Sí" in descripcion
        assert "Incluye cojines: Sí" in descripcion
