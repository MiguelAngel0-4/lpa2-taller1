"""
Clase abstracta para muebles para superficies de trabajo o del hogar.
"""

from abc import ABC, abstractmethod

from models.mueble import Mueble


class Superficie(Mueble, ABC):
    """
    Clase abstracta para muebles tipo superficie (mesas, escritorios, etc).
    Hereda de Mueble y define la interfaz base para este tipo de muebles.

    Conceptos OOP aplicados:
    - Herencia: Extiende la clase Mueble
    - Abstracción: Define características comunes de superficies
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        largo: float,
        ancho: float,
        altura: float,
    ):
        """
        Constructor para muebles de superficie.

        Args:
            largo: Largo de la superficie en cm
            ancho: Ancho de la superficie en cm
            altura: Altura de la superficie en cm
        """
        super().__init__(nombre, material, color, precio_base)
        self._largo = largo
        self._ancho = ancho
        self._altura = altura

    @property
    def largo(self) -> float:
        """Getter para largo."""
        return self._largo

    @largo.setter
    def largo(self, value: float) -> None:
        """Setter para largo con validación."""
        if value <= 0:
            raise ValueError("El largo debe ser mayor a 0")
        self._largo = value

    @property
    def ancho(self) -> float:
        """Getter para ancho."""
        return self._ancho

    @ancho.setter
    def ancho(self, value: float) -> None:
        """Setter para ancho con validación."""
        if value <= 0:
            raise ValueError("El ancho debe ser mayor a 0")
        self._ancho = value

    @property
    def altura(self) -> float:
        """Getter para altura."""
        return self._altura

    @altura.setter
    def altura(self, value: float) -> None:
        """Setter para altura con validación."""
        if value <= 0:
            raise ValueError("La altura debe ser mayor a 0")
        self._altura = value

    def calcular_area(self) -> float:
        """
        Calcula el área de la superficie.

        Returns:
            float: Área en cm²
        """
        return self.largo * self.ancho

    def calcular_factor_tamaño(self) -> float:
        """
        Calcula un factor basado en el tamaño de la superficie.

        Returns:
            float: Factor multiplicador para el precio
        """
        area = self.calcular_area()
        # Factor basado en área (cada 10000 cm² = +5%)
        factor = 1.0 + (area / 10000) * 0.05
        return factor

    def obtener_info_superficie(self) -> str:
        """
        Obtiene información específica de la superficie.

        Returns:
            str: Información detallada de dimensiones
        """
        area = self.calcular_area()
        return (
            f"Dimensiones: {self.largo}x{self.ancho}x{self.altura}cm (Área: {area}cm²)"
        )

    @abstractmethod
    def calcular_precio(self) -> float:
        """Método abstracto para calcular precio."""
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Método abstracto para obtener descripción."""
        pass
