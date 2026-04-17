import pandas as pd
from datetime import datetime
from typing import Dict, Any

class OmniMapper:
    """Odpowiada wyłącznie za mapowanie nazw kolumn NASA OMNI na format JSON."""

    _MAPPING = {
        'KP1800': 'Index_Kp',
        'DST1800': 'Index_Dst',
        'AP_INDEX1800': 'Index_Ap',
        'R1800': 'Solar_sunspots',
        'F10_INDEX1800': 'Solar_f107',
        'ABS_B1800': 'SW_B',
        'BZ_GSM1800': 'SW_Bz',
        'V1800': 'SW_V',
        'N1800': 'SW_density',
        'T1800': 'SW_temperature',
        'Pressure1800': 'SW_pressure',
        'PR-FLX_101800': 'Particles_P10',
        'PR-FLX_301800': 'Particles_P30',
        'PR-FLX_601800': 'Particles_P60'
    }

    @classmethod
    def map_to_json(cls, row: pd.Series, target_dt: datetime) -> Dict[str, Any]:
        """Konwertuje wiersz z OMNI na słownik wynikowy."""

        result = {
            "Requested_Datetime": str(target_dt),
            "Found_OMNI_Time": str(row['Time'])
        }

        for nasa_name, json_name in cls._MAPPING.items():
            if nasa_name in row:
                val = row[nasa_name]
                result[json_name] = val if pd.notna(val) else None

        return result