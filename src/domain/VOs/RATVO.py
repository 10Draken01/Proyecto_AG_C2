from dataclasses import dataclass

@dataclass
class RATVO:
    """
    Representa el rendimiento alimenticio o terapéutico de un huerto.
    """
    vegetable_percentage: float  # Porcentaje de vegetales
    medicinal_percentage: float  # Porcentaje de plantas medicinales