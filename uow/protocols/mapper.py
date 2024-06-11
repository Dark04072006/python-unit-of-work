from typing import Protocol, TypeVar


_EntityT = TypeVar("_EntityT")


class DataMapperProtocol(Protocol[_EntityT]):
    def insert(self, _entity: _EntityT) -> None:
        raise NotImplementedError

    def update(self, _entity: _EntityT) -> None:
        raise NotImplementedError

    def delete(self, _entity: _EntityT) -> None:
        raise NotImplementedError
