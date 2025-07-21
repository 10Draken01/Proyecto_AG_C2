from typing import Dict, List
from domain.entities.HuertoType import HuertoType
from domain.VOs.PlantVO import PlantVO

class CalculateFitnessUseCase:
    _weight_1: float = 0.15  # Compatibilidad especies
    _weight_2: float = 0.20  # Rendimiento
    _weight_3: float = 0.20  # Eficiencia hídrica
    _weight_4: float = 0.10  # Uso espacio
    _weight_5: float = 0.10  # Luz solar/sombra
    _weight_6: float = 0.10  # Facilidad mantenimiento
    _weight_7: float = 0.15  # Cumplimiento objetivo
    _CEE: float = 0.0  # Compatibilidad entre Especies
    _ECA: float = 0.0  # Eficiencia de Consumo de Agua
    _PLANTS: List[PlantVO] = []
    _PLANTS_IN_HUERTO: List[PlantVO] = []
    _MATRIZ_COMPATIBILIDAD: Dict[Dict[int]] = []

    def __init__(self, plants: List[PlantVO], matriz_compatibilidad: Dict[Dict[int]]):
        self._PLANTS = plants
        self._MATRIZ_COMPATIBILIDAD = matriz_compatibilidad

    def execute(self, huerto: HuertoType) -> int:
        """
        Calcula el puntaje de aptitud de una población.
        :param poblation: Lista de individuos.
        :return: Puntaje de aptitud total.
        """
        
        self.HUERTO = huerto
        # Inicializamos las plantas en el huerto, extraemos la información de las plantas
        self.__Inicializate_Plants_In_Huerto()
        
        # Calculamos la compatibilidad entre especies plantadas
        self.__Calculate_Compatibility()

        # Calculamos la eficiencia de Consumo de Agua
        self.__Calculate_ECA()

    def __Inicializate_Plants_In_Huerto(self) -> None:
        """
        Inicializa la lista de plantas en el huerto.
        :param huerto: HuertoType con las plantas.
        """
        for plant in self.HUERTO.plants:
            # buscar la informacion de la planta en la lista de plantas
            plant_info = next((p for p in self._PLANTS if p.id == plant.id), None)
            if plant_info:
                self._PLANTS_IN_HUERTO.append(plant_info)
                
    def __Calculate_Compatibility(self) -> int:
        """
        Calcula la compatibilidad entre especies plantadas.
        :return: Puntaje de compatibilidad.
        """
        compatibility_score = 0
        for i in range(len(self.HUERTO.plants)):
            for j in range(i + 1, len(self.HUERTO.plants)):
                plant1 = self.HUERTO.plants[i]
                plant2 = self.HUERTO.plants[j]
                compatibility_score += self._MATRIZ_COMPATIBILIDAD.get(plant1.id, {}).get(plant2.id, 0)
        return compatibility_score

    def __Calculate_ECA(self) -> None:
        """
        Calcula la Eficiencia de Consumo de Agua.
        :return: Eficiencia de Consumo de Agua.
        """
                
        # Calculamos el requerimiento hídrico total
        RHT = self.__Calculate_RHT()

        # Calculamos el requerimiento hídrico total máximo
        RHT_MAX = self.__Calculate_RHT_MAX()

        self._ECA = 1 - (RHT / RHT_MAX)

    def __Calculate_RHT(self):
        """
        Calcula el requerimiento hídrico total de un individuo.
        :return: Requerimiento hídrico total.
        """
        
        # Sumamos el riego semanal de todas las plantas en el huerto
        RHT = sum(plant.weeklyWatering for plant in self._PLANTS_IN_HUERTO)
        return RHT
        
        
    def __Calculate_RHT_MAX(self) -> int:
        """
        Calcula el requerimiento hídrico total máximo de un individuo.
        :return: Requerimiento hídrico total máximo.
        """
        # Calculamos el número de celdas ocupadas en el Layout del huerto
        cantidad_celdas = self.__Calculate_Celds()
        RHT_MAX = 0
        for plant in self.HUERTO.plants:
            # buscar la informacion de la planta en la lista de plantas
            for plant in self._PLANTS_IN_HUERTO:
                if plant.weeklyWatering > 0:
                    RHT_MAX += plant.weeklyWatering * cantidad_celdas

        return RHT_MAX

    def __Calculate_Celds(self) -> int:
        """
        Calcula el número de celdas ocupadas por las plantas.
        :return: Número de celdas ocupadas.
        """
        occupied_cells = 0
        for row in self.HUERTO.parcela.layout:
            if not isinstance(row, list):
                occupied_cells += 1
        return occupied_cells
    
    # Calculamos Rendimiento Alimenticio o Terapéutico Según el Usuario
    def __Calculate_RATSODU(self):
        pass