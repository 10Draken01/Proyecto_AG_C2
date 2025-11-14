"""
Algoritmo Genético para optimización de huertos urbanos.
Basado en especificación LaTeX PlantGen - Capítulo 3.
"""
import random
import math
from typing import List, Tuple, Dict, Optional
from src.domain.entities.Plant import Plant
from src.domain.entities.GardenLayout import GardenLayout
from src.domain.value_objects.GardenObjective import GardenObjective
from src.domain.value_objects.GardenConstraints import GardenConstraints


class GeneticAlgorithm:
    """
    Implementación del Algoritmo Genético Multi-Objetivo para PlantGen.

    Parámetros según documento LaTeX (Tabla 3.1):
    - Población: 40 individuos
    - Generaciones máximas: 150
    - Probabilidad de cruza: 0.85
    - Tasa de mutación: 0.08
    - Torneo k: 3
    - Individuos elite: 3
    - Paciencia: 20 generaciones sin mejora
    """

    def __init__(
        self,
        plants: List[Plant],
        compatibility_matrix: Dict[str, Dict[str, float]],
        objective: GardenObjective,
        constraints: GardenConstraints,
        population_size: int = 40,
        max_generations: int = 150,
        crossover_rate: float = 0.85,
        mutation_rate: float = 0.08,
        tournament_k: int = 3,
        elite_count: int = 3,
        patience: int = 20
    ):
        self.plants = plants
        self.compatibility_matrix = compatibility_matrix
        self.objective = objective
        self.constraints = constraints

        # Parámetros del AG
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_k = tournament_k
        self.elite_count = elite_count
        self.patience = patience

        # Mapeo de especies a IDs
        self.species_to_plant = {plant.species: plant for plant in plants}

        # Estadísticas
        self.generation_stats = []

    def run(self) -> List[GardenLayout]:
        """
        Ejecuta el algoritmo genético completo.

        Returns:
            Top 3 mejores configuraciones de huerto
        """
        # Fase 1: Inicialización de población
        population = self._initialize_population()

        # Evaluar población inicial
        for individual in population:
            self._evaluate_fitness(individual)

        best_fitness = max(ind.fitness for ind in population)
        generations_without_improvement = 0

        # Ciclo evolutivo
        for generation in range(self.max_generations):
            # Fase 2: Selección por Torneo
            selected = self._tournament_selection(population)

            # Fase 3: Cruza de Dos Puntos
            offspring = []
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    if random.random() < self.crossover_rate:
                        child1, child2 = self._two_point_crossover(selected[i], selected[i+1])
                        offspring.extend([child1, child2])
                    else:
                        offspring.extend([selected[i].clone(), selected[i+1].clone()])

            # Fase 4: Mutación por Intercambio
            for individual in offspring:
                if random.random() < self.mutation_rate:
                    self._swap_mutation(individual)

            # Fase 5: Evaluación
            for individual in offspring:
                self._evaluate_fitness(individual)

            # Fase 6: Reemplazo Generacional con Elitismo (μ+λ)
            population = self._elitist_replacement(population, offspring)

            # Verificar mejora
            current_best = max(ind.fitness for ind in population)
            if current_best > best_fitness:
                best_fitness = current_best
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1

            # Guardar estadísticas
            self.generation_stats.append({
                'generation': generation,
                'best_fitness': current_best,
                'avg_fitness': sum(ind.fitness for ind in population) / len(population),
                'diversity': self._calculate_diversity(population)
            })

            # Fase 7: Criterios de parada
            if generations_without_improvement >= self.patience:
                print(f"Convergencia: Sin mejora en {self.patience} generaciones")
                break

            # Verificar convergencia por varianza
            fitness_variance = self._calculate_variance([ind.fitness for ind in population])
            if fitness_variance < 0.001:
                print(f"Convergencia: Varianza de fitness < 0.001")
                break

        # Retornar top 3 mejores soluciones
        population.sort(key=lambda x: x.fitness, reverse=True)
        return population[:3]

    def _initialize_population(self) -> List[GardenLayout]:
        """
        Fase 1: Inicialización de población (40 individuos).
        Genera layouts aleatorios respetando restricciones hard.
        """
        population = []
        for _ in range(self.population_size):
            individual = self._create_random_individual()
            population.append(individual)
        return population

    def _create_random_individual(self) -> GardenLayout:
        """
        Crea un individuo aleatorio (layout de huerto).
        Respeta restricciones de área, agua y presupuesto.
        """
        # Dimensiones aleatorias dentro del área permitida
        area = self.constraints.max_area
        aspect_ratio = random.uniform(0.5, 2.0)  # Ratio ancho/alto
        width = math.sqrt(area * aspect_ratio)
        height = area / width

        # Tamaño de celda (entre 0.5 y 1.0 m²)
        cell_size = random.uniform(0.5, 1.0)

        # Calcular dimensiones de la matriz
        cols = int(width / cell_size)
        rows = int(height / cell_size)

        # Crear layout vacío
        layout = [[None for _ in range(cols)] for _ in range(rows)]

        # Llenar con plantas aleatorias respetando restricciones
        total_water = 0
        total_cost = 0
        used_area = 0

        available_cells = [(r, c) for r in range(rows) for c in range(cols)]
        random.shuffle(available_cells)

        for row, col in available_cells:
            # Seleccionar planta aleatoria
            plant = random.choice(self.plants)

            # Calcular costo estimado (10 MXN por m²)
            plant_cost = plant.size * 50

            # Verificar restricciones
            if (total_water + plant.weekly_watering <= self.constraints.max_water_weekly and
                total_cost + plant_cost <= self.constraints.max_budget and
                used_area + plant.size <= self.constraints.max_area):

                layout[row][col] = plant.id
                total_water += plant.weekly_watering
                total_cost += plant_cost
                used_area += plant.size

        return GardenLayout(width=width, height=height, layout=layout)

    def _tournament_selection(self, population: List[GardenLayout]) -> List[GardenLayout]:
        """
        Fase 2: Selección por Torneo (k=3).
        Selecciona población_size individuos mediante torneos.
        """
        selected = []
        for _ in range(self.population_size):
            # Seleccionar k individuos aleatorios
            tournament = random.sample(population, self.tournament_k)
            # Retornar el mejor
            winner = max(tournament, key=lambda x: x.fitness)
            selected.append(winner)
        return selected

    def _two_point_crossover(self, parent1: GardenLayout, parent2: GardenLayout) -> Tuple[GardenLayout, GardenLayout]:
        """
        Fase 3: Cruza de Dos Puntos.
        Divide el layout en 3 secciones e intercambia la sección central.
        """
        rows = len(parent1.layout)
        cols = len(parent1.layout[0]) if rows > 0 else 0

        # Seleccionar dos puntos de corte
        if rows < 3:
            # Si hay muy pocas filas, clonar padres
            return parent1.clone(), parent2.clone()

        cut1 = random.randint(1, rows - 2)
        cut2 = random.randint(cut1 + 1, rows - 1)

        # Crear hijos
        child1_layout = []
        child2_layout = []

        for i in range(rows):
            if i < cut1 or i >= cut2:
                # Secciones externas
                child1_layout.append(parent1.layout[i][:])
                child2_layout.append(parent2.layout[i][:])
            else:
                # Sección central intercambiada
                child1_layout.append(parent2.layout[i][:])
                child2_layout.append(parent1.layout[i][:])

        child1 = GardenLayout(width=parent1.width, height=parent1.height, layout=child1_layout)
        child2 = GardenLayout(width=parent2.width, height=parent2.height, layout=child2_layout)

        return child1, child2

    def _swap_mutation(self, individual: GardenLayout) -> None:
        """
        Fase 4: Mutación por Intercambio.
        Intercambia dos plantas aleatorias en el layout.
        """
        rows = len(individual.layout)
        cols = len(individual.layout[0]) if rows > 0 else 0

        if rows == 0 or cols == 0:
            return

        # Seleccionar dos celdas aleatorias
        r1, c1 = random.randint(0, rows-1), random.randint(0, cols-1)
        r2, c2 = random.randint(0, rows-1), random.randint(0, cols-1)

        # Intercambiar
        individual.layout[r1][c1], individual.layout[r2][c2] = \
            individual.layout[r2][c2], individual.layout[r1][c1]

    def _evaluate_fitness(self, individual: GardenLayout) -> None:
        """
        Fase 5: Evaluación de Fitness.
        Calcula las 4 métricas y el fitness global.
        """
        # Calcular métricas individuales
        individual.cee = self._calculate_cee(individual)
        individual.psntpa = self._calculate_psntpa(individual)
        individual.wce = self._calculate_wce(individual)
        individual.ue = self._calculate_ue(individual)

        # Calcular fitness global con pesos dinámicos
        weights = self.objective.get_weights()
        individual.fitness = (
            weights['cee'] * individual.cee +
            weights['psntpa'] * individual.psntpa +
            weights['wce'] * individual.wce +
            weights['ue'] * individual.ue
        )

    def _calculate_cee(self, individual: GardenLayout) -> float:
        """
        Calcula Compatibilidad Entre Especies (CEE).
        Fórmula: Σ(w_dist · C(c,v)) / Σ(w_dist · C_max)
        donde w_dist = e^(-d/σ) con σ = 1.5
        """
        layout = individual.layout
        rows = len(layout)
        cols = len(layout[0]) if rows > 0 else 0

        if rows == 0 or cols == 0:
            return 0.0

        sigma = 1.5  # metros
        total_weighted_compatibility = 0.0
        total_weighted_max = 0.0

        # Analizar pares adyacentes (derecha, abajo, diagonal)
        for r in range(rows):
            for c in range(cols):
                cell_id = layout[r][c]
                if cell_id is None:
                    continue

                cell_plant = next((p for p in self.plants if p.id == cell_id), None)
                if not cell_plant:
                    continue

                # Vecinos: derecha, abajo, diagonal
                neighbors = [
                    (r, c+1, 1.0),      # derecha (distancia 1m)
                    (r+1, c, 1.0),      # abajo (distancia 1m)
                    (r+1, c+1, 1.414)   # diagonal (distancia √2m)
                ]

                for nr, nc, distance in neighbors:
                    if nr < rows and nc < cols and layout[nr][nc] is not None:
                        neighbor_id = layout[nr][nc]
                        neighbor_plant = next((p for p in self.plants if p.id == neighbor_id), None)

                        if neighbor_plant:
                            # Peso por distancia
                            weight = math.exp(-distance / sigma)

                            # Compatibilidad
                            compat = self.compatibility_matrix.get(
                                cell_plant.species, {}
                            ).get(neighbor_plant.species, 0.0)

                            total_weighted_compatibility += weight * compat
                            total_weighted_max += weight * 1.0  # C_max = 1.0

        if total_weighted_max == 0:
            return 0.0

        return max(0.0, min(1.0, total_weighted_compatibility / total_weighted_max))

    def _calculate_psntpa(self, individual: GardenLayout) -> float:
        """
        Calcula Porcentaje de Satisfacción del Rendimiento Nutricional/Terapéutico.
        Basado en cantidad y calidad de plantas según objetivo.
        """
        plant_ids = individual.get_plant_ids()
        if not plant_ids:
            return 0.0

        total_production = 0.0
        target_types_count = 0

        for plant_id in plant_ids:
            plant = next((p for p in self.plants if p.id == plant_id), None)
            if not plant:
                continue

            # Producción estimada
            production = plant.get_production_per_cycle()
            total_production += production

            # Contar plantas según objetivo
            if self.objective.prioritizes_nutrition() and plant.has_type("vegetable"):
                target_types_count += 1
            elif self.objective.prioritizes_medicinal() and plant.has_type("medicinal"):
                target_types_count += 1
            elif self.objective.prioritizes_aesthetics() and plant.has_type("ornamental"):
                target_types_count += 1

        # Normalizar entre 0 y 1
        production_factor = min(total_production / 10.0, 1.0)  # 10 kg objetivo
        type_factor = min(target_types_count / len(plant_ids), 1.0)

        return (production_factor + type_factor) / 2.0

    def _calculate_wce(self, individual: GardenLayout) -> float:
        """
        Calcula Eficiencia Hídrica (Water Consumption Efficiency).
        Fórmula: 1 - (Agua_Total / Agua_Máxima)
        """
        plant_ids = individual.get_plant_ids()
        total_water = 0.0

        for plant_id in plant_ids:
            plant = next((p for p in self.plants if p.id == plant_id), None)
            if plant:
                count = individual.count_plant(plant_id)
                total_water += plant.weekly_watering * count

        if total_water > self.constraints.max_water_weekly:
            return 0.0  # Penalizar si excede restricción hard

        efficiency = 1.0 - (total_water / self.constraints.max_water_weekly)
        return max(0.0, min(1.0, efficiency))

    def _calculate_ue(self, individual: GardenLayout) -> float:
        """
        Calcula Utilización de Espacio (UE).
        Fórmula: Σ(q_p · a_p) / Área_Total ≤ 0.85
        """
        plant_ids = individual.get_plant_ids()
        total_used_area = 0.0

        for plant_id in plant_ids:
            plant = next((p for p in self.plants if p.id == plant_id), None)
            if plant:
                count = individual.count_plant(plant_id)
                total_used_area += plant.size * count

        total_area = individual.get_area()
        utilization = total_used_area / total_area if total_area > 0 else 0.0

        # Penalizar si excede 0.85
        if utilization > 0.85:
            return max(0.0, 1.0 - (utilization - 0.85) * 2)

        return min(1.0, utilization / 0.85)  # Normalizar a [0,1] con óptimo en 0.85

    def _elitist_replacement(self, population: List[GardenLayout], offspring: List[GardenLayout]) -> List[GardenLayout]:
        """
        Fase 6: Reemplazo Generacional con Elitismo (μ+λ).
        Preserva top 3 elite, selecciona mejores 37 de población + offspring.
        """
        # Ordenar población por fitness
        population.sort(key=lambda x: x.fitness, reverse=True)

        # Preservar elite
        elite = population[:self.elite_count]

        # Combinar resto de población con offspring
        combined = population[self.elite_count:] + offspring
        combined.sort(key=lambda x: x.fitness, reverse=True)

        # Seleccionar mejores
        new_population = elite + combined[:self.population_size - self.elite_count]

        return new_population

    def _calculate_diversity(self, population: List[GardenLayout]) -> float:
        """Calcula diversidad de la población (para estadísticas)"""
        if len(population) < 2:
            return 0.0

        fitness_values = [ind.fitness for ind in population]
        return self._calculate_variance(fitness_values)

    def _calculate_variance(self, values: List[float]) -> float:
        """Calcula varianza de una lista de valores"""
        if not values:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
