from typing import Dict, List, Literal, Union
from domain.VOs.RATVO import RATVO
from domain.entities.HuertoType import HuertoType
from domain.VOs.PlantVO import PlantVO
from application.DTOs.CalculateFitness.RequestCalculateFitness import RequestCalculateFitness
from application.DTOs.CalculateFitness.ResponseCalculateFitness import ResponseCalculateFitness

class CalculateFitnessUseCase:
    _weight_1: float = 0.15     # Compatibilidad especies
    _weight_2: float = 0.20     # Rendimiento
    _weight_3: float = 0.20     # Eficiencia hídrica
    _weight_4: float = 0.10     # Uso espacio
    _weight_5: float = 0.10     # Luz solar/sombra
    _weight_6: float = 0.10     # Facilidad mantenimiento
    _weight_7: float = 0.15     # Cumplimiento objetivo
    
    _CEE: float = 0.0           # Compatibilidad entre Especies
    _PSRATD: float = 0.0        # Porcentaje de Satisfacción del Rendimiento Alimenticio o Terapéutico Deseado
    _ECA: float = 0.0           # Eficiencia de Consumo de Agua
    
    _FITNESS: float = 0.0       # Puntaje de aptitud
    _PLANTS: List[PlantVO] = []
    _PLANTS_IN_HUERTO: List[PlantVO] = []
    _MATRIZ_COMPATIBILIDAD: Dict[Dict[int]] = []
    _RATD: RATVO            # Rendimiento Alimenticio o Terapéutico Deseado

    _SIZE_CELD_MIN: Dict[Literal["width", "height"], float] = {"width": 0.5, "height": 0.5}  # Tamaño mínimo de celda
    _SIZE_CELD_MAX: Dict[Literal["width", "height"], float] = {"width": 1.0, "height": 1.0}  # Tamaño máximo de celda

    _RESPONSE: ResponseCalculateFitness = ResponseCalculateFitness(
        message="",
        success=False,
        fitness=None
    )

    def __init__(self, plants: List[PlantVO], matriz_compatibilidad: Dict[Dict[int]], ratd: RATVO):
        """
        Inicializa el caso de uso con las plantas, la matriz de compatibilidad y el RATSODUVO.
        """
        self._PLANTS = plants
        self._MATRIZ_COMPATIBILIDAD = matriz_compatibilidad
        self._RATD = ratd

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
        
        # Calculamos el Rendimiento Alimenticio o Terapéutico del Huerto
        self.__Calculate_PSRATD()

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
        
        # Obtenemos el layout del huerto
        layout = self.HUERTO.parcela.layout

        def generate_key_frozenset(tuplas: Union[tuple, tuple]) -> int:
            """
            Genera un ID usando frozenset, que es independiente del orden
            """
            return hash(frozenset(tuplas))

        for row_index, row_initial in enumerate(layout):
                        
            # calcuamos la posicion de las celdas vecinas "Derecha" y "Abajo"
            filas_parcela = self.HUERTO.parcela.layout

            def get_pairs(row: int | List[int]) -> None:
                
                # Iteramos sobre las celdas de la fila de 2 en 2
                for celd_index in range(0, len(row), 2):
                    celd = row[celd_index]
                    if isinstance(celd, list):
                        # celd contiene una lista de ids de plantas
                        get_pairs(celd)
                    elif isinstance(celd, int):
                        # celd contiene la id de la planta
                        # buscar la planta en la lista de plantas
                        # [[c][r]]
                        # [[b][rb]]
                        # Donde c es la celda en la que estamos calculando las vecinas de esa, r es la celda derecha, b es la celda abajo y br es la celda derecha abajo
                        id_celd_right = celd_index + 1 if celd_index + 1 < len(row) else None
                        id_celd_bottom = row_index + 1 if row_index + 1 < len(filas_parcela) else None

                        # Extraemos la fila de abajo
                        row_bottom = layout[row_index + 1]
                        
                        # extraemos la cantidad de celdas en la fila
                        celds_in_row_bottom = len(row_bottom)
                        id_celd_bottom_right = row_bottom[celd_index + 1] if celd_index + 1 < celds_in_row_bottom else None

                        # Obtenemos las especies de las plantas en las celdas vecinas
                        plant_species_center = next((p.species for p in self._PLANTS_IN_HUERTO if p.id == celd), None)
                        plant_species_right = next((p.species for p in self._PLANTS_IN_HUERTO if p.id == id_celd_right), None)
                        plant_species_bottom = next((p.species for p in self._PLANTS_IN_HUERTO if p.id == id_celd_bottom), None)
                        plant_species_right_bottom = next((p.species for p in self._PLANTS_IN_HUERTO if p.id == id_celd_bottom_right), None)

                        # generamos las keys para agregar al diccionario de parejas
                        key_center_right = generate_key_frozenset((plant_species_center, plant_species_right))
                        key_center_bottom = generate_key_frozenset((plant_species_center, plant_species_bottom))
                        key_center_right_bottom = generate_key_frozenset((plant_species_center, plant_species_right_bottom))
                        
                        # Obtenemos las compatibilidades de las especies
                        valor_compatibilidad_pareja_1 = self._MATRIZ_COMPATIBILIDAD[plant_species_center][plant_species_right]
                        valor_compatibilidad_pareja_2 = self._MATRIZ_COMPATIBILIDAD[plant_species_center][plant_species_bottom]
                        valor_compatibilidad_pareja_3 = self._MATRIZ_COMPATIBILIDAD[plant_species_center][plant_species_right_bottom]
                        
                        # Agregamos las parejas al diccionario solo si no existen
                        if not key_center_right in pairs:
                            pairs[key_center_right] = valor_compatibilidad_pareja_1
                        if not key_center_bottom in pairs:
                            pairs[key_center_bottom] = valor_compatibilidad_pareja_2
                        if not key_center_right_bottom in pairs:
                            pairs[key_center_right_bottom] = valor_compatibilidad_pareja_3

            get_pairs(row_initial)

            # Inicializamos la suma de compatibilidad
            # Ejemplo de calculo de suma de compatibilidad vecinas
            # parejas  = {
            #             "CilantroEpazote": 0.5,
            #             "CilantroPerejil": 1,
            #         }
            # sumaCompatibilidadesVecinas  = parejas["CilantroEpazote"] + parejas["CilantroPerejil"]
            sumaCompatibilidadesVecinas = 0
            
            # Inicializamos la pareja de compatibilidad máxima
            pareja_compatibilidad_maxima = 0
            
            # Iteramos sobre las parejas y sumamos sus valores de compatibilidad
            for _, value in pairs.items():
                # Sumamos el valor de compatibilidad de la pareja
                sumaCompatibilidadesVecinas  += value
                pareja_compatibilidad_maxima = max(pareja_compatibilidad_maxima, value)
                
            # Calculamos la compatibilidad maxima posible
            # Ejemplo de calculo de compatibilidad maxima posible
            # total_parejas = 2
            # pareja_compatibilidad_maxima = parejas["CilantroPerejil"]
            # compatibilidadMaximaPosible = total_parejas * pareja_compatibilidad_maxima
            
            compatibilidadMaximaPosible = len(pairs) * pareja_compatibilidad_maxima

            # Calculamos la compatibilidad entre especies
            self._CEE += sumaCompatibilidadesVecinas  / compatibilidadMaximaPosible 
    
    # Calculamos el Porcentaje de Satisfacción del Rendimiento Alimenticio o Terapéutico Deseado (PSRATD)
    def __Calculate_PSRATD(self) -> None:
        """
        Calcula el Rendimiento Alimenticio o Terapéutico del Huerto (RATH).
        :return: Rendimiento Alimenticio o Terapéutico del Huerto.
        """
        # Calculamos el total de plantas en el huerto
        total_plants = len(self._PLANTS_IN_HUERTO)

        # Calculamos el total de vegetales y plantas medicinales
        total_vegetables = 0
        total_medicinal = 0
        for plant in self._PLANTS_IN_HUERTO:
            if "vegetable" in plant.type:
                total_vegetables += 1
            if "medicinal" in plant.type:
                total_medicinal += 1

        # Calculamos el porcentaje de vegetales y plantas medicinales RATH
        vegetable_percentage = (total_vegetables / total_plants)
        medicinal_percentage = (total_medicinal / total_plants)

        RATH = RATVO(
            vegetable_percentage = vegetable_percentage,
            medicinal_percentage = medicinal_percentage
        )

        # Calculamos le diferencia absoluta promedio entre el RATH y el RATD
        average_difference = (
            abs(RATH.vegetable_percentage - self._RATD.vegetable_percentage) +
            abs(RATH.medicinal_percentage - self._RATD.medicinal_percentage)
        ) / 2

        # Ahora la restamos de 1 para que un mejor cumplimiento dé un valor más alto.
        self._PSRATD = 1 - average_difference

    # Calculamos la Eficiencia de Consumo de Agua (ECA)
    def __Calculate_ECA(self) -> None:
        """
        Calcula la Eficiencia de Consumo de Agua.
        :return: Eficiencia de Consumo de Agua.
        """
        
        # Obtenemos el layout del huerto
        layout = self.HUERTO.parcela.layout
        
        # Definimos una variable para contar el total de plantas en el layout del huerto
        total_plants_in_layout = 0
        
        # Definimos el contador de requerimiento hídrico total (RHT)
        RHT = 0
        
        # Definimos el contador de requerimiento hídrico máximo (RH_MAX)
        RH_MAX: float = 0
        
        # Definimos funcion para obtener el requerimiento hídrico semanal de una fila del layout
        # Recibe una celda que puede ser una lista o un entero
        def get_weeklyWatering_row(celd: any) -> int:
            """
            Obtiene el requerimiento hídrico semanal de una fila del layout.
            :param row: Fila del layout.
            :return: Requerimiento hídrico semanal de la fila.
            """
            # Si la fila es una lista, iteramos sobre sus celdas
            if isinstance(celd, list):
                # Definimos que la celda es una lista de celdas
                row = celd
                sum_weekly_watering = 0
                for sub_celd in row:
                    sum_weekly_watering += get_weeklyWatering_row(sub_celd)
                return sum_weekly_watering

            if isinstance(celd, int):
                total_plants_in_layout += 1
                plant = next((p for p in self._PLANTS_IN_HUERTO if p.id == celd), None)
                if plant.weeklyWatering > RH_MAX:
                    RH_MAX = plant.weeklyWatering
                return plant.weeklyWatering
            return 0

        for row in layout:
            RHT += get_weeklyWatering_row(row)
        
        # Calculamos el Requerimiento hídrico total maximo (RHT) y el requerimiento hídrico máximo (RHT_MAX)
        RHT_MAX = RH_MAX * total_plants_in_layout

        # Calculamos la Eficiencia de Consumo de Agua (ECA)
        self._ECA = 1 - (RHT / RHT_MAX)