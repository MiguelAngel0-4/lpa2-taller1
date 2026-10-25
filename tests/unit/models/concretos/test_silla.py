import pytest
from src.models.concretos.silla import Silla

class TestSilla:
    @pytest.fixture
    def silla_basica(self):
        return Silla("Silla Básica", "Madera", 50.0, 4, "Madera")
    
    def test_instanciacion_correcta(self, silla_basica):
        # Verificar herencia de atributos
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.precio_base == 50.0
        
        # Verificar atributos específicos
        assert silla_basica.numero_patas == 4
        assert silla_basica.tipo_madera == "Madera"
    
    def test_calcular_precio(self, silla_basica):
        # Probar polimorfismo
        precio = silla_basica.calcular_precio()
        assert precio == 50.0  # Precio base sin modificaciones
    
    def test_obtener_descripcion(self, silla_basica):
        descripcion = silla_basica.obtener_descripcion()
        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion