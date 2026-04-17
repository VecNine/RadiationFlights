import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any
from hapiclient import hapi

from data_converter.interfaces.interface_space_weather import SpaceWeatherProvider
from data_converter.mappers.omni_mapper import OmniMapper


class HapiRemoteProvider(SpaceWeatherProvider):
    """Implementacja dla dynamicznego pobierania danych."""

    def __init__(self):
        self.server = 'https://cdaweb.gsfc.nasa.gov/hapi'
        self.dataset = 'OMNI2_H0_MRG1HR'
        self.params = [
            'ABS_B1800', 'BZ_GSM1800', 'T1800', 'N1800', 'V1800', 'Pressure1800',
            'PR-FLX_101800', 'PR-FLX_301800', 'PR-FLX_601800', 'R1800',
            'F10_INDEX1800', 'KP1800', 'DST1800', 'AP_INDEX1800'
        ]

    def fetch_data(self, target_dt: datetime) -> Dict[str, Any]:
        """
        Zwraca dane dla podanej daty.
        :param target_dt: data
        :return: dane dla daty
        """
        target_dt_utc = target_dt if target_dt.tzinfo else target_dt.replace(tzinfo=None)

        start_str = (target_dt_utc - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        stop_str = (target_dt_utc + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

        data, meta = hapi(self.server, self.dataset, ",".join(self.params), start_str, stop_str)

        if len(data) == 0:
            raise ValueError("Brak danych w NASA HAPI dla podanego zakresu.")

        df = pd.DataFrame(data)
        df['Time'] = pd.to_datetime(df['Time'].str.decode('utf-8'), utc=True)

        for p in meta['parameters']:
            col = p['name']
            if (fv := p.get('fill')) is not None:
                df[col] = df[col].replace(float(fv), np.nan)

        closest_row = self._find_closest(df, target_dt_utc)
        return OmniMapper.map_to_json(closest_row, target_dt)