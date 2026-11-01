from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
RUTA_BD = Path(__file__).resolve().parent.parent / "biblioteca.db"


# SQLite no controla las claves foráneas si no se lo pedimos en cada conexión
@event.listens_for(Engine, "connect")
def _activar_claves_foraneas(conexion, registro):
    conexion.execute("PRAGMA foreign_keys = ON")


class ConexionBD:
    """Singleton: guarda el único Engine y la fábrica de sesiones del sistema.

    Cada caso de uso abre su propia sesión: compartir una sola entre pantallas
    mezclaría transacciones.
    """

    _instancia = None
    _ruta = RUTA_BD

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._engine = create_engine(f"sqlite:///{cls._ruta}")
            cls._instancia._Session = sessionmaker(bind=cls._instancia._engine, expire_on_commit=False)
        return cls._instancia

    @classmethod
    def reiniciar(cls, ruta=RUTA_BD):
        """Descarta la instancia actual. Lo usan los tests para trabajar sobre otra base."""
        if cls._instancia is not None:
            cls._instancia._engine.dispose()
        cls._instancia = None
        cls._ruta = ruta

    @property
    def engine(self):
        return self._engine

    def crear_tablas(self):
        import Entidades  # Registra todas las tablas en Base.metadata
        Base.metadata.create_all(self._engine)

    @contextmanager
    def obtener_session(self):
        session = self._Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
