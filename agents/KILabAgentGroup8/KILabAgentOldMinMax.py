import math
from typing import Tuple, List, Optional
from environment.Battlesnake.agents.BaseAgent import BaseAgent
import numpy as np
import copy
from environment.Battlesnake.helper.DirectionUtil import DirectionUtil
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.grid_map import GridMap
from environment.Battlesnake.model.Occupant import Occupant
from environment.Battlesnake.util.kl_priority_queue import KLPriorityQueue
from agents.KILabAgentGroup8.simulator_environment import simulatorEnvironment
from agents.RandomAgent.RandomAgent import RandomAgent
from environment.Battlesnake.modes.Modes import GameMode
from environment.Battlesnake.model.RulesetSettings import RulesetSettings
from ctypes import *
import time


class KILabAgentOldMinMax(BaseAgent):

    def get_name(self):
        return 'OldMinMax'

    def get_head(self):
        return 'viper'

    def get_tail(self):
        return 'bolt'

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:

        # clib_minmax = cdll.LoadLibrary('./libminmax_thread.so')
        # clib_minmax = cdll.LoadLibrary('./libduel_ohne_pthread.so')
        clib_minmax = cdll.LoadLibrary('./agents/KILabAgentGroup8/shared_objects/minmax.so')
        clib_mcts = cdll.LoadLibrary('./agents/KILabAgentGroup8/shared_objects/libuntitled2.so')
        type_int_array_state = c_int * 121
        type_int_array_snake_head = c_int * 2
        array_state = type_int_array_state()
        you_snake_head = type_int_array_snake_head()
        opp_snake_head = type_int_array_snake_head()
        you_snake_length = c_int()
        opp_snake_length = c_int()
        you_snake_health = c_int()
        opp_snake_health = c_int()
        simulation_time = c_int()
        you_snake_direction = c_int()
        opp_snake_direction = c_int()
        for i in range(11):
            for j in range(11):
                array_state[i * 11 + j] = 0
        for f in board.food:
            array_state[f.x * 11 + f.y] = 500
        for snake in board.snakes:
            if not snake.is_alive():
                continue
            if snake.snake_id == you.snake_id:
                for i in range(len(snake.body)):
                    array_state[snake.body[-i - 1].x * 11 + snake.body[-i - 1].y] = i + 1
                you_snake_length = len(snake.body)
                you_snake_health = snake.health
                you_snake_head[0] = snake.body[0].x
                you_snake_head[1] = snake.body[0].y
                snake_direction = DirectionUtil.direction_to_reach_field(snake.body[1], snake.body[0])
                if snake_direction == Direction.UP:
                    you_snake_direction = 0
                if snake_direction == Direction.LEFT:
                    you_snake_direction = 1
                if snake_direction == Direction.RIGHT:
                    you_snake_direction = 2
                if snake_direction == Direction.DOWN:
                    you_snake_direction = 3
            else:
                for i in range(len(snake.body)):
                    array_state[snake.body[-i - 1].x * 11 + snake.body[-i - 1].y] = - i - 1
                opp_snake_length = len(snake.body)
                opp_snake_health = snake.health
                opp_snake_head[0] = snake.body[0].x
                opp_snake_head[1] = snake.body[0].y
                snake_direction = DirectionUtil.direction_to_reach_field(snake.body[1], snake.body[0])
                if snake_direction == Direction.UP:
                    opp_snake_direction = 0
                if snake_direction == Direction.LEFT:
                    opp_snake_direction = 1
                if snake_direction == Direction.RIGHT:
                    opp_snake_direction = 2
                if snake_direction == Direction.DOWN:
                    opp_snake_direction = 3
        simulation_time = 300

        if len(board.snakes) > 2:
            action = clib_mcts.getaction(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length,
                                you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction,
                                simulation_time)
        else:
            action = clib_minmax.getaction(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length,
                                you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction,
                                simulation_time)

        
        if action == 0:
            action = Direction.UP
        if action == 1:
            action = Direction.LEFT
        if action == 2:
            action = Direction.RIGHT
        if action == 3:
            action = Direction.DOWN

        return MoveResult(direction=action)

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass
