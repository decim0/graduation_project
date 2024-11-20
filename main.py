from logic import add_new_task, get_all_tasks, search_tasks, complete_task, update_task


if __name__ == "__main__":
    # add_new_task("Пойти в магазин", "Купить молоко и хлеб",
    #              "Medium", "2024-03-15", "Покупки")
    tasks = get_all_tasks()
    for task in tasks:
        print(f"{task.title}, {task.description}")
