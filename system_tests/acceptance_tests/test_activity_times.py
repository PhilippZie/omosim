import utils
import geopandas as gpd
import numpy as np
import pandas as pd

def test_activity_times(nuremberg):

    trips = nuremberg.omosim_trips
    start_times_per_agent = trips[trips['type'] == 'Trip'].groupby(['day', 'id'])['startTime'].agg(list)

    first_trips = []
    for day in start_times_per_agent:
        first_trips.append(day[0])

    time_deltas = pd.to_timedelta([f"{t}:00" for t in first_trips])
    mean_start_time = time_deltas.mean()

    lower_bound = pd.Timedelta("06:00:00")

    assert lower_bound <= mean_start_time, (
        f"Expected mean departure after {lower_bound}, but got {mean_td}"
    )