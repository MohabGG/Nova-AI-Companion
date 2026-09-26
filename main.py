
import sys

from PySide6.QtWidgets import QApplication
from app.window import CompanionWindow


def main():
    application = QApplication(sys.argv)

    window = CompanionWindow()
    window.show()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
