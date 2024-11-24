import sys
from PyQt6.QtWidgets import QApplication
from ui import TaskManagerUI

if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    ui: TaskManagerUI = TaskManagerUI()
    ui.show()
    app.exec()
