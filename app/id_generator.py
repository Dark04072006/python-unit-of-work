from sqlite3 import Connection


class IdGenerator:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def generate_new_post_id(self) -> int:
        cursor = self._connection.execute("SELECT id FROM posts")

        if cursor.lastrowid is None:
            return 1

        return cursor.lastrowid + 1

    def generate_new_comment_id(self) -> int:
        cursor = self._connection.execute("SELECT id FROM comments")

        if cursor.lastrowid is None:
            return 1

        return cursor.lastrowid + 1
