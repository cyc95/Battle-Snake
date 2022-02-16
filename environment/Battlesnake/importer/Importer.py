from environment.Battlesnake.model.Food import Food
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.Hazard import Hazard
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.RulesetSettings import RulesetSettings
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.EliminationEvent import EliminationEvent
from environment.Battlesnake.model.EliminationEvent import EliminatedCause


class CaseInsensitiveDict(dict):
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)

    def update(self, E={}, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)


def gg(l, d: dict):
    for k in l:
        if k in d:
            return d[k]
    return None


class Importer:

    @staticmethod
    def parse_request(json):
        game_json = json['game']
        turn = json['turn']
        board_json = json['board']
        you_json = json['you']

        game = Importer.parse_game_info(game_json)
        board = Importer.parse_board(board_json, turn=turn)
        you = Importer.parse_snake(you_json)

        return game, turn, board, you

    @staticmethod
    def parse_game_info(json):
        game_id = json['id']
        ruleset = json['ruleset']
        ruleset_name = ruleset['name'] if ruleset is not None else None
        ruleset_version = ruleset['version'] if ruleset is not None else None
        ruleset_settings_raw = ruleset['settings'] if ruleset is not None else None
        timeout = json['timeout']

        ruleset_settings = Importer.parse_rulset_settings(ruleset_settings_raw)

        return GameInfo(
            game_id=game_id,
            ruleset_name=ruleset_name,
            ruleset_version=ruleset_version,
            timeout=timeout,
            ruleset_settings=ruleset_settings
        )

    @staticmethod
    def parse_rulset_settings(json):

        data = {}

        if json:
            if 'foodSpawnChance' in json:
                data['foodSpawnChance'] = json['foodSpawnChance']
            if 'minimumFood' in json:
                data['minimumFood'] = json['minimumFood']
            if 'hazardDamagePerTurn' in json:
                data['hazardDamagePerTurn'] = json['hazardDamagePerTurn']
            if 'royale' in json:
                royale = json['royale']
                data['royale_shrinkEveryNTurns'] = royale['shrinkEveryNTurns']

            if 'squad' in json:
                squad = json['squad']
                data['squad_allowBodyCollisions'] = squad['allowBodyCollisions']
                data['squad_sharedElimination'] = squad['sharedElimination']
                data['squad_sharedHealth'] = squad['sharedHealth']
                data['squad_sharedLength'] = squad['sharedLength']

        return RulesetSettings(**data)

    @staticmethod
    def parse_board(json, turn: int, default_width=None, default_height=None):
        json = CaseInsensitiveDict(json)

        height = json['height'] if 'height' in json else default_height
        width = json['width'] if 'width' in json else default_width
        food_json_list = json['food']
        hazards_json_list = json['hazards'] if 'hazards' in json else []
        snakes_json_list = json['snakes']
        # kilab specific attribute
        dead_snakes_json_list = json['dead_snakes'] if 'dead_snakes' in json else []

        food = Importer.parse_food_array(food_json_list)
        hazards = Importer.parse_hazard_array(hazards_json_list)
        snakes = Importer.parse_snake_array(snakes_json_list)
        dead_snakes = Importer.parse_snake_array(dead_snakes_json_list)

        snakes_alive = [s for s in snakes if s.is_alive()]
        also_dead_snakes = [s for s in snakes if not s.is_alive()]

        dead_snakes.extend(also_dead_snakes)

        board = BoardState(
            turn=turn,
            width=width,
            height=height,
            food=food,
            hazards=hazards,
            snakes=snakes_alive,
            dead_snakes=dead_snakes
        )

        return board

    @staticmethod
    def parse_snake(json):
        json = CaseInsensitiveDict(json)

        snake_id = json['id']
        snake_name = json['name']
        # kilab specific attribute
        snake_color = json['color'] if 'color' in json else None
        health = json['health']
        body_json_list = json['body']
        latency = json['latency'] if 'latency' in json else 0
        # head = json['head']
        # length = json['length']
        shout = json['shout'] if 'shout' in json else ""
        squad = json['squad'] if 'squad' in json else ""

        body = Importer.parse_position_array(body_json_list)

        snake = Snake(
            snake_id=snake_id,
            snake_name=snake_name,
            snake_color=snake_color,
            health=health,
            body=body,
            latency=latency,
            shout=shout,
            squad=squad,
        )

        death_json = gg(("elimination_event", "death"), json)

        if death_json is not None:
            snake.elimination_event = Importer.parse_snake_death(death_json)

        return snake

    @staticmethod
    def parse_snake_death(json):
        json = CaseInsensitiveDict(json)

        cause = json["cause"]
        turn = json["turn"]
        by = gg(("by", "EliminatedBy"), json)

        event = EliminationEvent(EliminatedCause(cause), turn, by)

        return event

    @staticmethod
    def parse_snake_array(json_list):
        return list(map(Importer.parse_snake, json_list))

    @staticmethod
    def parse_position(json):
        json = CaseInsensitiveDict(json)

        x = json['x']
        y = json['y']

        return Position(x=x, y=y)

    @staticmethod
    def parse_position_array(json_list):
        return list(map(Importer.parse_position, json_list))

    @staticmethod
    def parse_food(json):
        json = CaseInsensitiveDict(json)

        x = json['x']
        y = json['y']

        return Food(x=x, y=y)

    @staticmethod
    def parse_food_array(json_list):
        return list(map(Importer.parse_food, json_list))

    @staticmethod
    def parse_hazard(json):
        json = CaseInsensitiveDict(json)

        x = json['x']
        y = json['y']

        return Hazard(x=x, y=y)

    @staticmethod
    def parse_hazard_array(json_list):
        return list(map(Importer.parse_hazard, json_list))

    @staticmethod
    def load_replay_file(filepath):
        import json
        with open(filepath, "r") as f:
            json_data = json.load(f)
        return Importer.parse_replay(json_data)

    @staticmethod
    def parse_replay(json):
        game = Importer.parse_game_info(json['game'])
        turns = json['total_turns']
        move_list = [Importer.parse_board(b) for b in json['moves']]

        return game, turns, move_list
