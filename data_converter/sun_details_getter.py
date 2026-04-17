import pandas as pd
from typing import Dict, Any

from data_converter.interfaces.interface_space_weather import SpaceWeatherProvider
from data_converter.model.local_csv_provider import LocalCsvProvider
from data_converter.model.remote_csv_provider import HapiRemoteProvider


class SpaceWeatherService:
    """Serwis spinający logikę, zależy od abstrakcji a nie od konkretu."""

    def __init__(self, provider: SpaceWeatherProvider):
        self.provider = provider

    def get_data(self, date_str: str) -> Dict[str, Any]:
        try:
            target_dt = pd.to_datetime(date_str, utc=True)
            return self.provider.fetch_data(target_dt)
        except Exception as e:
            return {"error": str(e), "status": "failed"}


if __name__ == "__main__":
    data_lotu = "2022-03-23 23:54:16"

    # Użycie API (HAPI)
    # service_remote = SpaceWeatherService(HapiRemoteProvider())
    # print("Wynik API:", service_remote.get_data(data_lotu))

    # Użycie Lokalnych Plików
    service_local = SpaceWeatherService(LocalCsvProvider(data_dir='data/omniNASA'))
    print("Wynik Lokalny:", service_local.get_data(data_lotu))