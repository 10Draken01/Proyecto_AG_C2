"""
Punto de entrada principal del microservicio PlantGen API.
FastAPI application con arquitectura limpia.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.infrastructure.database.MongoConnection import MongoConnection
from src.infrastructure.api.controllers import router

# Cargar variables de entorno
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    Se ejecuta al inicio y al cierre.
    """
    # Startup
    print("🚀 Iniciando PlantGen API...")
    await MongoConnection.connect()
    yield
    # Shutdown
    print("🛑 Cerrando PlantGen API...")
    await MongoConnection.disconnect()


# Crear aplicación FastAPI
app = FastAPI(
    title="PlantGen API",
    description="""
    Sistema Inteligente para Optimización de Huertos Urbanos mediante Algoritmos Genéticos.

    ## Características
    - Algoritmo genético multi-objetivo
    - Optimización de 4 métricas: CEE, PSNTPA, WCE, UE
    - Base de 50 plantas adaptadas a clima tropical (Suchiapas, Chiapas)
    - Matriz de compatibilidad basada en agricultura asociativa
    - Arquitectura limpia y microservicios

    ## Endpoints
    - **GET /health**: Verificar estado del servicio
    - **POST /generate**: Generar configuraciones de huerto optimizadas
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "service": "PlantGen API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health",
        "generate": "/api/v1/generate"
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 3005))

    print(f"""
    ╔═══════════════════════════════════════════════════╗
    ║           PlantGen API - Microservicio            ║
    ║    Optimización de Huertos Urbanos con AG         ║
    ╠═══════════════════════════════════════════════════╣
    ║  Puerto: {port}                                      ║
    ║  Docs: http://localhost:{port}/docs                  ║
    ║  Health: http://localhost:{port}/api/v1/health       ║
    ╚═══════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
