import utils
import geopandas as gpd
import numpy as np
import pandas as pd


def test_daily_distances(nuremberg):

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
    lb = 0.5

    assert expected_median * lb <= median_dist <= expected_median * ub, f"Median daily distance out of bounds: {median_dist:.2f} km"
    assert expected_avg * lb <= mean_dist <= expected_avg * ub, f"Unexpected average distance value: {mean_dist:.2f} km"
    assert expected_p25 * lb <= p25_dist <= expected_p25 * ub, f"P25 travel distance unrealistic: {p25_dist:.2f} km"
    assert expected_p75 * lb <= p75_dist <= expected_p75 * ub, f"P75 travel distance unrealistic: {p75_dist:.2f} km"
    assert max_dist <= expected_max, f"Unrealistic outlier agent detected: max daily distance is {max_dist:.2f} km"


