import multiprocessing

from environment.Battlesnake.agents.BaseAgent import BaseAgent
from typing import List, Optional
import pygame
import sys
import time
import traceback
from copy import deepcopy
from collections import Counter

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.RulesetSettings import RulesetSettings
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.errors import AgentTimeoutError
from environment.Battlesnake.modes.Modes import GameMode
from environment.Battlesnake.modes.Royal import RoyalGame
from environment.Battlesnake.modes.Solo import SoloGame
from environment.Battlesnake.modes.Standard import StandardGame
from environment.Battlesnake.modes.Squad import SquadGame
from environment.Battlesnake.modes.AbstractGame import AbstractGame
from environment.Battlesnake.renderer.field_color import FieldColor
from environment.Battlesnake.renderer.game_renderer import GameRenderer
from environment.Battlesnake.helper.helper import Helper
from environment.Battlesnake.exporter.Exporter import Exporter

default_colors = FieldColor.SNAKE_COLORS

class simulatorEnvironment:
    def __init__(
        self,
        width: int,
        height: int,
        agents: List[BaseAgent],
        mode: GameMode = GameMode.STANDARD,
        ruleset_settings: RulesetSettings = RulesetSettings(),
        squad_assignments: List[int] = None,
    ):
        self.width = width
        self.height = height
        self.num_snakes = len(agents)
        self.snake_ids = None
        self.agents: List[BaseAgent] = agents
        self.game: Optional[AbstractGame] = None
        self.board: Optional[BoardState] = None
        self.default_snake_colors = None
        self.mode = mode
        self.game_info = None
        self.ruleset_settings = ruleset_settings
        self.squad_assignments = squad_assignments
        if mode == GameMode.SQUAD:
            self.num_squads = len(set(squad_assignments))
            if self.num_snakes < 4:
                raise ValueError("In squad mode at least 4 players are required.")
            if (not squad_assignments or
               len(squad_assignments) != self.num_snakes or
               self.num_squads < 2 or
               any(count < 2 for count in Counter(squad_assignments).values())):
                raise ValueError("In squad mode at least 2 squads are required."
                                 " Every snake needs a squad and every squad two snakes.")

    def __del__(self):
        # prevent unnecessary instances running in connected remote snakes
        pass

    def reset(self, board_state=None):

        self.snake_ids = [Helper.generate_snake_id() for _ in range(self.num_snakes)]

        self.default_snake_colors = default_colors.copy()

        if self.mode == GameMode.STANDARD:
            game_class = StandardGame
        elif self.mode == GameMode.SOLO:
            game_class = SoloGame
        elif self.mode == GameMode.SQUAD:
            game_class = SquadGame
        elif self.mode == GameMode.ROYAL:
            game_class = RoyalGame
        else:
            raise ValueError('unknown mode:', self.mode)

        self.game = game_class(ruleset_settings=self.ruleset_settings)
        if board_state is None:
            self.board = self.game.create_initial_board_state(
                width=self.width, height=self.height, snake_ids=self.snake_ids
            )
        else:
            self.board = deepcopy(board_state)
            self.snake_ids = [n.snake_id for n in self.board.get_alive_and_dead_snakes()]

        self.update_snake_infos()

    def update_snake_infos(self):

        colors = self.default_snake_colors
        if self.mode == GameMode.SQUAD:
            squad_colors = {squad: None for squad in set(self.squad_assignments)}
            for squad in squad_colors:
                if squad_colors[squad] is None:
                    color = colors.pop(0)
                    colors.append(color)
                    squad_colors[squad] = color

        for idx, agent in enumerate(self.agents):
            snake_id = self.snake_ids[idx]
            snake = self.board.get_alive_or_dead_snake_by_id(snake_id)
            name = agent.get_name()
            color = agent.get_color()
            snake.snake_head = agent.get_head()
            snake.snake_tail = agent.get_tail()
            snake.snake_name = name
            if self.mode == GameMode.SQUAD:
                snake.squad = self.squad_assignments[idx]
            if snake.snake_color is None:
                if self.mode == GameMode.SQUAD:
                    snake.snake_color = squad_colors[snake.squad]
                else:
                    if color is None:
                        color = colors.pop(0)
                        colors.append(color)
                        snake.snake_color = color

    def step(self):
        """
        :return: Gibt zurück, ob das Spiel beendet wurde
        """
        if self.game.is_game_over(self.board):
            return True
        actions = {}
        board = self.board
        turn = self.board.turn
        for idx, snake_id in enumerate(self.snake_ids):
            agent = self.agents[idx]
            snake = board.get_alive_or_dead_snake_by_id(snake_id)
            #if not snake.is_alive():
            #    continue
            # nur 2 snakes. deswegen brauchen wir obere Code nicht
            agent_action = agent.move(game_info=self.game_info, turn=turn, board=board, you=snake)
            if agent_action is not None:
                agent_action = agent_action.direction
            actions[snake_id] = agent_action

        self.game.create_next_board_state(board=self.board, moves=actions)

        is_game_over = self.game.is_game_over(self.board)

        return is_game_over

    def step_action(self, action, opp_action, you_snake_id):
        """
        :return: Gibt zurück, ob das Spiel beendet wurde
        """           
        if self.game.is_game_over(self.board):
            return True

        actions = {}
        for idx, snake_id in enumerate(self.snake_ids):
            #snake = board.get_alive_or_dead_snake_by_id(snake_id)
            #if not snake.is_alive():
            #    continue
            # nur 2 snakes. deswegen brauchen wir obere Code nicht
            if snake_id != you_snake_id:
                actions[snake_id] = opp_action
            else:
                actions[snake_id] = action

        self.game.create_next_board_state(board=self.board, moves=actions)

        is_game_over = self.game.is_game_over(self.board)

        return is_game_over

    def is_game_over(self):
        return self.game.is_game_over(self.board)


