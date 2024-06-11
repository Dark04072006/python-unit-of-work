import logging
from app.domain import Post
from app.mappers import CommentMapper, PostMapper
from uow.protocols.unit_of_work import UnitOfWorkProtocol

logger = logging.getLogger(__name__)


class PostRepository:
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        post_mapper: PostMapper,
        comment_mapper: CommentMapper,
    ) -> None:
        self._uow = uow
        self._post_mapper = post_mapper
        self._comment_mapper = comment_mapper

    def load_post(self, post_id: int) -> Post:
        post = self._post_mapper.find_by_id(post_id)
        comments = self._comment_mapper.find_by_post_id(post_id)
        post.load_comments(comments)
        logger.info(f"Loaded post with ID {post_id}")
        return post

    def save_post(self, post: Post) -> None:
        if self._post_mapper.exists(post.id):
            self._uow.register_dirty(post)
            logger.info(f"Registered dirty post with ID {post.id}")
        else:
            self._uow.register_new(post)
            logger.info(f"Registered new post with ID {post.id}")

        for comment in post.comments:
            if not self._comment_mapper.exists(comment.id):
                self._uow.register_new(comment)
                logger.info(
                    f"Registered new comment with ID {comment.id} for post with ID {post.id}"
                )

    def delete_post(self, post: Post) -> None:
        self._uow.register_removed(post)
        logger.info(f"Registered removal of post with ID {post.id}")

        for comment in post.comments:
            self._uow.register_removed(comment)
            logger.info(
                f"Registered removal of comment with ID {comment.id} for post with ID {post.id}"
            )

        post.drop_comments()
        logger.info(f"Dropped comments for post with ID {post.id}")
