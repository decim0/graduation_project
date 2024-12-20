from db import Database
from models import Task
from datetime import date, datetime


def add_new_task(title: str,
                 description: str,
                 priority: str,
                 deadline: str | date | None,
                 tags: str | None) -> int | None:
    """Добавляет новую задачу.

    Args:
        title: Заголовок.
        description: Описание.
        priority: Приоритет.
        deadline: Дедлайн.
        tags: Тэги.

    Returns:
        id добавлненной задачи.
    """
    db = Database()
    task_id = db.add_task(title, description, priority, deadline, tags)
    db.close()
    return task_id


def get_all_tasks(sort_field: str = None,
                  sort_order: str = None,
                  priority_filter: str = None) -> list:
    """Возвращает список всех задач.

    Args:
        filter_criteria: Критерии фильтра (по умол. None).

    Returns:
        Список всех задач.
    """
    db = Database()
    tasks_tuples = db.get_tasks(sort_field, sort_order, priority_filter)
    tasks = [Task.from_tuple(task_tuple) for task_tuple in tasks_tuples]
    db.close()
    return tasks


def get_task_by_id(task_id: int) -> Task | None:
    """Возвращает задачу по id."""
    db = Database()
    task_tuple = db.get_task_by_id(task_id)
    db.close()
    if task_tuple:
        return Task.from_tuple(task_tuple)
    else:
        return None


def search_tasks(search_criteria: str) -> list:
    """Ищет задачи по критериям.

    Args:
        search_criteria: Критерии поиска.

    Returns:
        Список задач.
    """
    db = Database()
    tasks_tuples = db.search_tasks(search_criteria)
    tasks = [Task.from_tuple(task_tuple) for task_tuple in tasks_tuples]
    db.close()
    return tasks


def complete_task(task_id: int,
                  completed_at: str | datetime | None = datetime.now()
                  ) -> bool:
    """Завершает задачу, обновляя её статус и дату завершения.

    Args:
        task_id: id задачи.
        completed_at: Дата завершения (по умол. datetime.now()).

    Returns:
        bool значение в зависимости от выполнения.
    """
    db = Database()
    success = db.update_task_status(task_id, "Completed", completed_at)
    db.close()
    return success


def update_task(task_id: int,
                title: str = None,
                description: str = None,
                priority: str = None,
                deadline: str | date | None = None,
                tags: str = None) -> bool:
    """Обновляет данные задачи.

    Args:
        task_id: id задачи.
        title: Заголовок (по умол. None).
        description: Описание (по умол. None).
        priority: Приоритет (по умол. None).
        deadline: Дедлайн (по умол. None).
        tags: Тэги (по умол. None).

    Returns:
        bool значение в зависимости от выполнения.
    """
    db = Database()
    success = db.update_task(
        task_id, title, description, priority, deadline, tags)
    db.close()
    return success
