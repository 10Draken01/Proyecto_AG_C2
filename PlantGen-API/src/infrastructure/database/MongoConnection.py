"""
Conexión a MongoDB con autenticación.
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoConnection:
    """
    Singleton para manejar la conexión a MongoDB.
    """
    _client: AsyncIOMotorClient = None
    _database: AsyncIOMotorDatabase = None

    @classmethod
    async def get_database(cls) -> AsyncIOMotorDatabase:
        """
        Obtiene la instancia de la base de datos MongoDB.

        Returns:
            Base de datos MongoDB
        """
        if cls._database is None:
            await cls.connect()
        return cls._database

    @classmethod
    async def connect(cls):
        """
        Establece conexión con MongoDB usando credenciales del .env
        """
        # Leer variables de entorno
        mongo_user = os.getenv("MONGO_ROOT_USER", "admin")
        mongo_password = os.getenv("MONGO_ROOT_PASSWORD", "TuPassword123!")
        mongo_host = os.getenv("MONGO_HOST", "localhost")
        mongo_port = os.getenv("MONGO_PORT", "27017")
        mongo_db = os.getenv("MONGO_DATABASE", "Data_plants")

        # Construir URI de conexión
        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"

        try:
            # Crear cliente
            cls._client = AsyncIOMotorClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000
            )

            # Verificar conexión
            await cls._client.admin.command('ping')
            print(f"✓ Conectado exitosamente a MongoDB: {mongo_db}")

            # Obtener base de datos
            cls._database = cls._client[mongo_db]

        except Exception as e:
            print(f"✗ Error al conectar a MongoDB: {e}")
            raise

    @classmethod
    async def disconnect(cls):
        """Cierra la conexión a MongoDB"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._database = None
            print("✓ Desconectado de MongoDB")

    @classmethod
    async def health_check(cls) -> bool:
        """
        Verifica el estado de la conexión.

        Returns:
            True si la conexión está activa
        """
        try:
            if cls._client is None:
                return False
            await cls._client.admin.command('ping')
            return True
        except Exception:
            return False
