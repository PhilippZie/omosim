import utils
import geopandas as gpd
import numpy as np
import pandas as pd

def test_activity_times(nuremberg):

    trips = nuremberg.omosim_trips.sort_values(['day', 'id', 'legID']).copy()
    start_times_per_agent = trips[trips['type'] == 'Trip'].groupby(['day', 'id'])['startTime'].agg(list)

    trips['start_td'] = pd.to_timedelta(trips['startTime'] + ":00")
    trips['next_start_td'] = trips.groupby(['day', 'id'])['start_td'].shift(-1)

    work_trips = trips[(trips['stopAct'] == 'WORK') & (trips['next_start_td'].notna())]

    # Get span from starting the commute to leaving work in hours
    work_span_hours = (work_trips['next_start_td'] - work_trips['start_td']).dt.total_seconds() / 3600.0
    mean_span_hours = work_span_hours.mean()

    first_trips = []
    for day in start_times_per_agent:
        first_trips.append(day[0])

    time_deltas = pd.to_timedelta([f"{t}:00" for t in first_trips])
    mean_start_time = time_deltas.mean()

    lower_bound = pd.Timedelta("06:00:00")

    assert mean_span_hours >= 5.0, f"Unexpectedly low mean time at work (commute + work time: {mean_span_hours:.2f})"

    assert lower_bound <= mean_start_time, (
        f"Expected mean departure after {lower_bound}, but got {mean_td}"
    )