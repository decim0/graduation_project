import sqlite3
from datetime import datetime, date


class Database:
    """Класс для работы с базой данных SQLite."""

    def __init__(self, db_name: str = "graduation_project.sqlite") -> None:
        """Инициализация объекта Database.

        Args:
            db_name: Название БД (по умол. "graduation_project.sqlite").
        """
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
                priority TEXT NOT NULL
                    CHECK (priority IN ('Low', 'Medium', 'High')),
                deadline DATETIME,
                status TEXT NOT NULL DEFAULT 'Open' CHECK
                    (status IN ('Open', 'Completed')),
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
        """Добавляет новую задачу.

        Args:
            title: Название.
            description: Описание.
            priority: Приоритет.
            deadline: Дедлайн (по умол. None).
            tags: Тэги (по умол. None).
        """
        try:
            deadline_obj = datetime.fromisoformat(
                deadline) if isinstance(deadline, str) else deadline
            self.cursor.execute("""
                INSERT INTO Tasks
                    (title, description, priority, deadline, tags)
                VALUES (?, ?, ?, ?, ?)
            """, (title, description, priority, deadline_obj, tags))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении задачи: {e}")
            return None

    def get_tasks(self,
                  sort_field: str = None,
                  sort_order: str = None,
                  priority_filter: str = None) -> list:
        """Возвращает список задач, подходящих под фильтр.

        Args:
            filter_criteria: Критерии фильтра (по умол. None).
            query: Запрос.

        Returns:
            Список задач.
        """
        query: str = "SELECT * FROM tasks"
        where_clause = []
        parameters = []

        if priority_filter != "All":
            where_clause.append("priority = ?")
            parameters.append(priority_filter)

        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        if sort_field:
            order = "ASC" if sort_order == "ascending" else "DESC"
            query += f" ORDER BY {sort_field} {order}"

        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def search_tasks(self, search_criteria: dict) -> list:
        """Ищет задачи по заданным критериям.

        Args:
            search_criteria: Критерии поиска.
            query: Запрос.
            clauses: Условия.
            parameters: Параметры.

        Returns:
            Список задач.
        """
        query: str = "SELECT * FROM tasks WHERE "
        clauses: list = []
        parameters: list = []

        for column, value in search_criteria.items():
            if column == "title":
                words = value.split()
                for word in words:
                    clauses.append(f"{column} LIKE ?")
                    parameters.append(f"%{word}%")
            else:
                clauses.append(f"{column} = ?")
                parameters.append(value)

        query += " AND ".join(clauses)
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def update_task(self,
                    task_id: int,
                    title: str = None,
                    description: str = None,
                    priority: str = None,
                    deadline: str | date | None = None,
                    tags: str = None) -> bool:
        """Обновляет данные задачи.

        Args:
            task_id: id задачи.
            title: Название (по умол. None).
            description: Описание (по умол. None).
            priority: Приоритет (по умол. None).
            deadline: Дедлайн (по умол. None).
            tags: Тэги (по умол. None).
            set_clause: Условия.
            parameters: Параметры.

        Returns:
            bool значение в зависимости от выполнения.
        """
        try:
            set_clause: list = []
            parameters: list = []

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
        """Обновляет статус задачи.

        Args:
            task_id: id задачи.
            status: Статус.
            completed_at: Дата выполнения.

        Returns:
            bool значение в зависимости от выполнения.
        """
        try:
            completed_at_obj = datetime.fromisoformat(
                completed_at) if isinstance(
                completed_at, str) else completed_at
            self.cursor.execute("""
                UPDATE Tasks SET status = ?, completed_at = ? WHERE id = ?
            """, (status, completed_at_obj, task_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении задачи: {e}")
            return False

    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()
