from typing import Optional

import cherrypy

from environment.Battlesnake.agents.BaseAgent import BaseAgent
from environment.Battlesnake.importer.Importer import Importer
from environment.Battlesnake.model.Direction import Direction


class BattlesnakeServer:

    def __init__(self, agent: BaseAgent):
        self.agent: BaseAgent = agent

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, **params):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data

        data = {
            "apiversion": "1",
            "author": self.agent.get_author(),
            "color": self.agent.get_color_hex(),
            "head": self.agent.get_head(),
            "tail": self.agent.get_tail()
        }

        # filter None values
        data = {k: v for k, v in data.items() if v is not None}

        if 'kilab' in params:

            name = self.agent.get_name()
            data['name'] = name

        return data

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.

        data = cherrypy.request.json
        game_info, turn, board, you = Importer.parse_request(data)
        self.agent.start(game_info=game_info, turn=turn, board=board, you=you)

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".

        data = cherrypy.request.json
        # print(data)
        game_info, turn, board, you = Importer.parse_request(data)
        move_result = self.agent.move(game_info=game_info, turn=turn, board=board, you=you)
        move = move_result.direction
        move = BattlesnakeServer.decode_direction(move)

        print(f"MOVE: {move}")
        return {
            "move": move
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        game_info, turn, board, you = Importer.parse_request(data)
        self.agent.end(game_info=game_info, turn=turn, board=board, you=you)

        print("END")
        return "ok"

    @staticmethod
    def decode_direction(d: Direction):
        if d == Direction.UP:
            return 'up'
        elif d == Direction.DOWN:
            return 'down'
        elif d == Direction.LEFT:
            return 'left'
        elif d == Direction.RIGHT:
            return 'right'
        else:
            return None

    @staticmethod
    def encode_direction(s: str) -> Optional[Direction]:
        if s == 'up':
            return Direction.UP
        elif s == 'down':
            return Direction.DOWN
        elif s == 'left':
            return Direction.LEFT
        elif s == 'right':
            return Direction.RIGHT
        else:
            return None

    @staticmethod
    def start_server(agent: BaseAgent, port: int):
        if port is None:
            raise ValueError('please select your port')

        server = BattlesnakeServer(agent)
        cherrypy.config.update({"server.socket_host": "0.0.0.0"})
        cherrypy.config.update(
            {
                'engine.autoreload.on': False,
                "server.socket_port": port
            }
        )

        print("Starting Battlesnake Server...")
        cherrypy.quickstart(server)
