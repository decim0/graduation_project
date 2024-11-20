from datetime import datetime


class Task:
    """Класс представляет собой задачу."""

    def __init__(self,
                 id: int,
                 title: str,
                 description: str,
                 priority: str,
                 deadline: datetime | None,
                 status: str,
                 created_at: datetime,
                 completed_at: datetime | None,
                 tags: str | None) -> None:
        """Инициализация объекта Task.

        Args:
            id: id задачи.
            title: Заголовок.
            description : Описание.
            priority: Приоритет.
            deadline: Дедлайн.
            status : Статус.
            created_at: Дата создания.
            completed_at: Дата завершения.
            tags: Тэги.
        """
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = status
        self.created_at = created_at
        self.completed_at = completed_at
        self.tags = tags

    @classmethod
    def from_tuple(cls, task_tuple: tuple) -> "Task":
        """Создает объект Task из кортежа данных.

        Args:
            task_tuple: Кортеж данных.

        Returns:
            Объект Task из кортежа данных.
        """
        return cls(*task_tuple)
