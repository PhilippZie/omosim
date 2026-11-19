import utils
import geopandas as gpd
import numpy as np
import pandas as pd


def test_destination_distribution(nuremberg):

    trips = nuremberg.omosim_trips

    squares_1km = trips['GITTER_ZO_1km']
    squares_5km = trips['GITTER_ZO_5km']
    squares_500m = trips['GITTER_ZO_500m']

    num_unique_500m = squares_500m.nunique()
    num_unique_1km = squares_1km.nunique()
    num_unique_5km = squares_5km.nunique()

    num_squares_work = trips.loc[trips['stopAct'] == 'WORK', 'GITTER_ZO_1km'].nunique()
    num_squares_shopping = trips.loc[trips['stopAct'] == 'SHOPPING', 'GITTER_ZO_1km'].nunique()
    num_squares_home = trips.loc[trips['stopAct'] == 'HOME', 'GITTER_ZO_1km'].nunique()

    amount_nan_cells = trips['GITTER_ZO_1km'].isna().mean()

    assert amount_nan_cells < 0.05, f"Amount of cells ending outside the grid unexpectedly high: {amount_nan_cells}%"

    assert num_squares_work < num_squares_home, (
        f"Expected more unique home destinations ({num_squares_home}) than work: {num_squares_work}"
    )
    assert num_squares_shopping < num_squares_home, (
        f"Expected more unique home destinations ({num_squares_home}) than shopping: {num_squares_shopping}"
    )

    assert num_unique_1km > 10, f'All destinations are concentrated in only very few 1km cells {num_unique_1km}%'
    assert num_unique_500m > 20, f'All destinations are concentrated in only very few 500m cells {num_unique_500m}%'
    assert num_unique_5km > 5, f'All destinations are concentrated in only very few 5km cells {num_unique_5km}%'


