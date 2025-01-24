import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [
                [random.randint(0, 1) for _ in range(self.cols)]
                for _ in range(self.rows)
            ]
        else:
            grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        up_left, up, up_right = (row - 1, col - 1), (row - 1, col), (row - 1, col + 1)
        left, right = (row, col - 1), (row, col + 1)
        down_left, down, down_right = (
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
        )
        neighbours = [up_left, up, up_right, left, right, down_left, down, down_right]
        neighbour_values = []
        for x, y in neighbours:
            if 0 <= x < len(self.curr_generation) and 0 <= y < len(
                self.curr_generation[0]
            ):
                neighbour_values.append(self.curr_generation[x][y])
        return neighbour_values

    def get_next_generation(self) -> Grid:
        next_generation = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                sum_neighbours = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    if sum_neighbours == 2 or sum_neighbours == 3:
                        next_generation[i][j] = 1
                    else:
                        next_generation[i][j] = 0
                else:
                    if sum_neighbours == 3:
                        next_generation[i][j] = 1
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.generations += 1
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename, "r") as file:
            lines = [line.strip() for line in file]
            for line in lines:
                row = [int(el) for el in line]
                grid.append(row)
        life = GameOfLife((len(grid), len(grid[0])))
        life.curr_generation = grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as file:
            file.writelines([str(row) + "\n" for row in self.curr_generation])
