from dataclasses import dataclass, field

from uow.protocols.unit_of_work import UnitOfWorkProtocol
from uow.unit_of_work import UnitOfWork
from uow.protocols.mapper import DataMapperProtocol
from uow.map_registry import MappersRegistry


@dataclass
class User:
    id: int
    name: str
    posts: list[str] = field(default_factory=list)

    def add_post(self, post: str) -> None:
        self.posts.append(post)

    def remove_post(self, post: str) -> None:
        self.posts.remove(post)

    def __hash__(self) -> int:
        return self.id


class UserMapper(DataMapperProtocol[User]):
    def insert(self, _entity: User) -> None:
        print(f"Inserting user {_entity}")

    def update(self, _entity: User) -> None:
        print(f"Updating user {_entity}")

    def delete(self, _entity: User) -> None:
        print(f"Deleting user {_entity}")

    def find_by_id(self, user_id: int) -> User:
        # This should return a user object from the database
        # Here we are just mocking this part for simplicity
        print(f"Fetching user with id {user_id}")
        return User(id=user_id, name="Mocked User")


class UserGateway:
    def __init__(self, uow: UnitOfWorkProtocol, mapper: UserMapper) -> None:
        self._uow = uow
        self._mapper = mapper

    def get_user(self, user_id: int) -> User:
        user = self._mapper.find_by_id(user_id)
        return user

    def save_user(self, user: User) -> None:
        if self._is_new_user(user):
            self._uow.register_new(user)
        else:
            self._uow.register_dirty(user)

    def delete_user(self, user: User) -> None:
        self._uow.register_removed(user)

    def _is_new_user(self, user: User) -> bool:
        # This should check if the user exists in the database
        # For now, we are assuming user is new if ID is 0 (for simplicity)
        return user.id == 0


def main() -> None:
    user_mapper = UserMapper()

    registry = MappersRegistry()
    registry.register(User, user_mapper)

    uow = UnitOfWork(registry=registry)

    user_gateway = UserGateway(uow=uow, mapper=user_mapper)

    # Example of creating and saving a new user
    new_user = User(id=0, name="New User")
    user_gateway.save_user(new_user)
    uow.commit()

    # Example of updating an existing user
    existing_user = user_gateway.get_user(user_id=1)
    existing_user.add_post("New Post")
    user_gateway.save_user(existing_user)
    uow.commit()

    # Example of deleting a user
    user_to_delete = user_gateway.get_user(user_id=1)
    user_gateway.delete_user(user_to_delete)
    uow.commit()


if __name__ == "__main__":
    main()
