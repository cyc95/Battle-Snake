
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
from agents.KILabAgentGroup8.mcts import mcts
from agents.KILabAgentGroup8.KILabAgentV import KILabAgentV

import time


class KILabAgentOldOnServer(BaseAgent):

    def get_name(self):
        return 'KILabAgentOldOnServer'

    def get_head(self):
        return 'viper'

    def get_tail(self):
        return 'bolt'

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:

        possible_actions = you.possible_actions()
        if possible_actions is None:
            return None
        s_env = simulatorEnvironment(
            width=board.width,
            height=board.height,
            agents=[RandomAgent(), RandomAgent()],
            mode=GameMode.STANDARD,
            squad_assignments=[1, 1, 3, 3, 4, 4],
            ruleset_settings=RulesetSettings()
        )
        s_env.reset(board)
        root_node = mcts(0.35, s_env, you)
        root_v = root_node.policy_snake_test()
        action = np.argmax(root_v)

        if np.max(root_v) <= 0.9 and np.min([n for n in root_v if n != -1]) > -0.1:
            agent = KILabAgentV()
            opp_snake = copy.deepcopy([n for n in board.get_alive_and_dead_snakes() if n.snake_id != you.snake_id][0])
            action_agent = agent.move(game_info, turn, board, you).direction
            if action_agent is None:
                action_agent = possible_actions[action]
                return MoveResult(direction=action_agent)
            new_position = you.body[0].advanced(action_agent)
            if opp_snake.get_length() > you.get_length():
                if abs(new_position.x - opp_snake.body[0].x) + abs(new_position.y - opp_snake.body[0].y) == 1:
                    action_agent = possible_actions[action]
            return MoveResult(direction=action_agent)
        return MoveResult(direction=possible_actions[int(action)])

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

