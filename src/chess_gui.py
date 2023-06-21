from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QSlider, QListWidget, QListWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import chess.engine

from src.svg_button import SvgButton
from src.stockfish_thread import StockfishThread


class ChessGui(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("style\\style.qss", "r") as file:
            self.setStyleSheet(file.read())

        self.board = chess.Board()
        self.selected_piece = None
        self.buttons = []
        self.rank_labels = []
        self.file_labels = []
        self.engine_time = 2.0
        self.move_history = None
        self.current_move_index = 0

        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish\\stockfish-windows-2022-x86-64-avx2.exe")
        # Create time slider
        self.time_slider = QSlider(Qt.Horizontal, self)
        self.time_slider.setGeometry(275, 10, 150, 30)
        self.time_slider.setMinimum(1)
        self.time_slider.setMaximum(10)
        self.time_slider.setValue(2)  # Default value
        self.time_slider.valueChanged.connect(self.update_time)

        self.time_label = QLabel('Engine Time: 2s', self)
        self.time_label.setGeometry(440, 10, 100, 30)

        # Create skill slider
        self.skill_slider = QSlider(Qt.Horizontal, self)
        self.skill_slider.setGeometry(550, 10, 150, 30)
        self.skill_slider.setMinimum(0)
        self.skill_slider.setMaximum(20)
        self.skill_slider.setValue(10)  # Default value
        self.skill_slider.valueChanged.connect(self.update_skill)

        self.skill_label = QLabel('Engine Skill: 10', self)
        self.skill_label.setGeometry(715, 10, 100, 30)

        self.reset_button = QPushButton('Reset Game', self)
        self.reset_button.setGeometry(850, 10, 200, 30)  # Adjusted position
        self.reset_button.clicked.connect(self.reset_game)

        # Create export button
        self.export_button = QPushButton('Export Game', self)
        self.export_button.setGeometry(50, 10, 100, 30)
        self.export_button.clicked.connect(self.export_game)

        # Create import button
        self.import_button = QPushButton('Import Game', self)
        self.import_button.setGeometry(150, 10, 100, 30)
        self.import_button.clicked.connect(self.import_game)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chess")
        self.setGeometry(100, 100, 1100, 900)
        self.create_labels()
        self.create_board_buttons()
        self.create_move_history()
        self.update_ui()
        
    def update_time(self):
        self.engine_time = self.time_slider.value()
        self.time_label.setText('Engine Time: {}s'.format(self.engine_time))

    def update_skill(self):
        self.engine_skill = self.skill_slider.value()
        self.skill_label.setText('Engine Skill: {}'.format(self.engine_skill))
        self.engine.configure({"Skill Level": self.engine_skill})

    def create_labels(self):
        for i in range(8):
            self.create_rank_label(i)
            self.create_file_label(i)

    def create_rank_label(self, i):
        label = QLabel(self)
        label.setGeometry(25, i*100 + 75, 50, 50)
        self.rank_labels.append(label)

    def create_file_label(self, i):
        label = QLabel(self)
        label.setGeometry(i*100 + 100, 850, 50, 50)
        self.file_labels.append(label)

    def create_board_buttons(self):
        for i in range(64):
            self.create_board_button(i)

    def create_board_button(self, i):
        button = SvgButton(self)
        button.setGeometry((i % 8)*100 + 50, (i//8)*100 + 50, 100, 100)
        button.clicked.connect(self.make_move(i))
        if (i + i // 8) % 2 == 0:
            button.setStyleSheet("background-color: white")
        else:
            button.setStyleSheet("background-color: gray")
        self.buttons.append(button)

    def create_move_history(self):
        self.move_history = QListWidget(self)
        self.move_history.setGeometry(850, 50, 200, 800)
        self.move_history.itemClicked.connect(self.history_clicked)

    def update_ui(self):
        self.update_labels()
        self.update_board()

    def update_labels(self):
        for i in range(8):
            self.rank_labels[i].setText(str(8 - i))
            self.file_labels[i].setText(chr(ord('a') + i))

    def update_board(self):
        for i in range(64):
            self.update_square(i)

    def update_square(self, i):
        piece = self.board.piece_at((i % 8) + (7 - (i // 8)) * 8)
        if piece is not None:
            piece_color = 'w' if piece.color == chess.WHITE else 'b'
            piece_file = 'images/{}{}.svg'.format(piece_color, piece.symbol().upper())
            self.buttons[i].set_svg(piece_file)
        else:
            self.buttons[i].clear_svg()

    def make_move(self, index):
        def _make_move():
            real_index = (index % 8) + (7 - (index // 8)) * 8
            if self.selected_piece is None:
                piece = self.board.piece_at(real_index)
                if piece is not None and piece.color == self.board.turn:
                    self.selected_piece = real_index
            else:
                move = chess.Move(self.selected_piece, real_index)
                if move not in self.board.legal_moves:
                    promo_move = chess.Move(self.selected_piece, real_index, promotion=chess.QUEEN)
                    if promo_move in self.board.legal_moves:
                        # It's a valid pawn promotion, ask user for promotion choice
                        promo_choice = QMessageBox.question(self, "Pawn Promotion",
                                                            "Promote pawn to: ",
                                                            QMessageBox.StandardButtons(
                                                                QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel|QMessageBox.RestoreDefaults))
                        choices = {QMessageBox.Yes: chess.QUEEN, QMessageBox.No: chess.ROOK,
                                QMessageBox.Cancel: chess.BISHOP, QMessageBox.RestoreDefaults: chess.KNIGHT}
                        if promo_choice in choices:
                            move = chess.Move(self.selected_piece, real_index, promotion=choices[promo_choice])
                        else:
                            self.selected_piece = None
                            return
                        self.current_move_index += 1
                if move in self.board.legal_moves:
                    self.board.push(move)
                    # Add the move to the move history
                    item = QListWidgetItem(self.board.peek().uci())
                    item.setData(Qt.UserRole, move)
                    self.move_history.addItem(item)
                    self.selected_piece = None
                    self.update_ui()
                    self.check_game_end()

                    # After a successful move, let Stockfish make a move
                if not self.board.is_game_over():
                    self.stockfish_thread = StockfishThread(self.board, self.engine, self.engine_time)
                    self.stockfish_thread.signal.connect(self.update_after_stockfish)
                    self.stockfish_thread.start()
                else:
                    # Deselect the piece if the move is not legal
                    self.selected_piece = None
        return _make_move

    def update_after_stockfish(self, result):
        self.board.push(result.move)
        item = QListWidgetItem(self.board.peek().uci())
        item.setData(Qt.UserRole, result.move)
        self.move_history.addItem(item)
        self.update_ui()
        self.check_game_end()

    def check_game_end(self):
        if self.board.is_checkmate():
            QMessageBox.information(self, "Game Over", "Checkmate!")
        elif self.board.is_stalemate():
            QMessageBox.information(self, "Game Over", "Stalemate!")
        elif self.board.is_insufficient_material():
            QMessageBox.information(self, "Game Over", "Draw due to insufficient material!")
        elif self.board.is_seventyfive_moves():
            QMessageBox.information(self, "Game Over", "Draw due to the seventy-five move rule!")
        elif self.board.is_fivefold_repetition():
            QMessageBox.information(self, "Game Over", "Draw due to fivefold repetition!")
        elif self.board.is_variant_draw():
            QMessageBox.information(self, "Game Over", "Draw due to variant-specific conditions!")

    def closeEvent(self, event):
        # Make sure to quit the engine when the window is closed
        self.engine.quit()
        event.accept()

    def reset_game(self):
        self.board = chess.Board()
        self.move_history.clear()
        self.update_ui()

    def history_clicked(self, item):
        self.current_move_index = self.move_history.row(item)  # Set the current move index
        self.load_board_state()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if self.current_move_index > 0:
                self.current_move_index -= 1
                self.load_board_state()
        elif event.key() == Qt.Key_Right:
            if self.current_move_index < self.move_history.count() - 1:
                self.current_move_index += 1
                self.load_board_state()

    def load_board_state(self):
        self.board = chess.Board()
        for i in range(self.current_move_index + 1):
            move = self.move_history.item(i).data(Qt.UserRole)
            self.board.push(move)
        self.update_ui()

    def export_game(self):
        # Open a file dialog for saving files
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "PGN Files (*.pgn)", options=options)

        # If a file name is provided, write the game to that file
        if filename:
            game = chess.pgn.Game().from_board(self.board)
            with open(filename, 'w') as file:
                print(game, file=file, end="\n\n")

    def import_game(self):
        # Open a file dialog for opening files
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "PGN Files (*.pgn)", options=options)

        # If a file is selected, read the game from that file
        if filename:
            with open(filename) as f:
                game = chess.pgn.read_game(f)

            # Load the game into the board
            self.board = game.board()
            self.update_ui()
