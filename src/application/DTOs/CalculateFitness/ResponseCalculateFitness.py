
from traitlets import Int
from dataclasses import dataclass


@dataclass
class ResponseCalculateFitness:
    """
    DTO para solicitar el cálculo de la aptitud de un huerto.
    Contiene la información necesaria para calcular el puntaje de aptitud.
    """
    message: str
    success: bool
    fitness: Int | None