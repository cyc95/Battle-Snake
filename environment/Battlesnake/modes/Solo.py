
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.modes.Standard import StandardGame
from environment.Battlesnake.helper.helper import Helper
from environment.Battlesnake.model.Snake import Snake
from typing import List, Optional, Dict
from environment.Battlesnake.model.Snake import Snake


class SoloGame(StandardGame):

    def __init__(
            self,
            timeout: int = 400,
            game_info: Optional[GameInfo] = None,
            food_spawn_chance=0.15,
            minimumFood=1
    ):
        super().__init__(timeout, game_info, food_spawn_chance, minimumFood)

    @staticmethod
    def ruleset_name():
        return 'solo'

    def is_game_over(self, board: BoardState) -> bool:
        for s in board.snakes:
            if s.is_alive():
                return False
        return True
