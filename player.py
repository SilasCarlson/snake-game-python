import pygame.draw
import pygame.rect
import pygame.math

class BodyPart:
    def __init__(self, board_x, board_y, x, y, width, height):
        self._board_position = pygame.Vector2(board_x, board_y)
        self._position = pygame.Vector2(x, y)
        self._rectangle = pygame.Rect(x, y, width, height)
        self._color = "red"

    def get_board_position(self):
        return self._board_position

    def get_position(self):
        return self._position

    def set_board_position(self, board_position):
        self._board_position = board_position

    def set_position(self, position):
        self._position = position
        self._rectangle.x = position.x
        self._rectangle.y = position.y

    def set_color(self, color):
        self._color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self._rectangle)

class Player:
    def __init__(self, board_x, board_y, x, y, width, height):
        # Make the body parts
        self._width = width
        self._height = height
        self._head = BodyPart(board_x, board_y, x, y, self._width, self._height)
        self._tail = BodyPart(board_x + 1, board_y, x + 16, y, self._width, self._height)
        self._body_parts = [self._head, self._tail]

        self._head.set_color("orange")

    def draw(self, screen):
        for body_part in self._body_parts:
            body_part.draw(screen)

    def move(self, board_position, position, grow = False):
        # store the positions of the head
        last_board_position = self._head.get_board_position()
        last_position = self._head.get_position()

        for body_part in self._body_parts:
            if body_part == self._head:
                body_part.set_board_position(board_position)
                body_part.set_position(position)
            else:
                board_pos = body_part.get_board_position()
                pos = body_part.get_position()

                body_part.set_board_position(last_board_position)
                body_part.set_position(last_position)

                last_board_position = board_pos
                last_position = pos

        if grow:
            self._tail = BodyPart(last_board_position.x, last_board_position.y, last_position.x, last_position.y, 16, 16)
            self._body_parts.append(self._tail)

    def get_board_position(self):
        return self._head.get_board_position()