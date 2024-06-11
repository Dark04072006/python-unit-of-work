from dataclasses import dataclass, field


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
    comments: list[Comment] = field(default_factory=list)

    def load_comments(self, comments: list[Comment]) -> None:
        self.comments = comments

    def drop_comments(self) -> None:
        self.comments.clear()

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def remove_comment(self, comment: Comment) -> None:
        self.comments.remove(comment)

    def __hash__(self) -> int:
        return self.id
