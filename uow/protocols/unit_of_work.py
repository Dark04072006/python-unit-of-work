from typing import Any, Protocol


class UnitOfWorkProtocol(Protocol):
    def register_new(self, entity: Any) -> None:
        raise NotImplementedError

    def register_dirty(self, entity: Any) -> None:
        raise NotImplementedError

    def register_removed(self, entity: Any) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError
