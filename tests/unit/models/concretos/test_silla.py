import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from models.concretos.silla import Silla


class TestSilla:
    # silla_basica y silla_oficina vienen de tests/unit/conftest.py

    def test_instanciacion_correcta(self, silla_basica):
        # Verificar herencia de atributos
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.color == "Café"
        assert silla_basica.precio_base == 50.0

        # Verificar atributos específicos
        assert silla_basica.tiene_respaldo is False
        assert silla_basica.material_tapizado is None
        assert silla_basica.altura_regulable is False
        assert silla_basica.tiene_ruedas is False

    def test_jerarquia_de_herencia(self, silla_basica):
        assert isinstance(silla_basica, Asiento)
        assert isinstance(silla_basica, Mueble)

    def test_capacidad_siempre_es_una_persona(self, silla_basica, silla_oficina):
        assert silla_basica.capacidad_personas == 1
        assert silla_oficina.capacidad_personas == 1

    def test_valores_por_defecto(self):
        silla = Silla("Silla", "Madera", "Café", 100.0)
        assert silla.tiene_respaldo is True
        assert silla.material_tapizado is None
        assert silla.altura_regulable is False
        assert silla.tiene_ruedas is False

    def test_calcular_precio(self, silla_basica):
        # Probar polimorfismo
        precio = silla_basica.calcular_precio()
        assert precio == 50.0  # Precio base sin modificaciones

    def test_calcular_precio_silla_oficina(self, silla_oficina):
        # 200 * 1.3 (respaldo + cuero) + 30 (altura) + 20 (ruedas)
        assert silla_oficina.calcular_precio() == 310.0

    @pytest.mark.parametrize(
        "kwargs,esperado",
        [
            ({"tiene_respaldo": False}, 100.0),
            ({}, 110.0),
            ({"material_tapizado": "tela"}, 120.0),
            ({"material_tapizado": "cuero"}, 130.0),
            ({"tiene_respaldo": False, "altura_regulable": True}, 130.0),
            ({"tiene_respaldo": False, "tiene_ruedas": True}, 120.0),
        ],
    )
    def test_calcular_precio_segun_caracteristicas(self, kwargs, esperado):
        silla = Silla("Silla", "Madera", "Café", 100.0, **kwargs)
        assert silla.calcular_precio() == pytest.approx(esperado)

    @pytest.mark.parametrize(
        "material,precio_base,esperado",
        [
            ("Madera", 100.0, 100.0),
            ("Roble", 150.0, 150.0),
            ("Metal", 120.0, 120.0),
        ],
    )
    def test_silla_precios_diferentes_materiales(self, material, precio_base, esperado):
        silla = Silla(
            f"Silla {material}", material, "Café", precio_base, tiene_respaldo=False
        )
        assert silla.calcular_precio() == esperado

    def test_obtener_descripcion(self, silla_basica):
        descripcion = silla_basica.obtener_descripcion()
        assert "Silla: Silla Básica" in descripcion
        assert "Material: Madera" in descripcion
        assert "Color: Café" in descripcion
        assert "Capacidad: 1 personas" in descripcion
        assert "Altura regulable: No" in descripcion
        assert "Ruedas: No" in descripcion
        assert "Precio final: $50.0" in descripcion

    def test_obtener_descripcion_silla_oficina(self, silla_oficina):
        descripcion = silla_oficina.obtener_descripcion()
        assert "Tapizado: cuero" in descripcion
        assert "Altura regulable: Sí" in descripcion
        assert "Ruedas: Sí" in descripcion

    def test_setters_altura_y_ruedas(self, silla_basica):
        silla_basica.altura_regulable = True
        silla_basica.tiene_ruedas = True
        assert silla_basica.altura_regulable is True
        assert silla_basica.tiene_ruedas is True

    def test_regular_altura_sin_mecanismo(self, silla_basica):
        resultado = silla_basica.regular_altura(60)
        assert resultado == "Esta silla no tiene altura regulable"

    @pytest.mark.parametrize("altura", [40, 75, 100])
    def test_regular_altura_valida(self, silla_oficina, altura):
        resultado = silla_oficina.regular_altura(altura)
        assert resultado == f"Altura ajustada a {altura} cm"

    @pytest.mark.parametrize("altura", [39, 101, 0])
    def test_regular_altura_fuera_de_rango(self, silla_oficina, altura):
        resultado = silla_oficina.regular_altura(altura)
        assert resultado == "La altura debe estar entre 40 y 100 cm"

    @pytest.mark.parametrize(
        "altura_regulable,tiene_ruedas,esperado",
        [
            (True, True, True),
            (True, False, False),
            (False, True, False),
            (False, False, False),
        ],
    )
    def test_es_silla_oficina(self, altura_regulable, tiene_ruedas, esperado):
        silla = Silla(
            "Silla",
            "Metal",
            "Negro",
            100.0,
            altura_regulable=altura_regulable,
            tiene_ruedas=tiene_ruedas,
        )
        assert silla.es_silla_oficina() is esperado
