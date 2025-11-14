# 🏗️ Arquitectura de PlantGen API

## Principios de Diseño

PlantGen API está construida siguiendo los principios de **Clean Architecture** y **Domain-Driven Design (DDD)**, lo que garantiza:

- ✅ **Independencia de frameworks**
- ✅ **Testabilidad**
- ✅ **Independencia de la UI**
- ✅ **Independencia de la base de datos**
- ✅ **Independencia de agentes externos**

---

## Capas de la Arquitectura

### 1. Capa de Dominio (Domain Layer)

**Responsabilidad**: Contiene la lógica de negocio pura y las reglas del dominio.

**Componentes**:

#### Entidades (Entities)
- `Plant`: Representa una planta con sus atributos botánicos
- `GardenLayout`: Representa un diseño de huerto (individuo del AG)
- `CompatibilityPair`: Representa la relación de compatibilidad entre dos plantas

#### Value Objects
- `GardenObjective`: Define el objetivo del huerto (alimenticio, medicinal, etc.)
- `GardenConstraints`: Restricciones hard (área, agua, presupuesto)

#### Repositorios (Interfaces)
- `IPlantRepository`: Contrato para acceso a datos de plantas
- `ICompatibilityRepository`: Contrato para matriz de compatibilidad

#### Servicios de Dominio
- `GeneticAlgorithm`: Implementación del algoritmo genético multi-objetivo

**Principios**:
- Sin dependencias externas
- Inmutabilidad de Value Objects
- Validaciones de dominio en entidades

---

### 2. Capa de Aplicación (Application Layer)

**Responsabilidad**: Orquesta la lógica de negocio y coordina casos de uso.

**Componentes**:

#### DTOs (Data Transfer Objects)
- `GenerateGardenRequest`: DTO de entrada para generación de huerto
- `GenerateGardenResponse`: DTO de salida con soluciones
- `GardenSolutionDTO`: DTO para una configuración de huerto
- `PlantInGardenDTO`: DTO para información de planta en huerto

#### Casos de Uso (Use Cases)
- `GenerateGardenUseCase`: Orquesta la generación de huertos usando AG

**Principios**:
- Depende solo de la capa de dominio
- No tiene conocimiento de frameworks ni infraestructura
- Transforma datos de dominio a DTOs

---

### 3. Capa de Infraestructura (Infrastructure Layer)

**Responsabilidad**: Implementaciones concretas de interfaces y adaptadores externos.

**Componentes**:

#### Database
- `MongoConnection`: Gestión de conexión a MongoDB
- `MongoPlantRepository`: Implementación de IPlantRepository con MongoDB
- `MongoCompatibilityRepository`: Implementación de ICompatibilityRepository

#### API
- `controllers.py`: Controladores FastAPI con endpoints
- Manejo de peticiones HTTP
- Validación de entrada con Pydantic

**Principios**:
- Implementa interfaces definidas en dominio
- Depende de librerías externas (Motor, FastAPI)
- Adaptadores para frameworks

---

## Flujo de Datos

```
Cliente HTTP
    ↓
[FastAPI Controller]
    ↓
[GenerateGardenUseCase]
    ↓
[GeneticAlgorithm] ←→ [PlantRepository] ←→ [MongoDB]
                  ↔ [CompatibilityRepository] ←→ [MongoDB]
    ↓
[GenerateGardenResponse]
    ↓
Cliente HTTP
```

---

## Inversión de Dependencias

La arquitectura sigue el **Dependency Inversion Principle**:

```
Infrastructure → Application → Domain
     ↓               ↓            ↑
  (depende)     (depende)   (no depende)
```

Las capas externas dependen de las internas, nunca al revés.

---

## Algoritmo Genético - Diseño

### Parámetros Configurables

```python
class GeneticAlgorithm:
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
    )
```

### Ciclo Evolutivo

1. **Inicialización**
   - Genera 40 individuos aleatorios
   - Respeta restricciones hard (área, agua, presupuesto)

