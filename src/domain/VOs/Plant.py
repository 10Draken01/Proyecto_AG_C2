from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Plant:
    # Identificador único de la planta
    id: int
    # Ejemplo: "Albahaca", "Tomate cherry"
    species: str

    # Nombre científico
    scientificName: str

    # Puede contener varios tipos, sin repeticiones
    type: set[Literal["vegetable", "medicinal", "aromatic", "ornamental"]]
    
    # Requerimiento de sol
    sunRequirement: Literal["high", "medium", "low"]

    # Litros
    weeklyWatering: int

    # Días hasta la cosecha
    harvestDays: int

    # Tipo de suelo recomendado
    soilType: str

    # Litros por kg de producción
    waterPerKg: int

    # Lista de beneficios (nutricionales, medicinales, etc.)
    benefits: list[str] = field(default_factory=list)

    # Tamaño de la planta en m^2
    size: float