import logging
from app.domain import Comment, Post
from app.id_generator import IdGenerator
from app.repository import PostRepository
from uow.protocols.unit_of_work import UnitOfWorkProtocol

logger = logging.getLogger(__name__)


class CreatePost:
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        repository: PostRepository,
        id_generator: IdGenerator,
    ) -> None:
        self._uow = uow
        self._repository = repository
        self._id_generator = id_generator

    def __call__(self, title: str) -> None:
        post_id = self._id_generator.generate_new_post_id()
        new_post = Post(post_id, title)

        self._repository.save_post(new_post)
        self._uow.commit()
        logger.info(f"Created new post with ID {post_id}")


class CreateComment:
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        repository: PostRepository,
        id_generator: IdGenerator,
    ) -> None:
        self._uow = uow
        self._repository = repository
        self._id_generator = id_generator

    def __call__(self, post_id: int, text: str) -> None:
        post = self._repository.load_post(post_id)

        comment_id = self._id_generator.generate_new_comment_id()
        new_comment = Comment(comment_id, text, post_id)

        post.add_comment(new_comment)
        self._repository.save_post(post)
        self._uow.commit()
        logger.info(
            f"Created new comment with ID {comment_id} for post with ID {post_id}"
        )


class DeletePost:
    def __init__(self, uow: UnitOfWorkProtocol, repository: PostRepository) -> None:
        self._uow = uow
        self._repository = repository

    def __call__(self, post_id: int) -> None:
        post = self._repository.load_post(post_id)
        self._repository.delete_post(post)
        self._uow.commit()
        logger.info(f"Deleted post with ID {post_id}")