2. **Selección por Torneo**
   - Selecciona k=3 individuos aleatorios
   - Retorna el mejor del torneo

3. **Cruza de Dos Puntos**
   - Probabilidad: 0.85
   - Divide layout en 3 secciones
   - Intercambia sección central

4. **Mutación por Intercambio**
   - Tasa: 0.08 (8% de genes)
   - Intercambia dos plantas aleatorias

5. **Evaluación de Fitness**
   - Calcula 4 métricas: CEE, PSNTPA, WCE, UE
   - Aplica pesos dinámicos según objetivo

6. **Reemplazo Elitista**
   - Preserva top 3 individuos
   - Selecciona mejores 37 de población + offspring

7. **Criterios de Parada**
   - Máximo 150 generaciones
   - Sin mejora en 20 generaciones
   - Varianza < 0.001

---

## Métricas de Fitness

### CEE: Compatibilidad Entre Especies

```python
CEE = Σ(w_dist · C(c,v)) / Σ(w_dist · C_max)
```

Donde:
- `w_dist = e^(-d/σ)` con `σ = 1.5`
- `C(c,v)`: Compatibilidad entre plantas c y v
- `C_max = 1.0`

### PSNTPA: Satisfacción Nutricional/Terapéutica

```python
PSNTPA = (production_factor + type_factor) / 2
```

Donde:
- `production_factor`: Producción normalizada
- `type_factor`: Porcentaje de plantas del tipo objetivo

### WCE: Eficiencia Hídrica

```python
WCE = 1 - (Agua_Total / Agua_Máxima)
```

### UE: Utilización de Espacio

```python
UE = Σ(q_p · a_p) / Área_Total
```

Con penalización si excede 0.85

---

## Patrones de Diseño Utilizados

### 1. Repository Pattern
- Abstracción de acceso a datos
- Interfaces en dominio, implementación en infraestructura

### 2. Dependency Injection
- Inyección de repositorios en casos de uso
- FastAPI Depends para controladores

### 3. Factory Pattern
- Creación de individuos en AG
- Transformación de entidades a DTOs

### 4. Strategy Pattern
- Pesos dinámicos según objetivo
- Diferentes estrategias de optimización

### 5. Singleton Pattern
- `MongoConnection` para conexión única a BD

---

## Escalabilidad

### Horizontal
- Microservicio stateless
- Múltiples instancias detrás de load balancer

### Vertical
- Optimización del AG con caching
- Paralelización de evaluación de fitness

### Futura
- Mensajería asíncrona (RabbitMQ/Kafka)
- Cache distribuido (Redis)
- Kubernetes para orquestación

---

## Seguridad

### Implementada
- ✅ Validación de entrada con Pydantic
- ✅ Autenticación MongoDB
- ✅ Usuario no-root en Docker
- ✅ CORS configurado

### Recomendada para Producción
- 🔒 API Key authentication
- 🔒 Rate limiting
- 🔒 HTTPS/TLS
- 🔒 Secrets management (Vault)

---

## Testing (Futuro)

### Unit Tests
```python
tests/
├── domain/
│   ├── test_plant.py
│   ├── test_garden_layout.py
│   └── test_genetic_algorithm.py
├── application/
│   └── test_generate_garden_use_case.py
└── infrastructure/
    ├── test_mongo_plant_repository.py
    └── test_mongo_compatibility_repository.py
```

### Integration Tests
```python
tests/integration/
├── test_api_endpoints.py
└── test_database_integration.py
```

### E2E Tests
```python
tests/e2e/
└── test_complete_workflow.py
```

---

## Monitoreo (Futuro)

### Métricas Sugeridas
- Tiempo de ejecución del AG
- Número de generaciones hasta convergencia
- Distribución de fitness scores
- Uso de recursos (CPU, memoria)

### Herramientas
- Prometheus + Grafana
- Sentry para errores
- ELK Stack para logs

---

## Referencias

- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- FastAPI Documentation
- MongoDB Best Practices
