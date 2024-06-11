import logging
from sqlite3 import Connection
from app.domain import Comment, Post
from uow.protocols.mapper import DataMapperProtocol

logger = logging.getLogger(__name__)


class PostMapper(DataMapperProtocol[Post]):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def insert(self, entity: Post) -> None:
        self.connection.execute("INSERT INTO posts (title) VALUES (?)", (entity.title,))
        logger.info(f"Inserted new post with ID {entity.id}")

    def update(self, entity: Post) -> None:
        self.connection.execute(
            "UPDATE posts SET title = ? WHERE id = ?", (entity.title, entity.id)
        )
        logger.info(f"Updated post with ID {entity.id}")

    def delete(self, entity: Post) -> None:
        self.connection.execute("DELETE FROM posts WHERE id = ?", (entity.id,))
        logger.info(f"Deleted post with ID {entity.id}")

    def find_by_id(self, post_id: int) -> Post:
        cursor = self.connection.execute(
            "SELECT id, title FROM posts WHERE id = ?", (post_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"No post found with id {post_id}")

        post = Post(*row)
        logger.info(f"Retrieved post with ID {post_id}")
        return post

    def exists(self, post_id: int) -> bool:
        cursor = self.connection.execute("SELECT 1 FROM posts WHERE id = ?", (post_id,))
        exists = cursor.fetchone() is not None
        logger.info(f"Checked existence of post with ID {post_id}: {exists}")
        return exists


class CommentMapper(DataMapperProtocol[Comment]):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def insert(self, entity: Comment) -> None:
        self.connection.execute(
            "INSERT INTO comments (text, post_id) VALUES (?, ?)",
            (entity.text, entity.post_id),
        )
        logger.info(f"Inserted new comment with ID {entity.id}")

    def update(self, entity: Comment) -> None:
        self.connection.execute(
            "UPDATE comments SET text = ? WHERE id = ?", (entity.text, entity.id)
        )
        logger.info(f"Updated comment with ID {entity.id}")

    def delete(self, entity: Comment) -> None:
        self.connection.execute("DELETE FROM comments WHERE id = ?", (entity.id,))
        logger.info(f"Deleted comment with ID {entity.id}")

    def find_by_id(self, comment_id: int) -> Comment:
        cursor = self.connection.execute(
            "SELECT id, text, post_id FROM comments WHERE id = ?", (comment_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"No comment found with id {comment_id}")

        comment = Comment(*row)
        logger.info(f"Retrieved comment with ID {comment_id}")
        return comment

    def find_by_post_id(self, post_id: int) -> list[Comment]:
        cursor = self.connection.execute(
            "SELECT id, text, post_id FROM comments WHERE post_id = ?", (post_id,)
        )
        comments = [Comment(*row) for row in cursor.fetchall()]
        logger.info(f"Retrieved comments for post with ID {post_id}")
        return comments

    def exists(self, comment_id: int) -> bool:
        cursor = self.connection.execute(
            "SELECT 1 FROM comments WHERE id = ?", (comment_id,)
        )
        exists = cursor.fetchone() is not None
        logger.info(f"Checked existence of comment with ID {comment_id}: {exists}")
        return exists
