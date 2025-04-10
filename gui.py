import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel,
    QDialog, QVBoxLayout, QSpinBox, QDialogButtonBox, QMenuBar, QAction,
    QMessageBox, QTextBrowser, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize

try:
    from game_logic import Game
except ImportError:
    print("Ошибка: Не удалось импортировать класс Game из game_logic.py.")
    print("Убедитесь, что файл game_logic.py находится в той же директории.")
    sys.exit(1)

class RulesDialog(QDialog):
    """Диалоговое окно для отображения правил игры."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Правила игры")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout(self)
        text_browser = QTextBrowser(self)
        text_browser.setHtml("""
            <h1>Правила игры "2D Кубик Рубика"</h1>
            <p>Цель игры - вернуть поле в исходное состояние, когда каждая строка заполнена ячейками одного цвета.</p>
            <p>Игровое поле представляет собой сетку NxN цветных ячеек.</p>
            <h2>Управление:</h2>
            <ul>
                <li>Кнопки <b>&lt;</b> и <b>&gt;</b> рядом с каждой строкой циклически сдвигают ячейки этой строки влево или вправо соответственно.</li>
                <li>Кнопки <b>&and;</b> (вверх) и <b>&or;</b> (вниз) над/под каждым столбцом циклически сдвигают ячейки этого столбца вверх или вниз соответственно.</li>
            </ul>
            <h2>Меню:</h2>
            <ul>
                <li><b>Игра -> Новая игра:</b> Начать новую игру с текущими настройками размера (поле будет перемешано).</li>
                <li><b>Игра -> Перемешать:</b> Перемешать текущее поле заново.</li>
                <li><b>Игра -> Настройки:</b> Изменить размер игрового поля (начнется новая игра).</li>
                <li><b>Помощь -> Правила:</b> Показать окно с правилами.</li>
                <li><b>Помощь -> Об авторе:</b> Показать информацию об авторе.</li>
            </ul>
            <p>Удачи!</p>
        """)
        layout.addWidget(text_browser)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        self.setLayout(layout)

class SettingsDialog(QDialog):
    """Диалоговое окно для настройки размера поля."""
    def __init__(self, current_size, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки игры")
        self.layout = QVBoxLayout(self)
        self.label = QLabel(f"Текущий размер поля: {current_size}x{current_size}\nВыберите новый размер (2-10):")
        self.layout.addWidget(self.label)
        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(2, 10)
        self.spin_box.setValue(current_size)
        self.layout.addWidget(self.spin_box)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_selected_size(self):
        """Возвращает выбранный размер поля."""
        return self.spin_box.value()

class MainWindow(QMainWindow):
    """Главное окно игры."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Кубик Рубика")
        self.setMinimumSize(600, 500)
        self.game = Game(size=3)
        self.colors = Game.get_default_colors()
        self.cell_widgets = []
        self.shift_buttons = {}
        self._init_ui()
        self._update_grid_display()

    def _init_ui(self):
        """Инициализация интерфейса (меню, панель игры)."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self._create_menu()
        self.game_area_layout = QGridLayout()
        self.game_area_layout.setSpacing(3)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.game_area_layout)
        self.status_label = QLabel("Поле перемешано. Удачи!")
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        self.main_layout.addStretch(1)
        self._create_grid_widgets()

    def _create_menu(self):
        """Создание меню."""
        menu_bar = self.menuBar()
        game_menu = menu_bar.addMenu("Игра")
        help_menu = menu_bar.addMenu("Помощь")

        new_game_action = QAction("Новая игра", self)
        new_game_action.triggered.connect(self.start_new_game)
        game_menu.addAction(new_game_action)

        scramble_action = QAction("Перемешать", self)
        scramble_action.triggered.connect(self.scramble_game)
        game_menu.addAction(scramble_action)

        settings_action = QAction("Настройки", self)
        settings_action.triggered.connect(self.open_settings)
        game_menu.addAction(settings_action)

        game_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)

        rules_action = QAction("Правила", self)
        rules_action.triggered.connect(self.open_rules)
        help_menu.addAction(rules_action)

        about_action = QAction("Об авторе", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        """Отображает диалоговое окно 'Об авторе'."""
        author_info = """
        <p><b>2D Кубик Рубика (v1.0)</b></p>
        <p>Работа была выполнена студентом 2 курса 8 группы Заметаевым Ильей.</p>
        <p><b>Связь:</b> <a href='https://t.me/adventureforourmind'>Telegram</a>, Email - ilyxaz68@mail.ru, <a href='https://vk.com/ilyshka068'>VK</p>
        """
        QMessageBox.about(self, "Об авторе", author_info)

    def _create_grid_widgets(self):
        """Создает виджеты для ячеек и кнопок управления."""
        # Очищаем предыдущие виджеты
        for i in reversed(range(self.game_area_layout.count())):
            widget = self.game_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.cell_widgets = []
        self.shift_buttons = {}

        size = self.game.size
        self.cell_widgets = [[None for _ in range(size)] for _ in range(size)]

        cell_dimension = 60
        button_thickness = int(cell_dimension * 0.5)

        # Создаем кнопки сдвига столбцов
        for c in range(size):
            btn_up = QPushButton("▲")
            btn_up.setFixedSize(cell_dimension, button_thickness)
            btn_up.clicked.connect(lambda _, col=c: self._handle_shift('col', col, -1))
            self.game_area_layout.addWidget(btn_up, 0, c + 1, alignment=Qt.AlignCenter)
            self.shift_buttons[('col', c, -1)] = btn_up

            btn_down = QPushButton("▼")
            btn_down.setFixedSize(cell_dimension, button_thickness)
            btn_down.clicked.connect(lambda _, col=c: self._handle_shift('col', col, 1))
            self.game_area_layout.addWidget(btn_down, size + 1, c + 1, alignment=Qt.AlignCenter)
            self.shift_buttons[('col', c, 1)] = btn_down

        # Создаем ячейки и кнопки сдвига строк
        for r in range(size):
            btn_left = QPushButton("◀")
            btn_left.setFixedSize(button_thickness, cell_dimension)
            btn_left.clicked.connect(lambda _, row=r: self._handle_shift('row', row, -1))
            self.game_area_layout.addWidget(btn_left, r + 1, 0, alignment=Qt.AlignCenter)
            self.shift_buttons[('row', r, -1)] = btn_left

            # Ячейки
            for c in range(size):
                cell = QLabel("")
                cell.setFixedSize(cell_dimension, cell_dimension)
                cell.setAutoFillBackground(True)
                cell.setAlignment(Qt.AlignCenter)
                font_size = max(8, int(cell_dimension / 4))
                cell.setFont(QFont("Arial", font_size, QFont.Bold))
                self.cell_widgets[r][c] = cell
                self.game_area_layout.addWidget(cell, r + 1, c + 1)

            btn_right = QPushButton("▶")
            btn_right.setFixedSize(button_thickness, cell_dimension)
            btn_right.clicked.connect(lambda _, row=r: self._handle_shift('row', row, 1))
            self.game_area_layout.addWidget(btn_right, r + 1, size + 1, alignment=Qt.AlignCenter)
            self.shift_buttons[('row', r, 1)] = btn_right


    def _update_grid_display(self):
        """Обновляет отображение ячеек на основе текущего состояния игры."""
        board_data = self.game.board
        size = self.game.size

        # Проверка и пересоздание виджетов при необходимости
        needs_recreate = False
        if not self.cell_widgets or len(self.cell_widgets) != size:
            needs_recreate = True
        else:
            # Проверяем внутренние списки на случай, если они пустые или неправильного размера
            for row_widgets in self.cell_widgets:
                 if not row_widgets or len(row_widgets) != size:
                      needs_recreate = True
                      break

        if needs_recreate:
            print("Пересоздание виджетов сетки...")
            self._create_grid_widgets()
            QApplication.processEvents()
            self.adjustSize()

        # Обновляем цвета ячеек
        for r in range(size):
            for c in range(size):
                value = board_data[r][c]
                color = Game.get_color_for_value(value, self.colors)
                # Проверка на существование cell_widgets[r][c] перед доступом
                if r < len(self.cell_widgets) and c < len(self.cell_widgets[r]) and self.cell_widgets[r][c]:
                    cell = self.cell_widgets[r][c]
                    palette = cell.palette()
                    palette.setColor(QPalette.Window, color)
                    cell.setPalette(palette)
                    # cell.setText(str(value)) # Показ цифры цвета (опционально)


    def _handle_shift(self, axis, index, direction):
        """Обработчик нажатия кнопок сдвига."""
        if self.game.is_solved(): # Если игра уже решена, не даем сдвигать
             return

        if axis == 'row':
            self.game.shift_row(index, direction)
        elif axis == 'col':
            self.game.shift_col(index, direction)

        self._update_grid_display()
        self._check_win_condition() # Проверяем после каждого хода

    def _check_win_condition(self):
        """Проверяет условие победы и выводит сообщение."""
        if self.game.is_solved():
            self.status_label.setText("Поздравляем! Поле собрано!")
            QMessageBox.information(self, "Победа!", "Вы собрали поле!")
        else:
            # Обновляем статус только если не показываем сообщение о победе
             if not self.status_label.text().startswith("Поздравляем"):
                 self.status_label.setText("В процессе...")


    def start_new_game(self):
        """Начинает новую игру с текущим размером (поле будет перемешано)."""
        current_size = self.game.size # Сохраняем текущий размер
        self.game = Game(size=current_size) # Создаем новую игру (сразу перемешивается)
        self._update_grid_display()
        self.status_label.setText("Новая игра. Поле перемешано.")
        self.adjustSize()

    def scramble_game(self):
        """Перемешивает текущее поле заново."""
        if self.game.is_solved():
             # Если было решено, просто перемешиваем
             self.game.scramble()
        else:
             # Если не решено, спрашиваем
             reply = QMessageBox.question(self, "Перемешать заново?",
                                          "Хотите перемешать поле еще раз?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
             if reply == QMessageBox.Yes:
                 self.game.scramble() # Перемешиваем текущее состояние
             else:
                  return # Ничего не делаем

        self._update_grid_display()
        self.status_label.setText("Поле перемешано заново.")
        self._check_win_condition() # На всякий случай, вдруг случайно соберется :)
        self.adjustSize()

    def open_settings(self):
        """Открывает диалог настроек и начинает новую игру с новым размером."""
        dialog = SettingsDialog(self.game.size, self)
        if dialog.exec_() == QDialog.Accepted:
            new_size = dialog.get_selected_size()
            if new_size != self.game.size:
                try:
                    # Создаем новую игру с новым размером (сразу перемешивается)
                    self.game = Game(size=new_size)
                    self.status_label.setText(f"Размер изменен на {new_size}x{new_size}. Поле перемешано.")
                    self._update_grid_display() # Обновление вызовет пересоздание виджетов
                    self.adjustSize() # Подгоняем размер окна

                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось создать игру: {e}")

    def open_rules(self):
        """Открывает диалог с правилами."""
        dialog = RulesDialog(self)
        dialog.exec_()