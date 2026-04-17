import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any

class SpaceWeatherProvider(ABC):
    """Interfejs dla dostawców danych z wbudowaną logiką wyszukiwania najbliższego punktu."""

    @abstractmethod
    def fetch_data(self, target_dt: datetime) -> Dict[str, Any]:
        pass

    def _find_closest(self, df: pd.DataFrame, target_dt: datetime) -> pd.Series:

        if df.empty:
            raise ValueError("Zbiór danych jest pusty.")

        df = df.sort_values('Time').copy()

        if target_dt.tzinfo is not None:
            if df['Time'].dt.tz is None:
                df['Time'] = df['Time'].dt.tz_localize('UTC')
            else:
                df['Time'] = df['Time'].dt.tz_convert('UTC')

        idx = df['Time'].searchsorted(target_dt)

        if idx == 0:
            return df.iloc[0]
        if idx >= len(df):
            return df.iloc[-1]

        before = df.iloc[idx - 1]
        after = df.iloc[idx]

        if abs(after['Time'] - target_dt) < abs(before['Time'] - target_dt):
            return after
        return before