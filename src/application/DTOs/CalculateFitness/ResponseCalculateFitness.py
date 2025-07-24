
from dataclasses import dataclass
from src.domain.entities.HuertoType import HuertoType


@dataclass
class ResponseCalculateFitness:
    """
    DTO para solicitar el cálculo de la aptitud de un huerto.
    Contiene la información necesaria para calcular el puntaje de aptitud.
    """
    message: str
    success: bool
    huerto: HuertoType | None