import time


class RulesetSettings:

    def __init__(
            self,
            foodSpawnChance=15,
            minimumFood=1,
            hazardDamagePerTurn=14,
            royale_shrinkEveryNTurns=25,
            squad_allowBodyCollisions: bool=True,
            squad_sharedElimination: bool=True,
            squad_sharedHealth: bool=True,
            squad_sharedLength: bool=True,
    ):
        self.foodSpawnChance = foodSpawnChance
        self.minimumFood = minimumFood
        self.hazardDamagePerTurn = hazardDamagePerTurn
        self.royale_shrinkEveryNTurns = royale_shrinkEveryNTurns
        self.squad_allowBodyCollisions = squad_allowBodyCollisions
        self.squad_sharedElimination = squad_sharedElimination
        self.squad_sharedHealth = squad_sharedHealth
        self.squad_sharedLength = squad_sharedLength
        self.seed = int(time.time())

    def export_json(self):
        return {
            'foodSpawnChance': self.foodSpawnChance,
            'minimumFood': self.minimumFood,
            'hazardDamagePerTurn': self.hazardDamagePerTurn,
            'royale': {
                'shrinkEveryNTurns': self.royale_shrinkEveryNTurns
            },
            'squad': {
                'allowBodyCollisions': self.squad_allowBodyCollisions,
                'sharedElimination': self.squad_sharedElimination,
                'sharedHealth': self.squad_sharedHealth,
                'sharedLength': self.squad_sharedLength,
            }
        }
