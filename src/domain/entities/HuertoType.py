from dataclasses import dataclass
from ...domain.entities.ParcelaType import ParcelaType 
from typing import List

# Representa un individuo dentro de la población del algoritmo genético
@dataclass
class HuertoType:
    # Lista de plantas seleccionadas para el huerto
    plants: List[int]
    # Información de la parcela asignada
    parcela: ParcelaType
    
    # Compatibilidad entre especies plantadas (CEEP)
    # en ingles:
    # Compatibility between planted species (CBPS)
    compatibilityBetweenPlantedSpecies: float = 0.0

    # Porcentaje de Satisfacción del Rendimiento Alimenticio o Terapéutico Alcanzado (PSRATA)
    # en ingles: 
    # Percentage of Satisfaction with the Nutritional or Therapeutic Performance Achieved (PSNTPA)
    percentageSatisfactionNutritionalTherapeuticPerformanceAchieved: float = 0.0

    # Eficiencia de Consumo de Agua (ECA)
    # en ingles:
    # Water Consumption Efficiency (WCE)
    waterConsumptionEfficiency: float = 0.0

    # Valor total calculado por la función de aptitud
    fitnessScore: float = 0.0
