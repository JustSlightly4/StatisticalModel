import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import LogicFunctions
import DrawingFunctions

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrawingFunctions.MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
