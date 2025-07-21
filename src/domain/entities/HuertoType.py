from dataclasses import dataclass
from .PlantType import PlantType
from .ParcelaType import ParcelaType 
from typing import List

# Representa un individuo dentro de la población del algoritmo genético
@dataclass
class HuertoType:
    # Lista de plantas seleccionadas para el huerto
    plants: List[PlantType]
    # Información de la parcela asignada
    parcela: ParcelaType
    # Cantidad total de riego semanal (litros)
    totalIrrigation: int
    # Suma estimada de nutrientes aportados por las plantas
    totalNutritionalValue: int
    # Puntaje de compatibilidad entre especies plantadas
    compatibility: int
    # Tiempo estimado de mantenimiento (minutos por semana)
    careTime: int
    # Valor total calculado por la función de aptitud
    fitnessScore: int
