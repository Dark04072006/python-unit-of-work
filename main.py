from dataclasses import dataclass, field
from typing import List

from uow.protocols.unit_of_work import UnitOfWorkProtocol
from uow.unit_of_work import UnitOfWork
from uow.protocols.mapper import DataMapperProtocol
from uow.map_registry import MappersRegistry


@dataclass
class Comment:
    id: int
    text: str
    post_id: int

    def __hash__(self) -> int:
        return self.id


@dataclass
class Post:
    id: int
    title: str
    comments: List[Comment] = field(default_factory=list)

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def remove_comment(self, comment: Comment) -> None:
        self.comments.remove(comment)

    def __hash__(self) -> int:
        return self.id


class PostMapper(DataMapperProtocol[Post]):
    def insert(self, entity: Post) -> None:
        print(f"Inserting post {entity}")

    def update(self, entity: Post) -> None:
        print(f"Updating post {entity}")

    def delete(self, entity: Post) -> None:
        print(f"Deleting post {entity}")

    def find_by_id(self, post_id: int) -> Post:
        print(f"Fetching post with id {post_id}")
        return Post(id=post_id, title="Mocked Post")


class CommentMapper(DataMapperProtocol[Comment]):
    def insert(self, entity: Comment) -> None:
        print(f"Inserting comment {entity}")

    def update(self, entity: Comment) -> None:
        print(f"Updating comment {entity}")

    def delete(self, entity: Comment) -> None:
        print(f"Deleting comment {entity}")

    def find_by_id(self, comment_id: int) -> Comment:
        print(f"Fetching comment with id {comment_id}")
        return Comment(id=comment_id, text="Mocked Comment", post_id=1)


class PostGateway:
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        post_mapper: PostMapper,
        comment_mapper: CommentMapper,
    ) -> None:
        self._uow = uow
        self._post_mapper = post_mapper
        self._comment_mapper = comment_mapper

    def get_post(self, post_id: int) -> Post:
        return self._post_mapper.find_by_id(post_id)

    def save_post(self, post: Post) -> None:
        if self._is_new_post(post):
            self._uow.register_new(post)
        else:
            self._uow.register_dirty(post)
        for comment in post.comments:
            if self._is_new_comment(comment):
                self._uow.register_new(comment)
            else:
                self._uow.register_dirty(comment)

    def delete_post(self, post: Post) -> None:
        self._uow.register_removed(post)
        for comment in post.comments:
            self._uow.register_removed(comment)

    def _is_new_post(self, post: Post) -> bool:
        return post.id == 0

    def _is_new_comment(self, comment: Comment) -> bool:
        return comment.id == 0


def main() -> None:
    post_mapper = PostMapper()
    comment_mapper = CommentMapper()

    registry = MappersRegistry()
    registry.register(Post, post_mapper)
    registry.register(Comment, comment_mapper)

    uow = UnitOfWork(registry=registry)

    post_gateway = PostGateway(
        uow=uow, post_mapper=post_mapper, comment_mapper=comment_mapper
    )

    # Example of creating and saving a new post
    new_post = Post(id=0, title="New Post")
    new_comment = Comment(id=0, text="New Comment", post_id=0)
    new_post.add_comment(new_comment)
    post_gateway.save_post(new_post)

    # Example of updating an existing post
    existing_post = post_gateway.get_post(post_id=1)
    existing_post.add_comment(Comment(id=0, text="Another Comment", post_id=1))
    post_gateway.save_post(existing_post)

    # Example of deleting a post
    post_to_delete = post_gateway.get_post(post_id=1)
    post_gateway.delete_post(post_to_delete)
    uow.commit()


if __name__ == "__main__":
    main()
