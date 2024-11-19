import sqlite3
from datetime import datetime, date


class Database:
    def __init__(self, db_name: str = "graduation_project.sqlite") -> None:
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        """Создает таблицу tasks в базе данных."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT NOT NULL CHECK (priority IN ('Low', 'Medium', 'High')),
                deadline DATETIME,
                status TEXT NOT NULL DEFAULT 'Open' CHECK (status IN ('Open', 'Completed')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                tags TEXT
            )
        """)

        self.conn.commit()

    def add_task(self,
                 title: str,
                 description: str,
                 priority: str,
                 deadline: str | date | None,
                 tags: str | None) -> int | None:
        try:
            deadline_obj = datetime.fromisoformat(
                deadline) if isinstance(deadline, str) else deadline
            self.cursor.execute("""
                INSERT INTO Tasks (title, description, priority, deadline, tags)
                VALUES (?, ?, ?, ?, ?)
            """, (title, description, priority, deadline_obj, tags))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении задачи: {e}")
            return None

    def get_tasks(self, filter_criteria: dict | None = None) -> list:
        query: str = "SELECT * FROM tasks"
        if filter_criteria:
            where_clause = " WHERE " + \
                " AND ".join([f"{k} = ?" for k in filter_criteria])
            query += where_clause
            parameters = list(filter_criteria.values())
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_task(self,
                    task_id: int,
                    title: str = None,
                    description: str = None,
                    priority: str = None,
                    deadline: str | date | None = None,
                    tags: str = None) -> bool:
        try:
            set_clause = []
            parameters = []

            if title is not None:
                set_clause.append("title = ?")
                parameters.append(title)
            if description is not None:
                set_clause.append("description = ?")
                parameters.append(description)
            if priority is not None:
                set_clause.append("priority = ?")
                parameters.append(priority)
            if deadline is not None:
                deadline_obj = datetime.fromisoformat(
                    deadline) if isinstance(deadline, str) else deadline
                set_clause.append("deadline = ?")
                parameters.append(deadline_obj)
            if tags is not None:
                set_clause.append("tags = ?")
                parameters.append(tags)

            if not set_clause:
                return True

            set_str = ", ".join(set_clause)
            query = f"UPDATE Tasks SET {set_str} WHERE id = ?"
            parameters.append(task_id)

            self.cursor.execute(query, parameters)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка обновления задачи: {e}")
            return False

    def update_task_status(self,
                           task_id: int,
                           status: str,
                           completed_at: str | datetime | None) -> bool:
        try:
            completed_at_obj = datetime.fromisoformat(
                completed_at) if isinstance(completed_at, str) else completed_at
            self.cursor.execute("""
                UPDATE Tasks SET status = ?, completed_at = ? WHERE id = ?
            """, (status, completed_at_obj, task_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении задачи: {e}")
            return False

    def close(self) -> None:
        self.conn.close()
