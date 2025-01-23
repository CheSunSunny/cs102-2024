from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    directions = ["up", "right"]
    direction = choice(directions)
    if direction == "up" and coord[0] - 2 > 0:
        grid[coord[0] - 1][coord[1]] = " "
    else:
        direction = "right"
    if direction == "right" and coord[1] + 2 < len(grid[0]):
        grid[coord[0]][coord[1] + 1] = " "
    elif direction == "right" and coord[0] - 2 > 0:
        grid[coord[0] - 1][coord[1]] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    while empty_cells:
        x, y = empty_cells.pop(0)
        grid = remove_wall(grid, (x, y))

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = (
            randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        )
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for x, row in enumerate(grid):
        for y, cell in enumerate(grid[x]):
            if cell == k:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    step_x, step_y = x + dx, y + dy
                    if (
                        0 <= step_x < len(grid) and 0 <= step_y < len(grid[0])
                    ) and grid[step_x][step_y] == 0:
                        grid[step_x][step_y] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    curr_coord = exit_coord
    k = int(grid[exit_coord[0]][exit_coord[1]])
    path_len = grid[exit_coord[0]][exit_coord[1]]
    coords = [(x, y) for x, row in enumerate(grid) for y, cell in enumerate(row)]
    path = [curr_coord]

    while grid[curr_coord[0]][curr_coord[1]] != 1:
        near = [
            (curr_coord[0] + 1, curr_coord[1]),
            (curr_coord[0] - 1, curr_coord[1]),
            (curr_coord[0], curr_coord[1] + 1),
            (curr_coord[0], curr_coord[1] - 1),
        ]
        for cell in near:
            if (cell[0], cell[1]) in coords and grid[cell[0]][cell[1]] == k - 1:
                path.append((cell[0], cell[1]))
                curr_coord = (cell[0], cell[1])
                k -= 1
                break
    if len(path) != path_len:
        grid[curr_coord[0]][curr_coord[1]] = " "
        shortest_path(grid, exit_coord)

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    left_up_corner = coord == (0, 0)
    right_up_corner = coord == (0, len(grid[0]) - 1)
    left_down_corner = coord == (len(grid) - 1, 0)
    right_down_corner = coord == (len(grid) - 1, len(grid[0]) - 1)

    left_side = (0 <= coord[0] <= len(grid) - 1) and coord[1] == 0
    right_side = (0 <= coord[0] <= len(grid) - 1) and coord[1] == len(grid[0]) - 1
    up_side = coord[0] == 0 and (0 <= coord[1] <= len(grid[0]) - 1)
    down_side = coord[0] == len(grid) - 1 and (0 <= coord[1] <= len(grid[0]) - 1)

    if left_up_corner or right_up_corner or left_down_corner or right_down_corner:
        return True
    elif left_side:
        if grid[coord[0]][coord[1] + 1] == "■":
            return True
    elif right_side:
        if grid[coord[0]][coord[1] - 1] == "■":
            return True
    elif up_side:
        if grid[coord[0] + 1][coord[1]] == "■":
            return True
    elif down_side:
        if grid[coord[0] - 1][coord[1]] == "■":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[
    List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
]:
    """

    :param grid:
    :return:
    """
    if len(get_exits(grid)) == 1:
        return grid, get_exits(grid)[0]
    start, end = get_exits(grid)

    if encircled_exit(grid, start) or encircled_exit(grid, end):
        return grid, None

    grid[start[0]][start[1]] = 1
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell in [" ", "X"]:
                grid[x][y] = 0
    k = 0
    while grid[end[0]][end[1]] == 0:
        k += 1
        make_step(grid, k)

    return grid, shortest_path(grid, end)


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
