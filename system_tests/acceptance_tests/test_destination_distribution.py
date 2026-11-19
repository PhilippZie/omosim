import utils
import geopandas as gpd
import numpy as np
import pandas as pd


def test_destination_distribution(nuremberg):

    trips = nuremberg.omosim_trips


