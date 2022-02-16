from agents.KILabAgentGroup8.KILabAgent import KILabAgent
from environment.Battlesnake.server import BattlesnakeServer


agent = KILabAgent()  # TODO select your agent
port = 8008  # TODO set your port


BattlesnakeServer.start_server(
    agent=agent,
    port=port
)