from typing import Union
from flask import request
from datetime import datetime

from app.database import get_db_connection


class User:
    def __init__(self, username: Union[str, None], admin: bool):
        self.__username = username
        self.__admin = admin

    @property
    def username(self) -> Union[str, None]:
        return self.__username

    @property
    def admin(self) -> bool:
        return self.__admin


def get_user() -> Union[User, None]:
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        return None

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    sessions.username, expiration, admin
                FROM
                    sessions JOIN users ON sessions.username = users.username
                WHERE
                    session_id = %s
                ORDER BY
                    expiration DESC LIMIT 1
                """, (session_id,)
            )
            result = cur.fetchone()
            cur.close()

            if result is None:
                return None

            username, expiration, admin = result

            if expiration < datetime.now():
                return None

            return User(username, admin)
