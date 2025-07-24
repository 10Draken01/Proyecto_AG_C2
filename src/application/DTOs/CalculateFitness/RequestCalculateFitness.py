
from src.domain.entities.HuertoType import HuertoType
from dataclasses import dataclass


@dataclass
class RequestCalculateFitness:
    """
    DTO para solicitar el cálculo de la aptitud de un huerto.
    Contiene la información necesaria para calcular el puntaje de aptitud.
    """
    huerto: HuertoType