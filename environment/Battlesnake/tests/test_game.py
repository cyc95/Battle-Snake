import unittest

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.RulesetSettings import RulesetSettings
from environment.Battlesnake.modes.Standard import StandardGame


class MyTestCase(unittest.TestCase):

    def test_game_with_rulset_settings(self):
        ruleset_settings = RulesetSettings(foodSpawnChance=99)

        game = StandardGame(ruleset_settings=ruleset_settings)

        self.assertEqual(game.ruleset_settings.foodSpawnChance, 99)


if __name__ == '__main__':
    unittest.main()
