
import utils
import geopandas as gpd
import numpy as np
import pandas as pd

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

    # Check if the shares of very long and very short trips make sense
    if 'FOOT' in modal_share.columns and '<1km' in modal_share.index:
        foot_share_short = modal_share.loc['<1km', 'FOOT']
        assert foot_share_short >= 50.0, f"FOOT share for <1km trips too low: {foot_share_short:.1f}%"

    if 'FOOT' in modal_share.columns and '>50km' in modal_share.index:
        foot_share_long = modal_share.loc['>50km', 'FOOT']
        assert foot_share_long < 1.0, f"Unrealistic walking trips >50km: {foot_share_long:.1f}%"

    if 'BICYCLE' in modal_share.columns and '>50km' in modal_share.index:
        bicycle_share_long = modal_share.loc['>50km', 'BICYCLE']
        assert bicycle_share_long < 20.0, f"Unrealistic amount of bicycle trips >50km: {bicycle_share_long:.1f}%"
