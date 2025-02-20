import yaml

from configs.config_definition import AllConfig


class ConfigManager:
    ''' 設定を管理するクラス '''
    _config = None

    @staticmethod
    def load_config(file_path: str):
        ''' YAMLファイルを読み込んでAllConfigにマッピング '''
        with open(file_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
        ConfigManager._config = AllConfig(**config_dict)

    @staticmethod
    def get_display():
        ''' display用の設定値を取得する '''
        return ConfigManager._config.display

    @staticmethod
    def get_game():
        ''' game用の設定値を取得する '''
        return ConfigManager._config.game

    @staticmethod
    def get_block():
        ''' block用の設定値を取得する '''
        return ConfigManager._config.block
