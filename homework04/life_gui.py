import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.speed = speed
        self.cell_size = cell_size
        self.cell_width = self.life.cols
        self.cell_height = self.life.rows
        self.width = self.cell_size * self.cell_width
        self.height = self.cell_size * self.cell_height
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.grid = self.life.curr_generation

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        color = 0
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    color = "green"
                if cell == 0:
                    color = "white"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(color),
                    [
                        i * self.cell_size,
                        j * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ],
                )

    def run(self) -> None:
        """The running game"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        paused = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = True
                    if event.key == pygame.K_RETURN:
                        paused = False

            # click = pygame.mouse.get_pressed()
            # if click != (0, 0, 0) and paused:
            #     mouse_pos = pygame.mouse.get_pos()
            #     x, y = mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size
            #     if self.grid[y][x] == 1:
            #         self.grid[y][x] = 0
            #     else:
            #         self.grid[y][x] = 1

            # if self.life.is_max_generations_exceeded or not self.life.is_changing:
            #     running = False

            self.draw_grid()
            self.draw_lines()
            # if not paused:
            #     self.life.step()
            pygame.display.flip()
            self.life.step()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game_of_life = GameOfLife(size=(50, 50), randomize=True, max_generations=100)
    ui = GUI(game_of_life, cell_size=15, speed=10)
    ui.run()
