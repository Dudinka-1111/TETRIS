import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLUMNS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
BLACK = (0, 0, 0)
FPS = 1

# Цвета для фигур
COLORS = [
    (0, 255, 255),  # I - Голубой
    (128, 0, 128),  # T - Фиолетовый
    (255, 0, 0),    # Z - Красный
    (0, 255, 0),    # S - Зеленый
    (255, 255, 0),  # O - Желтый
    (255, 165, 0),  # L - Оранжевый
    (0, 0, 255)     # J - Синий
]

# Формы тетрисных фигур
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Класс фигуры
class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Класс игры
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_shape = Shape(COLUMNS // 2 - 1, 0)
        self.running = True
        self.game_over = False

    def draw_grid(self):
        self.screen.fill(BLACK)
        for y in range(ROWS):
            for x in range(COLUMNS):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(self.screen, self.grid[y][x],
                                     (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for y, row in enumerate(self.current_shape.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_shape.color,
                                     ((self.current_shape.x + x) * BLOCK_SIZE, (self.current_shape.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()

    def check_collision(self, dx, dy):
        for y, row in enumerate(self.current_shape.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.current_shape.x + x + dx, self.current_shape.y + y + dy
                    if nx < 0 or nx >= COLUMNS or ny >= ROWS or (ny >= 0 and self.grid[ny][nx]):
                        return True
        return False

    def lock_shape(self):
        for y, row in enumerate(self.current_shape.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_shape.y + y][self.current_shape.x + x] = self.current_shape.color

        if self.current_shape.y == 0:
            self.game_over = True
        else:
            self.current_shape = Shape(COLUMNS // 2 - 1, 0)

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        for _ in range(ROWS - len(new_grid)):
            new_grid.insert(0, [0] * COLUMNS)
        self.grid = new_grid

    def drop_shape(self):
        if not self.check_collision(0, 1):
            self.current_shape.y += 1
        else:
            self.lock_shape()
            self.clear_lines()

    def move(self, dx):
        if not self.check_collision(dx, 0):
            self.current_shape.x += dx

    def rotate_shape(self):
        self.current_shape.rotate()
        if self.check_collision(0, 0):
            self.current_shape.rotate()
            self.current_shape.rotate()
            self.current_shape.rotate()

    def display_game_over(self):
        font = pygame.font.SysFont('Arial', 36)
        text_surface = font.render('Game Over', True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1)
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()
                    elif event.key == pygame.K_DOWN:
                        self.drop_shape()
                    elif event.key == pygame.K_SPACE:
                        while not self.check_collision(0, 1):
                            self.current_shape.y += 1
                        self.lock_shape()
                        self.clear_lines()

            if not self.game_over:
                self.drop_shape()
                self.draw_grid()
            else:
                self.display_game_over()

        pygame.quit()

# Запуск игры
if __name__ == "__main__":
    tetris = Tetris()
    tetris.run()