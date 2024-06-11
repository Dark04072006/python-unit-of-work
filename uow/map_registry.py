from uow.protocols.mapper import _EntityT, DataMapperProtocol


class MappersRegistry(dict):
    def get(self, __key: type[_EntityT]) -> DataMapperProtocol[_EntityT]:
        mapper = super().get(__key)

        if mapper is None:
            raise KeyError(f"Mapper for {__key} not registered")

        return mapper

    def register(
        self, entity: type[_EntityT], mapper: DataMapperProtocol[_EntityT]
    ) -> None:
        return super().__setitem__(entity, mapper)

    def unregister(self, entity: type[_EntityT]) -> None:
        return super().__delitem__(entity)
