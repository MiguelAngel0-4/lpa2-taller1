"""
Clase abstracta para muebles de almacenamiento.
"""

from abc import ABC, abstractmethod

from models.mueble import Mueble


class Almacenamiento(Mueble, ABC):
    """
    Clase abstracta para muebles de almacenamiento (como armarios, cajoneras, etc).
    Hereda de Mueble y define la interfaz base para este tipo de muebles.

    Conceptos OOP aplicados:
    - Herencia: Extiende la clase Mueble
    - Abstracción: Define características comunes de almacenamiento
    """

    def __init__(
        self,
        nombre: str,
        material: str,
        color: str,
        precio_base: float,
        num_compartimentos: int,
        capacidad_litros: float,
    ):
        """
        Constructor para muebles de almacenamiento.

        Args:
            num_compartimentos: Número de compartimentos/divisiones
            capacidad_litros: Capacidad en litros de almacenamiento
        """
        super().__init__(nombre, material, color, precio_base)
        self._num_compartimentos = num_compartimentos
        self._capacidad_litros = capacidad_litros

    @property
    def num_compartimentos(self) -> int:
        """Getter para número de compartimentos."""
        return self._num_compartimentos

    @num_compartimentos.setter
    def num_compartimentos(self, value: int) -> None:
        """Setter para compartimentos con validación."""
        if value <= 0:
            raise ValueError("El número de compartimentos debe ser mayor a 0")
        self._num_compartimentos = value

    @property
    def capacidad_litros(self) -> float:
        """Getter para capacidad en litros."""
        return self._capacidad_litros

    @capacidad_litros.setter
    def capacidad_litros(self, value: float) -> None:
        """Setter para capacidad con validación."""
        if value <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        self._capacidad_litros = value

    def calcular_factor_almacenamiento(self) -> float:
        """
        Calcula un factor basado en la capacidad de almacenamiento.

        Returns:
            float: Factor multiplicador para el precio
        """
        factor = 1.0
        # Más compartimentos = más funcionalidad
        factor += (self.num_compartimentos - 1) * 0.05
        # Mayor capacidad = mayor precio
        factor += (self.capacidad_litros / 100) * 0.02
        return factor

    def obtener_info_almacenamiento(self) -> str:
        """
        Obtiene información específica del almacenamiento.

        Returns:
            str: Información detallada del almacenamiento
        """
        return f"Compartimentos: {self.num_compartimentos}, Capacidad: {self.capacidad_litros}L"

    @abstractmethod
    def calcular_precio(self) -> float:
        """Método abstracto para calcular precio."""
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Método abstracto para obtener descripción."""
        pass
