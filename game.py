import random
import pygame
from player import Player
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((384, 384))
        self._clock = pygame.time.Clock()
        self._is_running = False

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
        self._player = Player(player_board_x, player_board_y, player_x, player_y)

        # food
        food_board_x = 3
        food_board_y = 10
        food_x = food_board_x * self._board_square_size + self._board_padding
        food_y = food_board_y * self._board_square_size + self._board_padding
        self._food = Food(food_board_x, food_board_y, food_x, food_y, self._board_square_size, self._board_square_size)

    def start(self):
        self._is_running = True

        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False
                elif event.type == pygame.KEYDOWN:
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
                        player_board_position = self._player.get_board_position()
                        new_board_position = pygame.Vector2(player_board_position.x + movement_x, player_board_position.y + movement_y)
                        new_position = pygame.Vector2(
                            new_board_position.x * self._board_square_size + self._board_padding,
                            new_board_position.y * self._board_square_size + self._board_padding
                        )

                        food_board_position = self._food.get_board_position()
                        grow = food_board_position.x == new_board_position.x and food_board_position.y == new_board_position.y

                        if grow:
                            new_food_board_position = pygame.Vector2(random.randrange(0, self._board_width), random.randrange(0, self._board_height))
                            new_food_position = pygame.Vector2(
                                new_food_board_position.x * self._board_square_size + self._board_padding,
                                new_food_board_position.y * self._board_square_size + self._board_padding
                            )

                            self._food.set_board_position(new_food_board_position)
                            self._food.set_position(new_food_position)

                        self._player.move(new_board_position, new_position, grow)

            self._screen.fill("purple")

            # Draw
            self._player.draw(self._screen)
            self._food.draw(self._screen)

            pygame.display.flip()

            self._clock.tick(60)

        pygame.quit()