from dataclasses import dataclass, field
from typing import Literal

@dataclass
class PlantType:
    # Identificador único de la planta
    id: int
    # Coordenada X en el espacio del jardín
    posX: int
    # Coordenada Y en el espacio del jardín
    posY: int
    # Cantidad de plantas
    quantity: int