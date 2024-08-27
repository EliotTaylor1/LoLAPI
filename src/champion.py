import logging
from src.utils import load_champion_data


class Champion:
    logger = logging.getLogger(__name__)

    def __init__(self, champion_id: str):
        self._champion_name = None
        self._champion_id = champion_id
        self._champion_abilities = {}
        self._set_champion_data()

    def _set_champion_data(self):
        info = load_champion_data()
        data = info.get("data")
        for champion_key, champion_data in data.items():
            if champion_data.get("key") == str(self._champion_id):
                self._champion_name = champion_data.get("id")
                return
        else:
            Champion.logger.info(f"{data.get('key')} not found in data.")

    def get_name(self):
        return self._champion_name
