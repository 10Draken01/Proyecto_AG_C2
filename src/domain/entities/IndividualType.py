from dataclasses import dataclass
from .PlantType import PlantType  # Assuming PlantaType is defined in PlantaType.py
from typing import List

@dataclass
class IndividualType:
    # Lista de plantas seleccionadas
    plants: List[PlantType]
    # Matriz de distribución (ubicación espacial)
    layout: List[List[int]]
    # Litros por semana
    totalIrrigation: int
    # Suma estimada de nutrientes
    totalNutritionalValue: int
    # Puntaje de compatibilidad entre especies
    compatibility: int
    # Tiempo estimado de mantenimiento (min/semana)
    careTime: int
    # Valor total calculado por la función de aptitud
    fitnessScore: int
