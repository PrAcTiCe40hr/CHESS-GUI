from PyQt5.QtCore import QThread, pyqtSignal
import chess.engine


class StockfishThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, board, engine, engine_time):
        QThread.__init__(self)
        self.board = board
        self.engine = engine
        self.engine_time = engine_time

    def run(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=self.engine_time))
        self.signal.emit(result)
