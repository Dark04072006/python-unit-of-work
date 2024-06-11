from sqlite3 import Connection
from uow.map_registry import MappersRegistry
from uow.unit_of_work import UnitOfWork


class SqliteUnitOfWork(UnitOfWork):
    def __init__(self, connection: Connection, registry: MappersRegistry) -> None:
        super().__init__(registry)
        self._connection = connection

    def commit(self) -> None:
        self._connection.execute("BEGIN")

        try:
            super().commit()

        except Exception:
            self._connection.execute("ROLLBACK")
            raise

        self._connection.execute("COMMIT")
