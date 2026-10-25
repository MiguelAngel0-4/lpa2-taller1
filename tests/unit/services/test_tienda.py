import pytest
from unittest.mock import Mock, patch
from src.services.tienda import Tienda
from src.models.concretos.silla import Silla

class TestTienda:
    @pytest.fixture
    def tienda_vacia(self):
        return Tienda()
    
    @pytest.fixture
    def silla_mock(self):
        mock_silla = Mock(spec=Silla)
        mock_silla.nombre = "Silla Mock"
        mock_silla.calcular_precio.return_value = 75.0
        return mock_silla
    
    def test_agregar_producto(self, tienda_vacia, silla_mock):
        tienda_vacia.agregar_producto(silla_mock)
        assert len(tienda_vacia.inventario) == 1
        assert tienda_vacia.inventario[0] == silla_mock
    
    def test_vender_producto_existente(self, tienda_vacia, silla_mock):
        tienda_vacia.agregar_producto(silla_mock)
        
        with patch('builtins.print') as mock_print:
            resultado = tienda_vacia.vender_producto("Silla Mock")
            
            assert resultado is True
            assert len(tienda_vacia.inventario) == 0
            mock_print.assert_called_once()
    
    def test_vender_producto_inexistente(self, tienda_vacia):
        resultado = tienda_vacia.vender_producto("Producto Inexistente")
        assert resultado is False