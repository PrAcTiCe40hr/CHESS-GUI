import sys
from PyQt5.QtWidgets import QApplication
from src.chess_gui import ChessGui


def main():
    app = QApplication(sys.argv)
    gui = ChessGui()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()