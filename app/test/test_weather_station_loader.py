import os
import tempfile
from datetime import datetime

import pytest
from sqlalchemy import create_engine

from main import WeatherStationLoader


@pytest.fixture(scope="module")
def engine():
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def data():
    # Create a temporary directory and generate some test data
    with tempfile.TemporaryDirectory() as tmpdir:
        years = ["2019", "2020"]
        for year in years:
            os.makedirs(os.path.join(tmpdir, year))
            for i in range(1, 13):
                date_str = f"{year}-{i:02d}-01"
                date = datetime.strptime(date_str, "%Y-%m-%d")
                filename = f"{date.strftime('%Y%m')}.csv"
                path = os.path.join(tmpdir, year, filename)
                with open(path, "w") as f:
                    f.write(
                        f"""\
#;STATION;DATE;HOUR;PRECIPITATION;PRECIPITATION_TYPE;TEMPERATURE;HUMIDITY;WIND_DIRECTION;WIND_SPEED;GLOBAL_RADIATION;UV_RADIATION;MAX_WIND_GUST;MAX_WIND_GUST_DIRECTION;PRESSURE;PRESSURE_SEA_LEVEL
#;-------;----;----;-------------;-----------------;-----------;--------;-------------;----------;----------------;------------;-------------;----------------------;--------;------------------
#;  82598;{date_str};00:00;           0.0;                 ;       22.0;      60;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};01:00;           0.0;                 ;       21.0;      63;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};02:00;           0.0;                 ;       20.0;      67;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};03:00;           0.0;                 ;       19.0;      71;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};04:00;           0.0;                 ;       18.0;      75;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};05:00;           0.0;                 ;       17.0;      80;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};06:00;           0.0;                 ;       16.0;      85;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};07:00;           0.0;                 ;       15.0;      90;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};08:00;           0.0;                 ;       14.0;      95;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};09:00;           0.0;                 ;       13.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};10:00;           0.0;                 ;       12.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};11:00;           0.0;                 ;       11.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};12:00;           0.0;                 ;       10.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};13:00;           0.0;                 ;        9.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};14:00;           0.0;                 ;        8.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};15:00;           0.0;                 ;        7.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};16:00;           0.0;                 ;        6.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};17:00;           0.0;                 ;        5.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};18:00;           0.0;                 ;        4.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};19:00;           0.0;                 ;        3.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};20:00;           0.0;                 ;        2.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};21:00;           0.0;                 ;        1.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};22:00;           0.0;                 ;        0.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
#;  82598;{date_str};23:00;           0.0;                 ;        0.0;     100;          0.0;       1.0;             0.0;         0.0;             0.0;                   ;   1013;                  
"""
                    )
        yield tmpdir


def test_load_all(engine, data):
    loader = WeatherStationLoader(engine)
    loader.load_all()
    conn = engine.connect()
    result = conn.execute("SELECT COUNT(*) FROM WEATHER.WEATHER_TABLE").scalar()
    assert result == 48


def test_load_file(engine, data):
    loader = WeatherStationLoader(engine)
    loader.load_file("2019", "201901.csv")
    conn = engine.connect()
    result = conn.execute("SELECT COUNT(*) FROM WEATHER.WEATHER_TABLE").scalar()
    assert result == 24


def test_load_file_missing_data(engine, data):
    loader = WeatherStationLoader(engine)
    loader.load_file("2019", "201902.csv")
    conn = engine.connect()
    result = conn.execute("SELECT COUNT(*) FROM WEATHER.WEATHER_TABLE").scalar()
    assert result == 0


def test_load_file_invalid_data(engine, data):
    loader = WeatherStationLoader(engine)
    loader.load_file("2019", "201903.csv")
    conn = engine.connect()
    result = conn.execute("SELECT COUNT(*) FROM WEATHER.WEATHER_TABLE").scalar()
    assert result == 0
