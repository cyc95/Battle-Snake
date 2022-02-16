from environment.Battlesnake.model.RulesetSettings import RulesetSettings


class GameInfo:

    def __init__(self, game_id, ruleset_name, ruleset_version, timeout, ruleset_settings: RulesetSettings):
        self.id = game_id
        self.ruleset = {"name": ruleset_name, "version": ruleset_version, 'settings': ruleset_settings.export_json()}
        self.ruleset_settings: RulesetSettings = ruleset_settings
        self.timeout = timeout  # timeout in ms
        self.source = "KI-Labor"

    def export_json(self):
        return {
            "id": self.id,
            "ruleset": self.ruleset,
            "timeout": self.timeout,
            "source": self.source
        }
