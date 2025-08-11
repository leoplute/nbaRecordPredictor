from PySide6.QtWidgets import QApplication
import sys

from model import FantasyModel
from view import FantasyView
from controller import FantasyController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create MVC parts
    model = FantasyModel()
    view = FantasyView()
    controller = FantasyController(model, view)

    # Show UI
    view.show()

    sys.exit(app.exec())
