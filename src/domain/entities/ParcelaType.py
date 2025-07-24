from dataclasses import dataclass
from typing import List, Literal, Union


@dataclass
class ParcelaType:
    # Tamano de la parcela en m
    size_x: float
    size_y: float
    # Matriz de distribución (ubicación espacial)
    layout: List[List[Union[int, Literal["VOID"]]]]