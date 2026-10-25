import pytest

from models.mueble import Mueble
from models.categorias.superficies import Superficie
from models.concretos.mesa import Mesa


class TestMesa:
    @pytest.fixture
    def mesa_cuadrada(self):
        # 100x100 cm = 10000 cm² -> factor de tamaño 1.05
        return Mesa("Mesa Test", "Madera", "Roble", 200.0, largo=100, ancho=100)

    def test_instanciacion_correcta(self, mesa_comedor):
        assert mesa_comedor.nombre == "Mesa Comedor"
        assert mesa_comedor.material == "Madera"
        assert mesa_comedor.color == "Roble"
        assert mesa_comedor.precio_base == 200.0
        assert mesa_comedor.capacidad_personas == 6
        assert mesa_comedor.forma == "rectangular"

    def test_valores_por_defecto(self):
        mesa = Mesa("Mesa", "Madera", "Café", 100.0)
        assert mesa.forma == "rectangular"
        assert mesa.largo == 120.0
        assert mesa.ancho == 80.0
        assert mesa.altura == 75.0
        assert mesa.capacidad_personas == 4

    def test_jerarquia_de_herencia(self, mesa_comedor):
        assert isinstance(mesa_comedor, Superficie)
        assert isinstance(mesa_comedor, Mueble)

    def test_calcular_precio_basico(self, mesa_cuadrada):
        # 200 * 1.05, rectangular y 4 personas no suman recargos
        assert mesa_cuadrada.calcular_precio() == pytest.approx(210.0)

    @pytest.mark.parametrize("forma", ["redonda", "cuadrada", "ovalada"])
    def test_calcular_precio_forma_no_rectangular(self, forma):
        mesa = Mesa("Mesa", "Madera", "Roble", 200.0, forma=forma, largo=100, ancho=100)
        assert mesa.calcular_precio() == pytest.approx(260.0)

    @pytest.mark.parametrize(
        "capacidad,recargo",
        [
            (2, 0),
            (4, 0),
            (5, 50),
            (6, 50),
            (7, 100),
            (10, 100),
        ],
    )
    def test_calcular_precio_por_capacidad(self, capacidad, recargo):
        mesa = Mesa(
            "Mesa",
            "Madera",
            "Roble",
            200.0,
            largo=100,
            ancho=100,
            capacidad_personas=capacidad,
        )
        assert mesa.calcular_precio() == pytest.approx(210.0 + recargo)

    def test_obtener_descripcion(self, mesa_comedor):
        descripcion = mesa_comedor.obtener_descripcion()
        assert "Mesa: Mesa Comedor" in descripcion
        assert "Material: Madera" in descripcion
        assert "Color: Roble" in descripcion
        assert "Forma: rectangular" in descripcion
        assert "Dimensiones: 100.0x100.0x75.0cm" in descripcion
        assert "Capacidad: 6 personas" in descripcion
        assert f"Precio final: ${mesa_comedor.calcular_precio()}" in descripcion

    @pytest.mark.parametrize("forma", ["rectangular", "redonda", "cuadrada", "ovalada"])
    def test_setter_forma_valida(self, mesa_comedor, forma):
        mesa_comedor.forma = forma
        assert mesa_comedor.forma == forma

    @pytest.mark.parametrize("forma", ["triangular", "Redonda", ""])
    def test_setter_forma_invalida(self, mesa_comedor, forma):
        with pytest.raises(ValueError, match="Forma debe ser una de"):
            mesa_comedor.forma = forma

    def test_setter_capacidad_valida(self, mesa_comedor):
        mesa_comedor.capacidad_personas = 8
        assert mesa_comedor.capacidad_personas == 8

    @pytest.mark.parametrize("capacidad", [0, -3])
    def test_setter_capacidad_invalida(self, mesa_comedor, capacidad):
        with pytest.raises(ValueError, match="mayor a 0"):
            mesa_comedor.capacidad_personas = capacidad
