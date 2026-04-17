import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any

from data_converter.interfaces.interface_space_weather import SpaceWeatherProvider
from data_converter.mappers.omni_mapper import OmniMapper


class LocalCsvProvider(SpaceWeatherProvider):
    """Implementacja dla plików lokalnie pobranych"""

    def __init__(self, data_dir: str = 'omni_data_monthly'):
        self.data_dir = data_dir

    def fetch_data(self, target_dt: datetime) -> Dict[str, Any]:
        """
        Zwraca dane dla podanej daty.
        :param target_dt: data
        :return: dane dla podanego dnia
        """
        file_label = target_dt.strftime('%Y_%m')
        file_path = os.path.join(self.data_dir, f'omni_hourly_{file_label}.csv')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Brak danych dla daty {file_label} (plik {file_path} nie istnieje).")

        df = pd.read_csv(file_path)
        df['Time'] = pd.to_datetime(df['Time'])

        closest_row = self._find_closest(df, target_dt)
        return OmniMapper.map_to_json(closest_row, target_dt)