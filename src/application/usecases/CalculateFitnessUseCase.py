from typing import Dict, List, Literal, Union
from domain.VOs import RATSODUVO
from domain.entities.HuertoType import HuertoType
from domain.VOs.PlantVO import PlantVO
from application.DTOs.CalculateFitness.RequestCalculateFitness import RequestCalculateFitness
from application.DTOs.CalculateFitness.ResponseCalculateFitness import ResponseCalculateFitness

class CalculateFitnessUseCase:
    _weight_1: float = 0.15  # Compatibilidad especies
    _weight_2: float = 0.20  # Rendimiento
    _weight_3: float = 0.20  # Eficiencia hídrica
    _weight_4: float = 0.10  # Uso espacio
    _weight_5: float = 0.10  # Luz solar/sombra
    _weight_6: float = 0.10  # Facilidad mantenimiento
    _weight_7: float = 0.15  # Cumplimiento objetivo
    _RATSUDO: RATSODUVO
    _CEE: float = 0.0  # Compatibilidad entre Especies
    _ECA: float = 0.0  # Eficiencia de Consumo de Agua
    _FITNESS: float = 0.0  # Puntaje de aptitud
    _PLANTS: List[PlantVO] = []
    _PLANTS_IN_HUERTO: List[PlantVO] = []
    _MATRIZ_COMPATIBILIDAD: Dict[Dict[int]] = []

    _SIZE_CELD_MIN: Dict[Literal["width", "height"], float] = {"width": 0.5, "height": 0.5}  # Tamaño mínimo de celda
    _SIZE_CELD_MAX: Dict[Literal["width", "height"], float] = {"width": 1.0, "height": 1.0}  # Tamaño máximo de celda

    _RESPONSE: ResponseCalculateFitness = ResponseCalculateFitness(
        message="",
        success=False,
        fitness=None
    )

    def __init__(self, plants: List[PlantVO], matriz_compatibilidad: Dict[Dict[int]], ratsudo: RATSODUVO):
        """
        Inicializa el caso de uso con las plantas, la matriz de compatibilidad y el RATSODUVO.
        """
        self._PLANTS = plants
        self._MATRIZ_COMPATIBILIDAD = matriz_compatibilidad
        self._RATSUDO = ratsudo

    def execute(self, requestCalculateFitness: RequestCalculateFitness) -> ResponseCalculateFitness:
        """
        Calcula el puntaje de aptitud de una población.
        :param poblation: Lista de individuos.
        :return: Puntaje de aptitud total.
        """

        self.HUERTO = requestCalculateFitness.huerto
        # Inicializamos las plantas en el huerto, extraemos la información de las plantas
        self.__Inicializate_Plants_In_Huerto()
        
        # Calculamos la compatibilidad entre especies plantadas
        self.__Calculate_Compatibility()

        # Calculamos la eficiencia de Consumo de Agua
        self.__Calculate_ECA()
        
        
        
        return self._RESPONSE

    def __Inicializate_Plants_In_Huerto(self) -> None:
        """
        Inicializa la lista de plantas en el huerto.
        :param huerto: HuertoType con las plantas.
        """
        
        try:
            for plant in self.HUERTO.plants:
                # buscar la informacion de la planta en la lista de plantas
                plant_info = next((p for p in self._PLANTS if p.id == plant.id), None)
                if plant_info:
                    self._PLANTS_IN_HUERTO.append(plant_info)
        except Exception as e:
            # Manejo de errores al inicializar las plantas
            print(f'Hubo un error: {e}')
            self._RESPONSE.message = f"Error al inicializar las plantas en el huerto: {str(e)}"
            self._RESPONSE.success = False
            return

    def __Calculate_Compatibility(self) -> None:
        """
        Calcula la compatibilidad entre especies plantadas.
        :return: Puntaje de compatibilidad.
        """
        # Método 1: Usando frozenset, recibe una lista de 2 tuplas 
        # Lo tipamos como Union[tuple, tuple] para permitir tuplas de diferentes tipos
        # y por ejemplo recibiria una tupla de enteros
        
        # Inicializamos la variable para parejas
        pairs: Dict[str,int] = {}

        def generate_id_frozenset(tuplas: Union[tuple, tuple]) -> int:
            """
            Genera un ID usando frozenset, que es independiente del orden
            """
            return hash(frozenset(tuplas))

        for row_index, row_initial in enumerate(self.HUERTO.parcela.layout):
            index_position_plants = {
                "right": row_index + 1,
                "bottom": row_index
            }

            def get_pairs(row: int | List[int]) -> None:
                for celd_index, celd in enumerate(row):
                    if isinstance(celd, list):
                        get_pairs(celd)
                    else:
                        # celd contiene la id de la planta
                        # buscar la planta en la lista de plantas
                        plant_species_center = next((p.species for p in self._PLANTS_IN_HUERTO if p.id == celd), None)
                        
                        # calcuamos la posicion de las celdas vecinas "Derecha" y "Abajo"
                        filas_parcela = self.HUERTO.parcela.layout

                        index_celd_bottom = row_index + 1 if row_index + 1 < len(filas_parcela) else None
                        index_celd_right = celd_index + 1 if celd_index + 1 < len(row) else None
                        index_celd_right_bottom = row[row_index + 1]

                        # Obtenemos las especies de las plantas en las celdas vecinas
                        plant_species_right = next((p.species for p in self._PLANTS_IN_HUERTO if p.id == celd_right), None)
                        plant_species_bottom = next((p.species for p in self._PLANTS_IN_HUERTO if p.id == celd_bottom), None)

            get_pairs(row_initial)
                    

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