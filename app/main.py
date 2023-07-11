import os
import re

import pandas as pd
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


load_dotenv(find_dotenv())

DB_CONN = os.getenv("DB_CONN")
DATA_PATH = os.getenv("DATA_PATH")


class WeatherStationLoader:
    """
    A class used to load weather station data into a database.

    Attributes
    ----------
    engine : sqlalchemy.engine.base.Engine
        The SQLAlchemy engine used to connect to the database.

    Methods
    -------
    load_all()
        Loads all weather station data files into the database.
    load_file(year: str, file: str)
        Loads a single weather station data file into the database.
    """
    def __init__(self, engine: Engine):
        self.engine = engine

    def load_all(self) -> None:
        years_dir = os.listdir(DATA_PATH)
        for year in years_dir:
            files_dir = os.listdir(os.path.join(str(DATA_PATH), year))
            for file in files_dir:
                self.load_file(year, file)

    def load_file(self, year: str, file: str) -> None:
        path = os.path.join(str(DATA_PATH), year, file)
        with open(path, "r+") as f:
            location_header = [next(f) for x in range(8)]
            latitude = None
            longitude = None
            altitude = None
            latitude_match = re.search(":;{1,}(.+?)(;|\n)", location_header[4])
            if latitude_match:
                latitude = latitude_match.group(1)
            longitude_match = re.search(":;{1,}(.+?)(;|\n)", location_header[5])
            if longitude_match:
                longitude = longitude_match.group(1)
            altitude_match = re.search(":;{1,}(.+?)(;|\n)", location_header[6])
            if altitude_match:
                altitude = altitude_match.group(1)

            df = pd.read_csv(
                path, sep=";", encoding="latin-1", usecols=[0, 1, 2, 6, 7, 15, 18]
            )
            df = df.rename(
                columns={
                    "data_medicao": "measurement_date",
                    "hora_utc": "hour_utc",
                    "precipitacao_total": "total_precipitation",
                    "radiacao_global": "global_radiation",
                    "temperatura_ar": "air_temperature",
                    "umidade_relativa": "relative_humidity",
                    "velocidade_vento": "wind_speed",
                }
            )
            df["latitude"] = latitude
            df["longitude"] = longitude
            df["altitude"] = altitude
            df["measurement_date"] = pd.to_datetime(
                df["measurement_date"], format="%Y-%m-%d"
            )
            df["year"] = df["measurement_date"].dt.year
            df["month"] = df["measurement_date"].dt.month
            df["day"] = df["measurement_date"].dt.day
            df["day_of_year"] = df["measurement_date"].dt.dayofyear
            df["week_of_year"] = df["measurement_date"].dt.isocalendar().week

            df = df.astype(
                {
                    "total_precipitation": float,
                    "global_radiation": float,
                    "air_temperature": float,
                    "relative_humidity": float,
                    "wind_speed": float,
                    "year": int,
                    "month": int,
                    "day": int,
                    "day_of_year": int,
                    "week_of_year": int,
                }
            )
            df = df.sort_values(["measurement_date", "hour_utc"])
            df = df.dropna()
            df.to_sql(
                "WEATHER_TABLE",
                con=self.engine,
                schema="WEATHER",
                if_exists="append",
                index=False,
            )


def main() -> None:
    engine = create_engine(str(DB_CONN))
    weather_station_loader = WeatherStationLoader(engine)
    weather_station_loader.load_all()


if __name__ == "__main__":
    main()
