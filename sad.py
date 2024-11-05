import pytest
import sqlite3 as sq


class TestDataBase:

    @pytest.fixture
    def db_connection(self):
        conn = sq.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        conn.commit()
        yield conn
        conn.close()

    def test_add_user(self, db_connection):
        self._add_user(db_connection, 'Alice', 25)
        result = self._fetch_user(db_connection, 'Alice')
        assert result is not None

    def test_update_user_age(self, db_connection):
        self._add_user(db_connection, 'David', 40)
        self._update_user_age(db_connection, 'David', 41)
        result = self._fetch_user_age(db_connection, 'David')
        assert result == 41

    def _add_user(self, conn, name, age):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()

    def _update_user_age(self, conn, name, new_age):
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET age = ? WHERE name = ?", (new_age, name))
        conn.commit()

    def _fetch_user(self, conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return cursor.fetchone()

    def _fetch_user_age(self, conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM users WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None


