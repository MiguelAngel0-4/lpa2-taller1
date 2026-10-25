import pytest
from abc import ABC
from src.models.mueble import Mueble

class TestMueble:
    def test_es_clase_abstracta(self):
        # Verificar que Mueble es abstracta
        with pytest.raises(TypeError):
            mueble = Mueble("Mesa", "Madera", 100.0)
    
    def test_tiene_metodos_abstractos(self):
        # Verificar que tiene métodos abstractos
        assert hasattr(Mueble, 'calcular_precio')
        assert hasattr(Mueble, 'obtener_descripcion')
        
        # Verificar que son abstractos
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__