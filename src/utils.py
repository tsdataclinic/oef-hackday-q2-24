import ts3
from io import StringIO
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import numpy as np
import os
import censusdis.data as ced

def load_data_from_ts3(path):
    
    """
    Loads a csv from ts3
    """
    
    client = ts3.get_ts3_client()
    bucket_name = "q2-24-dataclinic-open-earth-hackday"

    response = client.get_object(
            Bucket= bucket_name, Key = path
    )

    bytes = response["Body"].read()
    s = str(bytes, "utf-8")
    data = StringIO(s)
    if path[-3:] == "csv":
        df = pd.read_csv(data, low_memory=False, index_col=0)
    elif path[-7:] == "geojson":
        df = gpd.read_file(data)
    
    return df

def write_to_ts3(df, path):
    
    """
    Writes a file out to ts3
    """
    client = ts3.get_ts3_client()
    bucket_name = "q2-24-dataclinic-open-earth-hackday"

    
    if path[-3:] == "csv":
        df_save = df.to_csv()
    elif path[-7:] == "geojson":
        df_save = df.to_json()
        
    client.put_object(
        Bucket=bucket_name, Key=path, Body=df_save
    )
    
def areal_interpolation(city_bounds, census_tracts, cols_to_interpolate, out_col_names, id_col = "place_id", planar_crs = "5070"):
    input_crs = city_bounds.crs

    city_bounds = city_bounds.to_crs(planar_crs).explode(index_parts=False) 
    city_bounds = city_bounds[city_bounds.geom_type == "Polygon"]
    census_tracts = census_tracts.to_crs(planar_crs)

    census_tracts["preclipped_area"] = census_tracts.area

    cities_clipped_tracts = city_bounds.overlay(census_tracts, how='intersection', keep_geom_type=False)
    cities_clipped_tracts["area_proportion"]  = cities_clipped_tracts.area / cities_clipped_tracts["preclipped_area"]
    for original_col, new_col in zip(cols_to_interpolate, out_col_names):
        cities_clipped_tracts[new_col] = cities_clipped_tracts[original_col] * cities_clipped_tracts["area_proportion"]
    
    city_interpolated_total = cities_clipped_tracts.groupby(id_col)[out_col_names].sum().reset_index()
    out = city_bounds.merge(city_interpolated_total)
    out = out.dissolve(by = "place_id").reset_index()

    return out.to_crs(input_crs)