from typing import List, Dict
from src.domain.VOs.PlantVO import PlantVO
from src.domain.VOs.RATVO import RATVO
from src.domain.entities.ParcelaType import ParcelaType
from src.application.usecases.CalculateFitnessUseCase import CalculateFitnessUseCase
from src.domain.entities.HuertoType import HuertoType

# from src.domain.entities.PlantType import PlantType  # Removed unused import
from src.application.DTOs.CalculateFitness.RequestCalculateFitness import RequestCalculateFitness
import json


# obtener la data del json de la lista de plantas 
# necesitamos leer el archivo JSON que contiene la lista de plantas

dir_plantas_json = 'src/data/plants_with_id.json'
dir_matriz_compatibilidad_json = 'src/data/matriz_compatibilities.json'

with open(dir_plantas_json, 'r', encoding='utf-8') as file:
    data = json.load(file)
    plantas_data: List[PlantVO] = [PlantVO(**item) for item in data]

with open(dir_matriz_compatibilidad_json, 'r', encoding='utf-8') as file:
    matriz_compatibilidad_data: Dict[str, Dict[str, float]] = json.load(file)
    print("Cilantro:", matriz_compatibilidad_data["Cilantro"]["Cilantro"])

ratd: RATVO = RATVO(
    vegetable_percentage= 0.1,
    medicinal_percentage= 0.5,
)

calculate_fitness_use_case = CalculateFitnessUseCase(plantas_data, matriz_compatibilidad_data, ratd)

# generar Huerto de Prueba

# Size de la verdolaga es 0.1 m^2
id_Verdolaga = 3
# weeklyWatering de la verdolaga es 6 litros
weeklyWatering_Verdolaga = 6

# Size del bok choy es 0.18 m^2
id_Bok_Choy = 4
# weeklyWatering del bok choy es 18 litros
weeklyWatering_Bok_Choy = 18

# Size del rábano es 0.08 m^2
id_Rábano = 5
# weeklyWatering del rábano es 6 litros
weeklyWatering_Rábano = 13

# Size de la albahaca es 0.18 m^2
id_Albahaca = 11
# weeklyWatering de la albahaca es 18 litros
weeklyWatering_Albahaca = 18

# inicializamos las plantas de prueba de esta manera para verlo mas visual
# Deberia quedar asi:
# plants: List[int] = [
#     id_Verdolaga, id_Bok_Choy, id_Rábano, id_Albahaca
# ]
plants: Dict[str, int] = {
    "Verdolaga": id_Verdolaga,
    "Bok Choy": id_Bok_Choy,
    "Rábano": id_Rábano,
    "Albahaca": id_Albahaca,
}

# Con 4 plantas de prueba
layout: List[int] = [
    # Fila 1
    [plants["Verdolaga"]],
        # la celda de la fila 1 tiene mas celdas entran varios rabanos
        # por lo que se puede considerar como una celda padre
        # en esta caso la celda padre mide 0.18 m^2
        [
            [plants["Rábano"]], [plants["Rábano"]]
        ],
    ["VOID"], 
    # Fila 2
    [plants["Bok Choy"]], [plants["Verdolaga"]], [plants["Albahaca"]],
        # la celda de la fila 2 tiene mas celdas entran varios
    # Fila 3
    ["VOID"], [plants["Bok Choy"]], ["VOID"],
]

parcela: ParcelaType = ParcelaType(
    size_x=6.0,  # 3 metros de ancho
    size_y=5.0,  # 5 metros de largo
    layout=layout
)

huerto: HuertoType = HuertoType(
    plants=[
        id_Verdolaga, id_Bok_Choy, id_Rábano, id_Albahaca
    ],
    parcela= parcela,
    compatibilityBetweenPlantedSpecies=0.0,
    percentageSatisfactionNutritionalTherapeuticPerformanceAchieved=0.0,
    waterConsumptionEfficiency=0.0,
)

requestCalculateFitness: RequestCalculateFitness = RequestCalculateFitness(
    huerto=huerto
)

response = calculate_fitness_use_case.execute(requestCalculateFitness = requestCalculateFitness)

print("Mensaje:", response.message)
print("Éxito:", response.success)
print("Huerto:")
print("  Plants:", response.huerto.plants)
print("  Parcela Size:", response.huerto.parcela.size_x, "x", response.huerto.parcela.size_y)
print("  Parcela Layout:")
for row in response.huerto.parcela.layout:
    print("    ", row)
    
print("  Compatibility Between Planted Species:", response.huerto.compatibilityBetweenPlantedSpecies)
print("  Percentage Satisfaction Nutritional Therapeutic Performance Achieved:", response.huerto.percentageSatisfactionNutritionalTherapeuticPerformanceAchieved)
print("  Water Consumption Efficiency:", response.huerto.waterConsumptionEfficiency)
print("  Fitness Score:", response.huerto.fitnessScore)