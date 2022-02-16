import sys
from typing import Tuple
import os

import numpy as np
import pygame

from environment.Battlesnake.helper.DirectionUtil import DirectionUtil
from .field_color import FieldColor
from .helper.rounded_rect import AAfilledRoundedRect
from ..model.Direction import Direction
from environment.Battlesnake.model.board_state import BoardState
from ..model.EliminationEvent import EliminatedCause
from ..model.Snake import Snake
from environment.Battlesnake.util.icon_getter import get_head_from_assets, get_tail_from_assets

pygame.init()
pygame.font.init()

LEADERBOARD_WIDTH = 400
LEADERBOARD_ITEM_HEIGHT = 100
GAME_PADDING = 30


class GameRenderer:
    """
    Diese Klasse sorgt dafür, dass das Spiel mittels pygame angezeigt werden kann.
    """

    def __init__(
            self,
            max_game_width: int,
            max_game_height: int,
            max_num_snakes: int
    ):
        """
        Erstellt ein Fenster für das Spiel
        :param game_width: Spielfeldbreite
        :param game_height: Spielfeldhöhe
        :param nb_snakes: Anzahl der Schlangen im Leaderboard
        """

        self.pixel_per_field = 30
        self.y_inverted = True
        self.max_game_width = max_game_width
        self.max_game_height = max_game_height
        self.draw_winner_overlay = False

        self.surface_game = None
        self.surface_leaderboard = None
        self.game_pixel_width = None
        self.game_pixel_height = None
        self.leaderboard_pixel_height = None
        self.screen = None

        self.setup(game_width=max_game_width, game_height=max_game_height, nb_snakes=max_num_snakes)
        self.init_screen()

        self.health_bar_rects = None

        try:
            karla_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "../fonts/karla/Karla-Regular.ttf")
            self.myfont_name = pygame.font.Font(karla_path, 25)
            self.myfont_die_reason = pygame.font.Font(karla_path, 16)
            self.myfont_latency = pygame.font.Font(karla_path, 16)
        except FileNotFoundError:
            print("WARNING: Fonts not found! Using system default", file=sys.stderr)
            self.myfont_name = pygame.font.Font(pygame.font.get_default_font() , 25)
            self.myfont_die_reason = pygame.font.Font(pygame.font.get_default_font(), 16)
            self.myfont_latency = pygame.font.Font(pygame.font.get_default_font(), 16)

    def init_screen(self):

        total_width = GAME_PADDING + self.game_pixel_width + GAME_PADDING + LEADERBOARD_WIDTH + GAME_PADDING
        total_height = GAME_PADDING + max(self.game_pixel_height, self.leaderboard_pixel_height) + GAME_PADDING

        self.screen = pygame.display.set_mode((total_width, total_height))

        pygame.display.set_caption('KI-Labor Battlesnake')

    def setup(self, game_width: int, game_height: int, nb_snakes):

        game_pixel_width = game_width * self.pixel_per_field
        game_pixel_height = game_height * self.pixel_per_field

        leaderboard_pixel_height = nb_snakes * LEADERBOARD_ITEM_HEIGHT

        self.surface_game = pygame.Surface((game_pixel_width, game_pixel_height))
        self.surface_leaderboard = pygame.Surface((LEADERBOARD_WIDTH, leaderboard_pixel_height))

        self.game_height = game_height
        self.game_width = game_width

        self.game_pixel_width = game_pixel_width
        self.game_pixel_height = game_pixel_height
        self.leaderboard_pixel_height = leaderboard_pixel_height

    def display(self, board: BoardState):
        """
        Zeigt das Spiel an
        :param board: Game Objekt, das angezeigt wird
        :return:
        """

        # Der Hintergrund wird mit schwarz gefüllt
        self.screen.fill((0, 0, 0))

        # Die Spieloberfläche wird gezeichnet
        self.render(board, self.surface_game)
        self.render_leaderboard(board, self.surface_leaderboard)

        game_position = (GAME_PADDING, GAME_PADDING)
        self.screen.blit(self.surface_game, game_position)

        # Das Leaderboard wird gezeichnet
        leaderboard_y_start = GAME_PADDING + max((self.game_pixel_height - self.leaderboard_pixel_height) / 2, 0)
        leaderboard_position = (GAME_PADDING + self.game_pixel_width + GAME_PADDING, leaderboard_y_start)
        self.screen.blit(self.surface_leaderboard, leaderboard_position)

        # Wenn das Spiel gewonnen wurde, Info anzeigen
        if board.finished() and self.draw_winner_overlay:

            if len(board.snakes) == 1:
                snake = board.snakes[0]
                message = snake.snake_name + ' hat gewonnen'
            else:
                message = 'Unentschieden'

            font = pygame.font.Font(None, 40)
            text = font.render(message, True, (255, 255, 255))

            text_rect = text.get_rect()
            text_x = self.screen.get_width() / 2 - text_rect.width / 2
            text_y = self.screen.get_height() / 2 - text_rect.height / 2
            self.screen.blit(text, [text_x, text_y])

        # GUI aktualisieren
        pygame.display.flip()

    def game_to_pixel_coordinates(self, pts: np.ndarray):
        """
        Umrechnung der Spielfeldkoordinaten in Pixelkoordinaten
        """

        if self.y_inverted:
            pts[..., 1] = self.game_height - pts[..., 1]

        return (pts * self.pixel_per_field).astype(np.int32)

    def game_to_pixel_scale(self, data: np.ndarray):
        return data * self.pixel_per_field

    @staticmethod
    def color_image(image: pygame.Surface, color: Tuple[int, int, int]):
        arr = pygame.surfarray.pixels3d(image)
        arr[:,:,0] = color[0]
        arr[:,:,1] = color[1]
        arr[:,:,2] = color[2]

    @staticmethod
    def rotate_points_around_center(pts: np.ndarray, cnt: np.ndarray, degrees: float):
        """
        Rotiert die Punkte pts um das Zentrum cnt um die angegebene Gradzahl
        :param pts: Punkte, die rotiert werden sollen
        :param cnt: Zentrum der Rotation
        :param degrees: Grad um die rotiert werden soll
        :return: rotierte Punkte
        """
        ang = degrees / 180 * np.pi
        return np.dot(pts - cnt, np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]])) + cnt

    @staticmethod
    def flip_points_around_center(pts: np.ndarray, cnt: np.ndarray, vertical=False, horizontal=False):

        flip_mult = np.eye(2, 2)

        if vertical:
            flip_mult[0, 0] = -1

        if horizontal:
            flip_mult[1, 1] = -1

        return np.dot(pts - cnt, flip_mult) + cnt

    @staticmethod
    def rotate_asset(image: pygame.Surface, direction: Direction, y_inverted: bool):
        """
        Rotates Battlesnake head/tail asset toward given direction.
        Default is Direction.Right
        https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        """
        loc = image.get_rect().center
        angle = 0
        if direction == Direction.RIGHT:
            return image
        elif direction == Direction.DOWN:
            angle = -90 if y_inverted else 90
        elif direction == Direction.UP:
            angle = 90 if y_inverted else -90
        elif direction == Direction.LEFT:
            return pygame.transform.flip(image, True, False)
        else:
            print('ERROR unknown head direction')
        rot_sprite = pygame.transform.rotate(image, angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite


    @staticmethod
    def rotate_points(direction: Direction, pts: np.ndarray, center: np.ndarray, y_inverted):
        """
        Rotiert Punkte um eine Richtung
        Grundausrichtung ist  Direction.RIGHT
        """

        if direction == Direction.DOWN:
            a = 90 if y_inverted else -90
            pts = GameRenderer.rotate_points_around_center(pts, center, a)
            return pts

        elif direction == Direction.RIGHT:
            return GameRenderer.flip_points_around_center(pts, center, horizontal=y_inverted)

        elif direction == Direction.UP:
            a = -90 if y_inverted else 90
            pts = GameRenderer.rotate_points_around_center(pts, center, a)
            return pts

        elif direction == Direction.LEFT:
            return GameRenderer.flip_points_around_center(pts, center, vertical=True, horizontal=y_inverted)

        else:
            print('ERROR unknown head direction')

    def render(self, board: BoardState, surface: pygame.Surface):

        surface.fill(FieldColor.background)

        for hazard in board.hazards:
            pts = [
                [hazard.x, hazard.y],
                [hazard.x + 1, hazard.y + 1]
            ]

            pts = np.array(pts)
            pts_pg = self.game_to_pixel_coordinates(pts)

            p_x_min = min(pts_pg[:, 0])
            p_x_max = max(pts_pg[:, 0])

            p_y_min = min(pts_pg[:, 1])
            p_y_max = max(pts_pg[:, 1])

            pygame.draw.rect(surface, FieldColor.hazard, pygame.Rect(p_x_min, p_y_min, p_x_max - p_x_min, p_y_max - p_y_min), 0)


        # draw alive snakes on top of dead snakes
        # snakes = sorted(board.all_snakes, key=lambda s: s.is_alive(), reverse=False)
        snakes = board.get_all_snakes_sorted()

        # Snakes zeichnen
        for snake in snakes:

            snake_id = snake.snake_id
            snake_body = snake.body
            snake_length = len(snake_body)
            snake_color = snake.snake_color
            is_alive = snake.is_alive()

            if not is_alive:
                snake_color = GameRenderer.mix_colors(snake_color, FieldColor.background, 0.5)

            directions = []

            for i in range(snake_length - 1):
                body_cur = snake_body[i]
                body_last = snake_body[i + 1]
                d = DirectionUtil.direction_to_reach_field(from_position=body_last, to_position=body_cur)

                # body may have overlapping parts in the beginning
                if d is None:
                    snake_length = i + 1
                    break

                directions.append(d)

            if len(directions) == 0:
                directions.append(Direction.UP)

            # copy last direction for tail
            directions.append(directions[len(directions) - 1])

            for body_idx in range(snake_length):
                body_part = snake_body[body_idx]
                direction = directions[body_idx]

                x_min, y_min, x_max, y_max = body_part.x, body_part.y, body_part.x + 1, body_part.y + 1,

                # TODO draw a little bit darker if on a hazard
                if body_idx == 0:
                    # Kopf zeichnen

                    head_png = get_head_from_assets(snake.snake_head)
                    head_png = pygame.transform.scale(head_png, self.game_to_pixel_scale(np.array((1, 1))))
                    head_png = GameRenderer.rotate_asset(head_png, direction, self.y_inverted)
                    GameRenderer.color_image(head_png, snake_color)
                    head_rect = head_png.get_rect()
                    head_rect.center = self.game_to_pixel_coordinates(np.array((x_min + 0.5, y_min + 0.5)))
                    self.surface_game.blit(head_png, head_rect)

                elif body_idx == snake_length - 1:
                    # Hinterteil zeichnen

                    tail_png = get_tail_from_assets(snake.snake_tail)
                    tail_png = pygame.transform.scale(tail_png, self.game_to_pixel_scale(np.array((1, 1))))
                    tail_png = GameRenderer.rotate_asset(tail_png, DirectionUtil.get_opposite_direction(direction), self.y_inverted)
                    GameRenderer.color_image(tail_png, snake_color)
                    tail_rect = tail_png.get_rect()
                    tail_rect.center = self.game_to_pixel_coordinates(np.array((x_min + 0.5, y_min + 0.5)))
                    self.surface_game.blit(tail_png, tail_rect)
                else:

                    pts = [
                        [x_min, y_min],
                        [x_max, y_max]
                    ]

                    pts = np.array(pts)
                    pts_pg = self.game_to_pixel_coordinates(pts)

                    p_x_min = min(pts_pg[:, 0])
                    p_x_max = max(pts_pg[:, 0])

                    p_y_min = min(pts_pg[:, 1])
                    p_y_max = max(pts_pg[:, 1])

                    pygame.draw.rect(surface, snake_color,
                                     pygame.Rect(p_x_min, p_y_min, p_x_max - p_x_min, p_y_max - p_y_min), 0)

        # draw food
        for f in board.food:
            center = np.array([
                f.x + 0.5, f.y + 0.5
            ])

            radius_pg = int(0.8 * self.pixel_per_field / 2)
            center_pg = self.game_to_pixel_coordinates(center)

            # TODO draw a little bit darker if on a hazard
            pygame.draw.circle(surface, FieldColor.food, center_pg, radius_pg)

    def render_leaderboard(self, board: BoardState, surface: pygame.Surface):
        """
        Leaderboard zeichnen
        :param board: aktuelles Spiel
        :param surface: pygame surface (Fenster)
        :return:
        """

        surface.fill((0, 0, 0))

        surface_width = surface.get_width()
        snakes = board.get_all_snakes_sorted(reverse=True)

        text_color = (255, 255, 255)

        padding_content_left = 20

        for i in range(len(snakes)):
            snake = snakes[i]

            x_start = 0
            y_start = i * LEADERBOARD_ITEM_HEIGHT

            snake_color = snake.snake_color

            snake_health = max(snake.health, 0)
            snake_text_color = text_color

            if snake.elimination_event is not None:
                snake_eliminated_cause = snake.elimination_event.cause
                snake_eliminated_cause_text = GameRenderer.snake_death_reason(snake, board=board) if snake_eliminated_cause is not None else None
            else:
                snake_eliminated_cause_text = None

            if not snake.is_alive():
                snake_text_color = GameRenderer.mix_colors(snake_text_color, FieldColor.background, 0.3)
                snake_color = GameRenderer.mix_colors(snake_color, FieldColor.background, 0.5)

            snake_latency_text = '{} ms'.format(int(1000*snake.latency) if snake.latency is not None else '')

            textsurface_snake_name = self.myfont_name.render(snake.snake_name, True, snake_text_color)
            textsurface_snake_length = self.myfont_name.render(str(snake.get_length()), True, snake_text_color)
            if snake.squad:
                textsurface_snake_squad = self.myfont_latency.render(f'Squad {snake.squad}', True, snake_text_color)
            textsurface_eliminated_cause = self.myfont_die_reason.render(snake_eliminated_cause_text, True,
                                                                         snake_text_color)
            textsurface_latency = self.myfont_latency.render(snake_latency_text, True, snake_text_color)

            if snake.squad:
                textsurface_snake_squad_rect = textsurface_snake_squad.get_rect()
            textsurface_snake_length_rect = textsurface_snake_length.get_rect()
            textsurface_latency_rect = textsurface_latency.get_rect()

            surface.blit(textsurface_snake_name, (x_start + padding_content_left, y_start))
            surface.blit(textsurface_snake_length,
                         (x_start + surface_width - textsurface_snake_length_rect.width, y_start))

            if snake.squad:
                surface.blit(textsurface_snake_squad, (x_start + padding_content_left, y_start + 25))
            surface.blit(textsurface_latency,
                         (x_start + surface_width - textsurface_latency_rect.width, y_start + 25))

            eliminated_reason_y = y_start + 50

            surface.blit(textsurface_eliminated_cause, (x_start + padding_content_left, eliminated_reason_y))

            bar_y_start = y_start + 50

            health_bar_height = 20

            color_rect = pygame.Rect(x_start, y_start, 5, LEADERBOARD_ITEM_HEIGHT - 25)
            AAfilledRoundedRect(surface, color_rect, snake_color, 1.0)

            background_bar_color = GameRenderer.mix_colors(snake.snake_color, FieldColor.background, 0.5)
            background_bar_rect = pygame.Rect(x_start, bar_y_start, surface_width, health_bar_height)
            # pygame.draw.rect(surface, background_bar_color, background_bar_rect)
            # AAfilledRoundedRect(surface, background_bar_rect, background_bar_color, 1.0)

            # snake_health = 1
            if snake.is_alive() and snake_health > 0:
                bar_rect = pygame.Rect(x_start + padding_content_left, bar_y_start,
                                       snake_health / 100 * (surface_width - padding_content_left), health_bar_height)
                # pygame.draw.rect(surface, snake_info.color, bar_rect)
                AAfilledRoundedRect(surface, bar_rect, snake.snake_color, 1.0)

    @staticmethod
    def snake_death_reason(snake: Snake, board: BoardState):
        ee = snake.elimination_event
        ec = ee.cause

        if ec == EliminatedCause.EliminatedByCollision:
            s = board.get_alive_or_dead_snake_by_id(ee.by)
            return "Ran into {}'s body".format(s.snake_name)
        elif ec == EliminatedCause.EliminatedByHeadToHeadCollision:
            s = board.get_alive_or_dead_snake_by_id(ee.by)
            return 'Lost head-to-head with {}'.format(s.snake_name)
        elif ec == EliminatedCause.EliminatedByOutOfBounds:
            return 'Moved out of bounds'
        elif ec == EliminatedCause.EliminatedByOutOfHealth:
            return 'Out of health'
        elif ec == EliminatedCause.EliminatedBySelfCollision:
            return 'Collided with itself'
        else:
            print('WARNING: unknown eliminated cause:', ec)
            return ''

    @staticmethod
    def mix_colors(color_a, color_b, ratio):
        """
        Mischt zwei Farben
        :param color_a:
        :param color_b:
        :param ratio: Verhältnis der Mischung. 0 entspricht nur Farbe B und 1 nur Farbe A
        :return:
        """
        m = (ratio * np.array(color_a) + (1 - ratio) * np.array(color_b))

        return tuple([int(i) for i in m])
