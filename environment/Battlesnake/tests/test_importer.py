import unittest
import json
import os

from environment.Battlesnake.importer.Importer import Importer
from environment.Battlesnake.model.EliminationEvent import EliminatedCause
from environment.Battlesnake.model.Food import Food
from environment.Battlesnake.model.Position import Position


class ImporterTestCase(unittest.TestCase):

    def test_parse_request(self):

        with open(os.path.dirname(__file__) + '/data/request_1.json') as json_file:
            data = json.load(json_file)

        # print(data)

        parsed = Importer.parse_request(data)
        # print(parsed)

        game_info, turn, board, you = parsed

        self.assertEqual(game_info.id, "game-00fe20da-94ad-11ea-bb37")
        self.assertEqual(game_info.ruleset['name'], "standard")
        self.assertEqual(game_info.ruleset['version'], "v.1.2.3")
        self.assertEqual(game_info.ruleset_settings.hazardDamagePerTurn, 7)
        self.assertEqual(game_info.ruleset_settings.foodSpawnChance, 15)
        self.assertEqual(game_info.ruleset_settings.minimumFood, 1)
        self.assertEqual(game_info.ruleset_settings.royale_shrinkEveryNTurns, 29)
        self.assertEqual(game_info.ruleset_settings.squad_allowBodyCollisions, True)
        self.assertEqual(game_info.ruleset_settings.squad_sharedElimination, False)
        self.assertEqual(game_info.ruleset_settings.squad_sharedHealth, True)
        self.assertEqual(game_info.ruleset_settings.squad_sharedLength, True)
        self.assertEqual(game_info.timeout, 500)

        self.assertEqual(turn, 14)
        self.assertEqual(you.snake_id, "snake-508e96ac-94ad-11ea-bb37")
        self.assertEqual(you.snake_name, "My Snake")
        self.assertEqual(you.health, 54)
        self.assertEqual(you.body[1], Position(x=1, y=0))
        self.assertEqual(you.get_length(), 3)
        self.assertEqual(you.latency, "111")
        self.assertEqual(you.shout, "why are we shouting??")
        self.assertEqual(you.squad, "")

        self.assertEqual(board.height, 11)
        self.assertEqual(board.width, 11)
        self.assertEqual(len(board.snakes), 2)
        self.assertEqual(board.snakes[0].snake_id, "snake-508e96ac-94ad-11ea-bb37")
        self.assertEqual(board.snakes[1].snake_id, "snake-b67f4906-94ae-11ea-bb37")
        self.assertEqual(len(board.food), 3)
        self.assertEqual(board.food[0], Position(x=5, y=5))
        self.assertEqual(board.food[1], Position(x=9, y=0))
        self.assertEqual(board.food[2], Position(x=2, y=6))

        self.assertEqual(len(board.hazards), 1)
        self.assertEqual(board.hazards[0], Position(x=3, y=2))

    def test_parse_snake(self):

        data = {
            "id": "snake-508e96ac-94ad-11ea-bb37",
            "name": "My Snake",
            "health": 54,
            "body": [
                {"x": 0, "y": 5},
                {"x": 1, "y": 5},
                {"x": 1, "y": 4}
            ],
            "latency": "111",
            "head": {"x": 0, "y": 0},
            "length": 3,
            "shout": "why are we shouting??",
            "squad": "A"
        }

        snake = Importer.parse_snake(data)

        self.assertEqual(snake.snake_id, "snake-508e96ac-94ad-11ea-bb37")
        self.assertEqual(snake.snake_name, "My Snake")
        self.assertEqual(snake.health, 54)
        self.assertEqual(len(snake.body), 3)
        self.assertEqual(snake.body[0], Position(x=0, y=5))
        self.assertEqual(snake.body[1], Position(x=1, y=5))
        self.assertEqual(snake.body[2], Position(x=1, y=4))
        self.assertEqual(snake.get_length(), 3)
        self.assertEqual(snake.latency, "111")
        self.assertEqual(snake.shout, "why are we shouting??")
        self.assertEqual(snake.squad, "A")

    def test_parse_bs_crawled_game(self):

        with open(os.path.dirname(__file__) + '/data/turns.json') as json_file:
            data = json.load(json_file)

        # print(data)

        turn_data_first = data[0]

        board = Importer.parse_board(turn_data_first, turn=0, default_width=10, default_height=10)
        self.assertEqual(len(board.snakes), 4)
        self.assertEqual(len(board.dead_snakes), 0)

        self.assertEqual(len(board.food), 5)
        self.assertEqual(board.food[1], Food(x=0, y=4))

        self.assertEqual(len(board.hazards), 0)

        snake_first = board.snakes[0]
        self.assertEqual(snake_first.snake_id, "gs_cbYdFhWCVTwdRXmbDvYmRG4T")
        self.assertEqual(snake_first.snake_name, "moon-snake-pika")
        self.assertEqual(len(snake_first.body), 3)
        self.assertEqual(snake_first.body[1], Position(x=5, y=9))

    def test_parse_bs_crawled_game_turn_83(self):

        with open(os.path.dirname(__file__) + '/data/turns.json') as json_file:
            data = json.load(json_file)

        turn_data = data[83]

        board = Importer.parse_board(turn_data, turn=0, default_width=10, default_height=10)
        self.assertEqual(len(board.snakes), 2)
        self.assertEqual(len(board.dead_snakes), 2)
        snake_first = board.snakes[0]
        self.assertEqual(snake_first.snake_id, "gs_cbYdFhWCVTwdRXmbDvYmRG4T")
        self.assertEqual(snake_first.snake_name, "moon-snake-pika")
        self.assertEqual(len(snake_first.body), 13)
        self.assertEqual(snake_first.body[2], Position(x=5, y=6))
        self.assertEqual(snake_first.health, 89)
        self.assertIsNone(snake_first.elimination_event)

        snake_second = board.dead_snakes[0]
        self.assertEqual(snake_second.snake_id, "gs_6TH9BpwSrWrkVVRPhdq6wpT6")
        self.assertEqual(snake_second.snake_name, "Ouroboros 2")
        self.assertIsNotNone(snake_second.elimination_event)
        self.assertEqual(snake_second.elimination_event.cause, EliminatedCause.EliminatedBySelfCollision)
        self.assertEqual(snake_second.elimination_event.turn, 19)
        self.assertEqual(snake_second.elimination_event.by, "gs_6TH9BpwSrWrkVVRPhdq6wpT6")

    def test_parse_bs_crawled_game_turn_107(self):

        with open(os.path.dirname(__file__) + '/data/turns.json') as json_file:
            data = json.load(json_file)

        turn_data = data[107]

        board = Importer.parse_board(turn_data, turn=0, default_width=10, default_height=10)
        self.assertEqual(len(board.snakes), 1)
        self.assertEqual(len(board.dead_snakes), 3)
        self.assertEqual(board.finished(), True)


if __name__ == '__main__':
    unittest.main()
