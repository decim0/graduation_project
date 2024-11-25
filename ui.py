from PyQt6.QtWidgets import (QWidget, QDialog, QFormLayout, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
                             QGridLayout, QTextEdit, QListWidget,
                             QListWidgetItem, QDateTimeEdit,
                             QMessageBox, QDialogButtonBox)
from PyQt6.QtCore import Qt, QDateTime
from logic import (add_new_task,
                   get_all_tasks,
                   search_tasks,
                   complete_task,
                   update_task,
                   get_task_by_id)
from models import Task


class TaskManagerUI(QWidget):
    """Основной пользовательский интерфейс приложения
    Task Manager (наследуется от QWidget)."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setWindowFlags(self.windowFlags())

        title_label: QLabel = QLabel("Title:")
        self.title_edit: QLineEdit = QLineEdit()
        description_label: QLabel = QLabel("Description:")
        self.description_edit: QTextEdit = QTextEdit()
        priority_label: QLabel = QLabel("Priority:")
        self.priority_combo: QComboBox = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        deadline_label: QLabel = QLabel("Deadline:")
        self.deadline_edit: QDateTimeEdit = QDateTimeEdit(
            QDateTime.currentDateTime())
        self.deadline_edit.setCalendarPopup(True)
        tags_label: QLabel = QLabel("Tags:")
        self.tags_edit: QLineEdit = QLineEdit()
        add_button: QPushButton = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        sort_label: QLabel = QLabel("Sort by:")
        self.sort_field_combo: QComboBox = QComboBox()
        self.sort_field_combo.addItems(
            ["Title", "Status", "Priority", "Deadline"])
        self.sort_order_combo: QComboBox = QComboBox()
        self.sort_order_combo.addItems(["Ascending", "Descending"])
        priority_filter_label = QLabel("Filter by Priority:")
        self.priority_filter_combo = QComboBox()
        self.priority_filter_combo.addItems(["All", "Low", "Medium", "High"])

        add_layout: QGridLayout = QGridLayout()
        add_layout.addWidget(title_label, 0, 0)
        add_layout.addWidget(self.title_edit, 0, 1)
        add_layout.addWidget(description_label, 1, 0)
        add_layout.addWidget(self.description_edit, 1, 1)
        add_layout.addWidget(priority_label, 2, 0)
        add_layout.addWidget(self.priority_combo, 2, 1)
        add_layout.addWidget(deadline_label, 3, 0)
        add_layout.addWidget(self.deadline_edit, 3, 1)
        add_layout.addWidget(tags_label, 4, 0)
        add_layout.addWidget(self.tags_edit, 4, 1)
        add_layout.addWidget(add_button, 5, 1)

        self.task_list: QListWidget = QListWidget()
        self.task_list.itemClicked.connect(self.show_task_details)

        search_label: QLabel = QLabel("Search:")
        self.search_edit: QLineEdit = QLineEdit()
        search_button: QPushButton = QPushButton("Search")
        search_button.clicked.connect(self.search_tasks)

        search_layout: QHBoxLayout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_button)

        sort_layout: QHBoxLayout = QHBoxLayout()
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_field_combo)
        sort_layout.addWidget(self.sort_order_combo)

        priority_filter_layout = QHBoxLayout()
        priority_filter_layout.addWidget(priority_filter_label)
        priority_filter_layout.addWidget(self.priority_filter_combo)

        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addLayout(add_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(sort_layout)
        main_layout.addLayout(priority_filter_layout)
        main_layout.addWidget(self.task_list)
        self.setLayout(main_layout)
        self.update_task_list()
        self.sort_field_combo.currentIndexChanged.connect(
            self.update_task_list)
        self.sort_order_combo.currentIndexChanged.connect(
            self.update_task_list)
        self.priority_filter_combo.currentIndexChanged.connect(
            self.update_task_list)

    def add_task(self) -> None:
        """Добавление задачи и обновление списка задач."""
        title: str = self.title_edit.text()
        description: str = self.description_edit.toPlainText()
        priority: str = self.priority_combo.currentText()
        deadline: str = self.deadline_edit.dateTime().toString(
            "yyyy-MM-dd HH:mm:ss")
        tags: str = self.tags_edit.text()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите заголовок задачи!")
            return

        add_new_task(title, description, priority, deadline, tags)
        self.update_task_list()
        self.clear_input_fields()

    def clear_input_fields(self) -> None:
        """Очищает поля ввода для добавления новой задачи."""
        self.title_edit.clear()
        self.description_edit.clear()
        self.priority_combo.setCurrentIndex(0)
        self.deadline_edit.setDateTime(QDateTime.currentDateTime())
        self.tags_edit.clear()

    def update_task_list(self) -> None:
        """Обновление списка задач, отображаемых в UI."""
        sort_field = self.sort_field_combo.currentText().lower()
        sort_order = self.sort_order_combo.currentText().lower()
        priority_filter = self.priority_filter_combo.currentText()
        self.task_list.clear()
        tasks: list[Task] = get_all_tasks(
            sort_field, sort_order, priority_filter)
        for task in tasks:
            item_text: str = f"""Title: {task.title}
