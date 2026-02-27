import pygame.math
import pygame.draw
import pygame.rect

class Food:
    def __init__(self, board_x, board_y, x, y, width, height):
        self._board_position = pygame.Vector2(board_x, board_y)
        self._position = pygame.math.Vector2(x, y)
        self._rectangle = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, "green", self._rectangle)

    def get_board_position(self):
        return self._board_position

    def set_board_position(self, board_position):
        self._board_position = board_position

    def set_position(self, position):
        self._position = position
        self._rectangle.x = position.x
        self._rectangle.y = position.y
