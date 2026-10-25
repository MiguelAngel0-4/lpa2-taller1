import pytest

from models.mueble import Mueble
from models.categorias.asientos import Asiento
from models.concretos.sofa import Sofa
from models.concretos.cama import Cama
from models.concretos.sofacama import SofaCama


class TestSofaCama:
    @pytest.fixture
    def sofa_cama(self):
        # Valores por defecto: 3 personas, tela, matrimonial, con colchón, plegable
        return SofaCama("Sofá Cama Moderno", "Tela", "Beige", 1000.0)

    def test_herencia_multiple(self, sofa_cama):
        assert isinstance(sofa_cama, Sofa)
        assert isinstance(sofa_cama, Cama)
        assert isinstance(sofa_cama, Asiento)
        assert isinstance(sofa_cama, Mueble)

        # Verificar atributos de Sofa
        assert sofa_cama.capacidad_personas == 3
        assert sofa_cama.material_tapizado == "tela"
        assert sofa_cama.tiene_brazos is True

        # Verificar atributos de Cama
        assert sofa_cama.tamaño == "matrimonial"
        assert sofa_cama.incluye_colchon is True

        # Verificar métodos específicos
        assert hasattr(sofa_cama, "convertir_a_cama")
        assert hasattr(sofa_cama, "convertir_a_sofa")

    def test_orden_resolucion_metodos(self):
        mro = SofaCama.__mro__
        assert mro[0] is SofaCama
        assert mro[1] is Sofa
        assert mro.index(Sofa) < mro.index(Cama)
        assert mro.index(Cama) < mro.index(Mueble)

    def test_constructor_cooperativo_inicializa_cama(self, sofa_cama):
        # Asiento llama a super().__init__, que en el MRO de SofaCama es Cama
        assert sofa_cama.tiene_cabecera is False

    def test_resolucion_metodos(self):
        sofa_cama = SofaCama("Sofá Cama", "Cuero", "Marrón", 600.0, 2)

        # Verificar que usa el método correcto (MRO)
        precio = sofa_cama.calcular_precio()
        assert precio > 600.0  # Debe incluir recargos de ambas clases

    def test_calcular_precio_sobrescribe_padres(self):
        assert SofaCama.calcular_precio is not Sofa.calcular_precio
        assert SofaCama.calcular_precio is not Cama.calcular_precio

    def test_calcular_precio_por_defecto(self, sofa_cama):
        # Sofá: 1000 * 1.3 + 150 (brazos) = 1450
        # Cama: + 300 (matrimonial) + 250 (colchón)
        assert sofa_cama.calcular_precio() == pytest.approx(2000.0)

    @pytest.mark.parametrize(
        "tamaño,esperado",
        [
            ("individual", 1700.0),
            ("matrimonial", 2000.0),
            ("queen", 2200.0),
            ("king", 2400.0),
        ],
    )
    def test_calcular_precio_por_tamaño(self, tamaño, esperado):
        sofa_cama = SofaCama("Sofá Cama", "Tela", "Beige", 1000.0, tamaño_cama=tamaño)
        assert sofa_cama.calcular_precio() == pytest.approx(esperado)

    @pytest.mark.parametrize(
        "mecanismo,esperado",
        [
            ("plegable", 2000.0),
            ("extensible", 2000.0),
            ("hidraulico", 2150.0),
            ("electrico", 2300.0),
        ],
    )
    def test_calcular_precio_por_mecanismo(self, mecanismo, esperado):
        sofa_cama = SofaCama(
            "Sofá Cama", "Tela", "Beige", 1000.0, mecanismo_conversion=mecanismo
        )
        assert sofa_cama.calcular_precio() == pytest.approx(esperado)

    def test_calcular_precio_sin_colchon(self):
        sofa_cama = SofaCama("Sofá Cama", "Tela", "Beige", 1000.0, incluye_colchon=False)
        assert sofa_cama.calcular_precio() == pytest.approx(1750.0)

    def test_propiedades_especificas(self, sofa_cama):
        assert sofa_cama.mecanismo_conversion == "plegable"
        assert sofa_cama.modo_actual == "sofa"
        assert sofa_cama.tamaño_cama == sofa_cama.tamaño == "matrimonial"

    def test_convertir_a_cama(self, sofa_cama):
        resultado = sofa_cama.convertir_a_cama()
        assert resultado == "Sofá convertido a cama usando mecanismo plegable"
        assert sofa_cama.modo_actual == "cama"

    def test_convertir_a_cama_dos_veces(self, sofa_cama):
        sofa_cama.convertir_a_cama()
        resultado = sofa_cama.convertir_a_cama()
        assert resultado == "El sofá-cama ya está en modo cama"
        assert sofa_cama.modo_actual == "cama"

    def test_convertir_a_sofa_estando_en_sofa(self, sofa_cama):
        resultado = sofa_cama.convertir_a_sofa()
        assert resultado == "El sofá-cama ya está en modo sofá"
        assert sofa_cama.modo_actual == "sofa"

    def test_convertir_a_sofa_desde_cama(self, sofa_cama):
        sofa_cama.convertir_a_cama()
        resultado = sofa_cama.convertir_a_sofa()
        assert resultado == "Cama convertida a sofá usando mecanismo plegable"
        assert sofa_cama.modo_actual == "sofa"

    @pytest.mark.parametrize(
        "tamaño,como_cama",
        [
            ("individual", 1),
            ("matrimonial", 2),
            ("queen", 2),
            ("king", 2),
        ],
    )
    def test_obtener_capacidad_total(self, tamaño, como_cama):
        sofa_cama = SofaCama("Sofá Cama", "Tela", "Beige", 1000.0, 3, tamaño_cama=tamaño)
        assert sofa_cama.obtener_capacidad_total() == {
            "como_sofa": 3,
            "como_cama": como_cama,
        }

    def test_obtener_descripcion(self, sofa_cama):
        descripcion = sofa_cama.obtener_descripcion()
        assert "Sofá-Cama: Sofá Cama Moderno" in descripcion
        assert "Material: Tela" in descripcion
        assert "Color: Beige" in descripcion
        assert "Capacidad: 3 personas, Respaldo: Sí, Tapizado: tela" in descripcion
        assert "Tamaño como cama: matrimonial" in descripcion
        assert "Incluye colchón: Sí" in descripcion
        assert "Mecanismo: plegable" in descripcion
        assert "Modo actual: sofa" in descripcion
        assert "Precio final: $2000.0" in descripcion

    def test_obtener_descripcion_refleja_modo(self, sofa_cama):
        sofa_cama.convertir_a_cama()
        assert "Modo actual: cama" in sofa_cama.obtener_descripcion()

    def test_str(self, sofa_cama):
        assert str(sofa_cama) == "Sofá-cama Sofá Cama Moderno (modo: sofa)"
        sofa_cama.convertir_a_cama()
        assert str(sofa_cama) == "Sofá-cama Sofá Cama Moderno (modo: cama)"