Status: {task.status}
Priority: {task.priority}
Tags: {task.tags if task.tags else "N/A"}"""
            item: QListWidgetItem = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, task.id)
            self.task_list.addItem(item)

    def search_tasks(self) -> None:
        """Выполняет поиск задач на основе поискового запроса
           и обновляет список задач."""
        search_term: str = self.search_edit.text()
        if search_term:
            tasks: list[Task] = search_tasks(search_term)
            self.update_task_list_from_tasks(tasks)
        else:
            self.update_task_list()

    def update_task_list_from_tasks(self, tasks: list[Task]) -> None:
        """Обновляет список задач определенным списком задач."""
        self.task_list.clear()
        for task in tasks:
            item_text: str = f"""Title: {task.title}
Status: {task.status}
Priority: {task.priority}
Tags: {task.tags if task.tags else "N/A"}"""
            item: QListWidgetItem = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, task.id)
            self.task_list.addItem(item)

    def show_task_details(self, item: QListWidgetItem) -> None:
        """Отображает подробную информацию о выбранной задаче и
           предоставляет опции для обновления или завершения."""
        task_id: int = item.data(Qt.ItemDataRole.UserRole)
        try:
            task: Task = get_task_by_id(task_id)
            details_dialog = TaskDetailsDialog(task)
            details_dialog.exec()
            self.update_task_list()
        except IndexError:
            QMessageBox.warning(self, "Ошибка", "Задача не найдена.")


class TaskDetailsDialog(QDialog):
    """Диалоговое окно для отображения сведений о задаче и предоставления
       параметров обновления/завершения."""

    def __init__(self, task: Task):
        super().__init__()
        self.setWindowTitle("Task Details")
        self.task_id: int = task.id
        self.task: Task = task
        self.layout: QVBoxLayout = QVBoxLayout()
        self.form: QFormLayout = QFormLayout()
        self.form.addRow(QLabel("Title:"), QLabel(task.title))
        self.form.addRow(QLabel("Description:"), QLabel(task.description))
        self.form.addRow(QLabel("Priority:"), QLabel(task.priority))
        self.form.addRow(QLabel("Deadline:"), QLabel(task.deadline))
        self.form.addRow(QLabel("Status:"), QLabel(task.status))
        self.form.addRow(QLabel("Tags:"), QLabel(task.tags))

        self.update_button: QPushButton = QPushButton("Update Task")
        self.update_button.clicked.connect(self.update_task)

        self.complete_button: QPushButton = QPushButton("Complete Task")
        self.complete_button.clicked.connect(self.complete_task)

        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close)
        self.button_box.rejected.connect(self.reject)

        self.layout.addLayout(self.form)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.complete_button)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def update_task(self) -> None:
        """Открывает диалоговое окно задачи обновления."""
        update_dialog: TaskUpdateDialog = TaskUpdateDialog(self.task)
        update_dialog.exec()
        self.accept()

    def complete_task(self) -> None:
        """Завершает задачу и закрывает диалоговое окно."""
        if complete_task(self.task_id):
            QMessageBox.information(
                self, "Успех", "Задача успешно выполнена!")
        else:
            QMessageBox.warning(
                self, "Ошибка", "Ошибка при завершении задачи.")
        self.accept()


class TaskUpdateDialog(QDialog):
    """Диалоговое окно для обновления сведений о задаче."""

    def __init__(self, task: Task):
        super().__init__()
        self.setWindowTitle("Update Task")
        self.task_id: int = task.id
        self.form: QFormLayout = QFormLayout()
        self.title_edit: QLineEdit = QLineEdit(task.title)
        self.description_edit: QTextEdit = QTextEdit(task.description)
        self.priority_combo: QComboBox = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setCurrentText(task.priority)
        self.deadline_edit: QDateTimeEdit = QDateTimeEdit(
            QDateTime.currentDateTime())
        self.deadline_edit.setCalendarPopup(True)
        self.tags_edit: QLineEdit = QLineEdit(task.tags)

        self.form.addRow(QLabel("Title:"), self.title_edit)
        self.form.addRow(QLabel("Description:"), self.description_edit)
        self.form.addRow(QLabel("Priority:"), self.priority_combo)
        self.form.addRow(QLabel("Deadline:"), self.deadline_edit)
        self.form.addRow(QLabel("Tags:"), self.tags_edit)

        self.button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.update)
        self.button_box.rejected.connect(self.reject)

        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.addLayout(self.form)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def update(self) -> None:
        """Обновляет задачу."""
        title: str = self.title_edit.text()
        description: str = self.description_edit.toPlainText()
        priority: str = self.priority_combo.currentText()
        deadline: str = self.deadline_edit.dateTime().toString("yyyy-MM-dd")
        tags: str = self.tags_edit.text()

        if update_task(self.task_id,
                       title,
                       description,
                       priority,
                       deadline,
                       tags):
            QMessageBox.information(
                self, "Успех", "Задача успешно обновлена!")
        else:
            QMessageBox.warning(
                self, "Ошибка", "Ошибка при обновлении задачи.")
        self.accept()
