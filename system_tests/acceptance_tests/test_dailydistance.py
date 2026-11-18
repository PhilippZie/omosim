import utils
import geopandas as gpd
import numpy as np
import pandas as pd

def test_avg_daily_distances(nuremberg):

    trips = nuremberg.omosim_trips
    daily_per_agent = trips[trips['type'] == 'Trip'].groupby(['day', 'id'])['distanceKilometer'].sum()

    p25_dist = daily_per_agent.quantile(0.25)
    median_dist = daily_per_agent.median()
    p75_dist = daily_per_agent.quantile(0.75)
    mean_dist = daily_per_agent.mean()
    max_dist = daily_per_agent.max()

    # TODO: expect mid values here
    expected_avg = 23.3
    expected_median = 13.3
    expected_p25 = 4.2
    expected_p75 = 29.5
    expected_max = 300.0

    ub = 2.0
    lb = 0.25

    assert expected_median * lb <= median_dist <= expected_median * ub, f"Median daily distance out of bounds: {median_dist:.2f} km"
    assert expected_avg * lb <= mean_dist <= expected_avg * ub, f"Unexpected average distance value: {mean_dist:.2f} km"
    assert expected_p25 * lb <= p25_dist <= expected_p25 * ub, f"P25 travel distance unrealistic: {p25_dist:.2f} km"
    assert expected_p75 * lb <= p75_dist <= expected_p75 * ub, f"P75 travel distance unrealistic: {p75_dist:.2f} km"
    assert max_dist <= expected_max, f"Unrealistic outlier agent detected: max daily distance is {max_dist:.2f} km"

def test_destination_distribution(nuremberg):
    pass

def test_mode_shares(nuremberg):

    trips = nuremberg.omosim_trips
    modes_per_agent = trips[trips['type'] == 'Trip'].groupby(['day', 'id'])['mode'].agg(list)

    bins = [0, 1, 2, 5, 10, 20, 50, np.inf]
    labels = ['<1km', '1-2km', '2-5km', '5-10km', '10-20km', '20-50km', '>50km']

    trips['distance_bin'] = pd.cut(
        trips['distanceKilometer'],
        bins=bins,
        labels=labels,
        right=False
    )

    modal_share = pd.crosstab(
        index=trips['distance_bin'],
        columns=trips['mode'],
        normalize='index'
    ) * 100

    # Check if the foot shares of very long and very short trips make sense
    if 'FOOT' in modal_share.columns and '<1km' in modal_share.index:
        foot_share_short = modal_share.loc['<1km', 'FOOT']
        assert foot_share_short >= 15.0, f"FOOT share for <1km trips too low: {foot_share_short:.1f}%"

    if 'FOOT' in modal_share.columns and '>50km' in modal_share.index:
        foot_share_long = modal_share.loc['>50km', 'FOOT']
        assert foot_share_long < 1.0, f"Unrealistic walking trips >50km: {foot_share_long:.1f}%"


def test_activity_times(nuremberg):

    trips = nuremberg.omosim_trips
    start_times_per_agent = trips[trips['type'] == 'Trip'].groupby(['day', 'id'])['startTime'].agg(list)

    first_trips = []
    for day in start_times_per_agent:
        first_trips.append(day[0])

    time_deltas = pd.to_timedelta([f"{t}:00" for t in first_trips])
    mean_start_time = time_deltas.mean()

    lower_bound = pd.Timedelta("05:00:00")

    assert lower_bound <= mean_start_time, (
        f"Expected mean departure after {lower_bound}, but got {mean_td}"
    )
