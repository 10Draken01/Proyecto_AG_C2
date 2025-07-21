from dataclasses import dataclass, field
from typing import List, Literal
@dataclass
class ParcelaType:
    # Tamano de la parcela en m
    size_x: float
    size_y: float
    # Matriz de distribución (ubicación espacial)
    layout: List[List[int]]
    