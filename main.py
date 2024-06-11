import logging
import sqlite3
from app.domain import Comment, Post
from app.id_generator import IdGenerator
from app.interactor import CreatePost, CreateComment, DeletePost
from app.mappers import CommentMapper, PostMapper
from app.repository import PostRepository
from app.uow import SqliteUnitOfWork
from uow.map_registry import MappersRegistry

logging.basicConfig(level=logging.INFO)


def create_post_run(interactor: CreatePost) -> None:
    titles = [
        "First post",
        "Second post",
        "Third post",
        "Fourth post",
        "Fifth post",
        "Sixth post",
        "Seventh post",
        "Eighth post",
        "Ninth post",
        "Tenth post",
    ]

    for title in titles:
        interactor(title)


def create_comment_run(interactor: CreateComment) -> None:
    post_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    texts = [
        "First comment",
        "Second comment",
        "Third comment",
        "Fourth comment",
        "Fifth comment",
        "Sixth comment",
        "Seventh comment",
        "Eighth comment",
        "Ninth comment",
        "Tenth comment",
    ]

    for post_id, text in zip(post_ids, texts):
        interactor(post_id, text)


def delete_post_run(interactor: DeletePost) -> None:
    post_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for post_id in post_ids:
        interactor(post_id)


def main() -> None:
    with sqlite3.connect("sql/posts.sqlite3", isolation_level=None) as connection:
        with open("sql/schema.sql") as f:
            connection.executescript(f.read())
            connection.commit()

        post_mapper = PostMapper(connection)
        comment_mapper = CommentMapper(connection)

        mappers_registry = MappersRegistry()
        mappers_registry.register(Post, post_mapper)
        mappers_registry.register(Comment, comment_mapper)

        uow = SqliteUnitOfWork(connection, mappers_registry)

        post_repository = PostRepository(uow, post_mapper, comment_mapper)
        id_generator = IdGenerator(connection)

        create_post = CreatePost(uow, post_repository, id_generator)

        create_comment = CreateComment(uow, post_repository, id_generator)

        delete_post = DeletePost(uow, post_repository)

        create_post_run(create_post)
        create_comment_run(create_comment)
        delete_post_run(delete_post)


if __name__ == "__main__":
    main()
