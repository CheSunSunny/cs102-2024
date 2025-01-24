import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Начальное поле игры
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        rows = self.cell_height
        cols = self.cell_width
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
        else:
            grid = [[0 for _ in range(cols)] for _ in range(rows)]

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    color = 'green'
                if cell == 0:
                    color = 'white'
                pygame.draw.rect(self.screen,
                                 pygame.Color(color),
                                 i * self.cell_size,
                                 j * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        up_left, up, up_right = (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)
        left, right = (row, col - 1), (row, col + 1)
        down_left, down, down_right = (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
        neighbours = [up_left, up, up_right, left, right, down_left, down, down_right]
        neighbour_values = []
        for x, y in neighbours:
            if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
                neighbour_values.append(self.grid[x][y])
        return neighbour_values

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        pass
