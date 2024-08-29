import os
os.chdir("/home/canyon/hackday-q2-2024-open-earth-foundation")
from src.utils import *
import censusdis.data as ced
import matplotlib.pyplot as plt
from censusdis.states import ALL_STATES_AND_DC
import pandas as pd
import warnings
warnings.simplefilter("ignore", UserWarning)
alber_eq_us = "EPSG:5070"
DATASET = "acs/acs5"
YEAR = 2020
CENSUS_VARS = {"NAME" : "NAME",
               "B01001_001E" : "total_pop",
               "B25003_001E": "total_households",
               "B08201_002E" : "households_no_vehicle",
               "B08604_001E" : "worker_pop"
}

states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
    'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming',
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
    'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN',
    'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
    'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
    'VA', 'WA', 'WV', 'WI', 'WY'
]
def find_state(address):
    for state in states:
        if state in address:
            return state
    return None

state_to_fips = {
    'Alabama': '01',
    'Alaska': '02',
    'Arizona': '04',
    'Arkansas': '05',
    'California': '06',
    'Colorado': '08',
    'Connecticut': '09',
    'Delaware': '10',
    'Florida': '12',
    'Georgia': '13',
    'Hawaii': '15',
    'Idaho': '16',
    'Illinois': '17',
    'Indiana': '18',
    'Iowa': '19',
    'Kansas': '20',
    'Kentucky': '21',
    'Louisiana': '22',
    'Maine': '23',
    'Maryland': '24',
    'Massachusetts': '25',
    'Michigan': '26',
    'Minnesota': '27',
    'Mississippi': '28',
    'Missouri': '29',
    'Montana': '30',
    'Nebraska': '31',
    'Nevada': '32',
    'New Hampshire': '33',
    'New Jersey': '34',
    'New Mexico': '35',
    'New York': '36',
    'North Carolina': '37',
    'North Dakota': '38',
    'Ohio': '39',
    'Oklahoma': '40',
    'Oregon': '41',
    'Pennsylvania': '42',
    'Rhode Island': '44',
    'South Carolina': '45',
    'South Dakota': '46',
    'Tennessee': '47',
    'Texas': '48',
    'Utah': '49',
    'Vermont': '50',
    'Virginia': '51',
    'Washington': '53',
    'West Virginia': '54',
    'Wisconsin': '55',
    'Wyoming': '56'
}
def get_fips_code(state_name):
    return state_to_fips.get(state_name, 'State not found')

def get_city_interpolation():

    city_gdf = load_data_from_ts3("Geometries/US_city_geometries.geojson")
    city_gdf["state"] = city_gdf['display_name'].apply(find_state)
    city_gdf["fip"] = city_gdf['state'].apply(get_fips_code)

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

        return out.to_crs(input_crs)

    US_interpolated_arr = []
    for fips in range(57):
        if fips < 10:
            fips = f"0{fips}"
        fips = str(fips)
        print(f"Processing state: {fips}")
        try:
            STATE_tracts = ced.download(DATASET, YEAR, CENSUS_VARS, state=fips, county = "*",tract = "*", with_geometry=True).rename(CENSUS_VARS, axis = 1).to_crs(4326)
        except:
            print(f"Invalid state code: {fips}")
            continue

        STATE_interpolated = areal_interpolation(city_gdf[city_gdf["fip"]==fips], STATE_tracts, ['total_pop', 'total_households', 'households_no_vehicle', 'worker_pop'], ['interpolated_pop', 'interpolated_households', 'interpolated_households_no_vehicle', 'interpolated_workers'])
        #STATE_interpolated_city_only = STATE_interpolated[STATE_interpolated["addresstype"]=='city']
        STATE_interpolated.set_index("locode")
        STATE_interpolated = STATE_interpolated[~STATE_interpolated.index.duplicated(keep='first')]
        US_interpolated_arr.append(STATE_interpolated)
        print(f"Finished processing state: {fips}")
    return pd.concat(US_interpolated_arr)
