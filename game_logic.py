import random
from collections import deque


class Game:
    """
    Класс, реализующий логику игры "2D Кубик Рубика со сдвигами".

    Атрибуты:
        size (int): Размер игрового поля (size x size).
        _board (list[list[int]]): Текущее состояние игрового поля.
        _initial_board (list[list[int]]): Начальное (решенное) состояние поля.
    """

    def __init__(self, size=3):
        """
        Инициализирует игру с заданным размером поля.

        Args:
            size (int): Размер стороны квадратного поля. Должен быть >= 2.
        """
        if not isinstance(size, int) or size < 2:
            raise ValueError("Размер поля должен быть целым числом >= 2")
        self._size = size
        self._initial_board = self._create_initial_board()
        self._board = [row[:] for row in self._initial_board]
        self.scramble()

    def _create_initial_board(self):
        """Создает начальное (решенное) состояние поля."""
        return [[r for _ in range(self._size)] for r in range(self._size)]

    @property
    def board(self):
        """
        Возвращает копию текущего состояния игрового поля.
        """
        return [row[:] for row in self._board]

    @property
    def size(self):
        return self._size

    def scramble(self, moves=None):
        """
        Перемешивает игровое поле, выполняя случайные сдвиги.
        """
        if moves is None:
            moves = self._size * 5

        for _ in range(moves):
            axis = random.choice(['row', 'col'])
            index = random.randrange(self._size)
            direction = random.choice([-1, 1]) # -1: влево/вверх, 1: вправо/вниз

            if axis == 'row':
                self.shift_row(index, direction)
            else:
                self.shift_col(index, direction)

        if self.is_solved():
             self.shift_row(0, 1)

    def shift_row(self, row_index, direction):
        """
        Циклически сдвигает указанную строку влево (direction=-1) или вправо (direction=1).
        """
        if not (0 <= row_index < self._size):
            raise IndexError("Неверный индекс строки")
        if direction not in [-1, 1]:
            raise ValueError("Направление должно быть -1 или 1")

        row_deque = deque(self._board[row_index])
        row_deque.rotate(direction)
        self._board[row_index] = list(row_deque)

    def shift_col(self, col_index, direction):
        """
        Циклически сдвигает указанный столбец вверх (direction=-1) или вниз (direction=1).
        """
        if not (0 <= col_index < self._size):
            raise IndexError("Неверный индекс столбца")
        if direction not in [-1, 1]:
            raise ValueError("Направление должно быть -1 или 1")

        col_deque = deque(self._board[r][col_index] for r in range(self._size))
        col_deque.rotate(direction)
        for r in range(self._size):
            self._board[r][col_index] = col_deque[r]

    def is_solved(self):
        """Проверяет, решено ли игровое поле."""
        return self._board == self._initial_board

    def reset(self):
        """Сбрасывает поле к начальному состоянию."""
        self._board = [row[:] for row in self._initial_board]

    @staticmethod
    def get_default_colors():
        """
        Возвращает стандартный набор цветов для отображения.
        Используем @staticmethod, т.к. этот метод не зависит от
        конкретного экземпляра игры (self).
        """

        from PyQt5.QtGui import QColor
        from PyQt5.QtCore import Qt

        return [
            QColor(Qt.red), QColor(Qt.green), QColor(Qt.blue),
            QColor(Qt.cyan), QColor(Qt.magenta), QColor(Qt.yellow),
            QColor(Qt.gray), QColor(Qt.darkRed), QColor(Qt.darkGreen),
            QColor(Qt.darkBlue), QColor(Qt.darkCyan), QColor(Qt.darkMagenta),
            QColor(Qt.darkYellow), QColor(Qt.darkGray), QColor(Qt.white),
            QColor(Qt.black)
        ]

    @staticmethod
    def get_color_for_value(value, colors):
        """
        Возвращает цвет для заданного числового значения из списка цветов.
        Использует модуль (%) для зацикливания цветов, если их меньше, чем size.
        """
        return colors[value % len(colors)]