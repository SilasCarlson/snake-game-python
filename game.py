import random
import pygame
from enum import Enum, auto
from player import Player
from food import Food

class GameState(Enum):
    GAME = auto()
    LOSE = auto()

class Game:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((384, 384))
        self._clock = pygame.time.Clock()
        self._is_running = False
        self._move_event = pygame.USEREVENT + 1
        self._gui_font = pygame.font.SysFont("Arial", 24)
        self._gui_font_large = pygame.font.SysFont("Arial", 48)
        self._last_movement_x = -1
        self._last_movement_y = 0
        self._score = 0
        self._state = GameState.GAME
        self._movement_stack = [pygame.Vector2(self._last_movement_x, self._last_movement_y)]

        pygame.display.set_caption("Snake Game")

        pygame.time.set_timer(self._move_event, 100)

        # board
        self._board_padding = 32
        self._board_square_size = 16
        self._board_width = 20
        self._board_height = 20
        self._board = [[0 for _ in range(self._board_width)] for _ in range(self._board_height)]

        # player
        player_board_x = 10
        player_board_y = 10
        player_x = player_board_x * self._board_square_size + self._board_padding
        player_y = player_board_y * self._board_square_size + self._board_padding
        self._player = Player(player_board_x, player_board_y, player_x, player_y, 16, 16)

        # food
        food_board_x = 3
        food_board_y = 10
        food_x = food_board_x * self._board_square_size + self._board_padding
        food_y = food_board_y * self._board_square_size + self._board_padding
        self._food = Food(food_board_x, food_board_y, food_x, food_y, self._board_square_size, self._board_square_size)

    def get_new_player_position(self):
        # Get the new position for the player
        player_board_position = self._player.get_board_position()
        new_board_position = pygame.Vector2(player_board_position.x + self._last_movement_x,
                                            player_board_position.y + self._last_movement_y)

        new_position = self.get_position_from_board(new_board_position)

        return new_board_position, new_position

    def start(self):
        self._is_running = True

        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False
                elif event.type == pygame.KEYDOWN and self._state == GameState.GAME:
                    movement_x = 0
                    movement_y = 0

                    if event.key == pygame.K_LEFT:
                        movement_x = -1
                    elif event.key == pygame.K_RIGHT:
                        movement_x = 1
                    elif event.key == pygame.K_UP:
                        movement_y = -1
                    elif event.key == pygame.K_DOWN:
                        movement_y = 1

                    if movement_x != 0 or movement_y != 0:
                        self._last_movement_x = movement_x
                        self._last_movement_y = movement_y
                        self._movement_stack.append(pygame.Vector2(self._last_movement_x, self._last_movement_y))

                elif event.type == self._move_event and self._state == GameState.GAME:
                    new_board_position, new_position = self.get_new_player_position()

                    ran_into_self = False
                    for index, body_part in enumerate(self._player.get_body_parts()):
                        body_part_board_position = body_part.get_board_position()
                        if body_part_board_position == new_board_position:
                            if index == 1:
                                # pop the movement stack and update the last movement keys to be that so the player doesn't just freeze and stop moving
                                self._movement_stack.pop()
                                self._last_movement_x = self._movement_stack[-1].x
                                self._last_movement_y = self._movement_stack[-1].y
                                new_board_position, new_position = self.get_new_player_position()
                            else:
                                ran_into_self = True

                    if new_board_position.x < 0 or new_board_position.x >= self._board_width or new_board_position.y < 0 or new_board_position.y >= self._board_height or ran_into_self:
                        self._state = GameState.LOSE
                    else:
                        # Get the food position
                        food_board_position = self._food.get_board_position()
                        grow = food_board_position.x == new_board_position.x and food_board_position.y == new_board_position.y

                        # If the player is touching the food then move the food to a random position on the board
                        if grow:
                            new_food_board_position = pygame.Vector2(random.randrange(0, self._board_width),
                                                                     random.randrange(0, self._board_height))
                            new_food_position = self.get_position_from_board(new_food_board_position)

                            self._food.set_board_position(new_food_board_position)
                            self._food.set_position(new_food_position)

                            self._score += 1

                        self._player.move(new_board_position, new_position, grow)

            self._screen.fill("purple")

            # Draw
            self._player.draw(self._screen)
            self._food.draw(self._screen)

            # Border
            text_surface = self._gui_font.render(f"Score {self._score}", True, "black")
            self._screen.blit(text_surface, (8, 0))
            pygame.draw.lines(self._screen, "black", True, [
                (self._board_padding, self._board_padding),
                (self._board_padding + self._board_width * self._board_square_size, self._board_padding),
                (self._board_padding + self._board_width * self._board_square_size, self._board_padding + self._board_height * self._board_square_size),
                (self._board_padding, self._board_padding + self._board_height * self._board_square_size)
            ])

            if self._state == GameState.LOSE:
                lose_text_surface = self._gui_font_large.render("You Lost!", True, "black")
                self._screen.blit(lose_text_surface, ((self._screen.get_width() - lose_text_surface.get_width()) / 2, (self._screen.get_height() - lose_text_surface.get_height()) / 2))

            pygame.display.flip()

            self._clock.tick(60)

        pygame.quit()

    def get_position_from_board(self, board_position):
        return pygame.Vector2(
            board_position.x * self._board_square_size + self._board_padding,
            board_position.y * self._board_square_size + self._board_padding
        )