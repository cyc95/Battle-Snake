import random
import numpy as np
from typing import Dict

from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.Hazard import Hazard
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.modes.Standard import StandardGame


class RoyalGame(StandardGame):
    pass

    @staticmethod
    def ruleset_name():
        return 'royal'

    def create_next_board_state(self, board: BoardState, moves: Dict[str, Direction], only_deterministic: bool = False):

        super().create_next_board_state(board=board, moves=moves, only_deterministic=only_deterministic)

        self.populateHazards(board)


    def populateHazards(self, board: BoardState):
        royale_shrinkEveryNTurns = self.ruleset_settings.royale_shrinkEveryNTurns

        if royale_shrinkEveryNTurns < 1:
            raise ValueError("royale game can't shrink more frequently than every turn")

        if board.turn < royale_shrinkEveryNTurns:
            return

        numShrinks = board.turn // royale_shrinkEveryNTurns
        rng = np.random.default_rng(self.ruleset_settings.seed)
        x_min = 0
        x_max = board.width - 1
        y_min = 0
        y_max = board.height - 1

        for _ in range(numShrinks):

            m = rng.integers(0, 4)
            if m == 0:
                x_min += 1
            elif m == 1:
                x_max -= 1
            elif m == 2:
                y_min += 1
            elif m == 3:
                y_max += 1

        board.hazards = []
        for x in range(board.width):
            for y in range(board.height):
                if x < x_min or x > x_max or y < y_min or y > y_max:
                    board.hazards.append(Hazard(x=x, y=y))



