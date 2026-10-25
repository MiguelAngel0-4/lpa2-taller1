import pytest
from src.models.concretos.sofacama import SofaCama

class TestSofaCama:
    def test_herencia_multiple(self):
        sofa_cama = SofaCama("Sofá Cama Moderno", "Tela", 500.0, 3, "Queen")
        
        # Verificar atributos de Sofa
        assert sofa_cama.capacidad_personas == 3
        
        # Verificar atributos de Cama
        assert sofa_cama.tamaño_colchon == "Queen"
        
        # Verificar método específico
        assert hasattr(sofa_cama, 'transformar')
    
    def test_resolucion_metodos(self):
        sofa_cama = SofaCama("Sofá Cama", "Cuero", 600.0, 2, "Full")
        
        # Verificar que usa el método correcto (MRO)
        precio = sofa_cama.calcular_precio()
        assert precio > 600.0  # Debe incluir recargos de ambas clases