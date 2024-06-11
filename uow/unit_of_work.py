from typing import Any
from uow.protocols.unit_of_work import UnitOfWorkProtocol
from uow.map_registry import MappersRegistry
from uow.object_state import ObjectState
from uow.object_store import ObjectStore


class UnitOfWork(UnitOfWorkProtocol):
    def __init__(self, registry: MappersRegistry) -> None:
        self._registry = registry
        self._object_store = ObjectStore()

    def register_new(self, entity: Any) -> None:
        if self._object_store.is_dirty(entity):
            raise ValueError(f"Entity {entity} is already registered as dirty")

        if self._object_store.is_removed(entity):
            raise ValueError(f"Entity {entity} is already registered as removed")

        if self._object_store.is_new(entity):
            raise ValueError(f"Entity {entity} is already registered as new")

        self._object_store.attach(entity, ObjectState.NEW)

    def register_dirty(self, entity: Any) -> None:
        if self._object_store.is_removed(entity):
            raise ValueError(f"Entity {entity} is already registered as removed")

        if self._object_store.is_dirty(entity) or self._object_store.is_new(entity):
            return None

        self._object_store.attach(entity, ObjectState.DIRTY)

    def register_removed(self, entity: Any) -> None:
        if self._object_store.is_new(entity):
            return self._object_store.detach(entity)

        if self._object_store.is_dirty(entity):
            self._object_store.detach(entity)

        if not self._object_store.is_removed(entity):
            self._object_store.attach(entity, ObjectState.REMOVED)

    def register_clean(self, entity: Any) -> None:
        self._object_store.attach(entity, ObjectState.CLEAN)

    def commit(self) -> None:
        for entity, state in self._object_store.items():
            mapper = self._registry.get(type(entity))
            if state == ObjectState.NEW:
                mapper.insert(entity)
            elif state == ObjectState.DIRTY:
                mapper.update(entity)
            elif state == ObjectState.REMOVED:
                mapper.delete(entity)

        self._object_store.clear()
