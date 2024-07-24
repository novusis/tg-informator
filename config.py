import json
import os

import utils


class Config:
    APP_CONFIG_PATH = f"data/app_config_{os.getenv('CONFIG', 'dev')}.json"

    with open(APP_CONFIG_PATH, 'r') as f:
        app_config = json.load(f)

    # with open("messages/game_config.json", 'r') as f:
    #     game_config = json.load(f)

    @staticmethod
    def app_url(version):
        return Config.app('app_url') + "?r=" + version

    @staticmethod
    def app(field):
        game_config = Config.APP_CONFIG_PATH
        if not Config.app_config:
            utils.log_error(f"GameConfig.get_app_config > error no app config <{game_config}>")
            return ""

        if 'application' not in Config.app_config:
            utils.log_error(f"GameConfig.get_app_config > error not <application> node in config <{game_config}>")
            return ""

        if field not in Config.app_config['application']:
            utils.log_error(f"GameConfig.get_app_config > error not field <application.{field}> in config <{game_config}>")
            return ""

        return Config.app_config['application'][field]