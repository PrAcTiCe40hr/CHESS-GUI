import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from src.chess_gui import ChessGui


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon\\chess.svg"))
    gui = ChessGui()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
