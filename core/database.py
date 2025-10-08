import sqlite3


class Database:
    def __init__(self, db_name=":memory:"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.initialize_db()

    def initialize_db(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY,
                clan_tag TEXT
            )
        """
        )
        self.connection.commit()

    def add_server(self, id, clan_tag):
        self.cursor.execute(
            "INSERT INTO servers (id, clan_tag) VALUES (?, ?)",
            (id, clan_tag),
        )
        self.connection.commit()

    # def add_user(self, id, player_tag, clan_tag):
    #     self.cursor.execute(
    #         "INSERT INTO users (id, player_tag, clan_tag) VALUES (?, ?, ?)",
    #         (id, player_tag, clan_tag),
    #     )
    #     self.connection.commit()

    def get_server(self, id) -> tuple | None:
        self.cursor.execute("SELECT * FROM servers WHERE id = ?", (id,))
        return self.cursor.fetchone()

    # def get_user(self, id) -> tuple | None:
    #     self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    #     return self.cursor.fetchone()

    def update_clan_tag(self, id, clan_tag) -> None:
        self.cursor.execute(
            "UPDATE servers SET clan_tag = ? WHERE id = ?",
            (clan_tag, id),
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
