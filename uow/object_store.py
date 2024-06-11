from typing import Any

from uow.object_state import ObjectState


class ObjectStore(dict[Any, ObjectState]):
    def attach(self, entity: Any, state: ObjectState) -> None:
        return super().__setitem__(entity, state)

    def detach(self, entity: Any) -> None:
        return super().__delitem__(entity)

    def is_new(self, entity: Any) -> bool:
        if not super().__contains__(entity):
            return False

        return super().__getitem__(entity) == ObjectState.NEW

    def is_dirty(self, entity: Any) -> bool:
        if not super().__contains__(entity):
            return False

        return super().__getitem__(entity) == ObjectState.DIRTY

    def is_removed(self, entity: Any) -> bool:
        if not super().__contains__(entity):
            return False

        return super().__getitem__(entity) == ObjectState.REMOVED
