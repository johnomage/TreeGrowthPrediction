
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import os
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv


# def separate_caps(city_query: str) -> str:
#     """
#     Insert spaces before each capital letter in the city name.

#     Parameters:
#         city_query (str): The city name to format.

#     Returns:
#         str: The formatted city name with spaces before capital letters.
#     """
#     return ''.join([' ' + i if i.isupper() else i for i in city_query]).strip()



def get_city_name(latitude: float, longitude: float) -> str:
    """
    Get the city name from given latitude and longitude.

    Parameters:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        str: The name of the city or an error message if not found.
    """
    load_dotenv()
    
    try:
        geolocator = Nominatim(user_agent=os.getenv('USER_AGENT'))
        location = geolocator.reverse((latitude, longitude), exactly_one=True, timeout=10)

        if location and "address" in location.raw:
            address = location.raw["address"]
            city_name = (
                address.get("suburb")
                or address.get("village")
                or address.get("town")
                or address.get("city")
                or pd.NA
            )
            return city_name
        else:
            return pd.NA
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error: {e}")
        return "Error fetching city name"
    

def get_city_coordinates(city_query: str):
    """
    Get the coordinates (latitude and longitude) for a given city name.

    Parameters:
        city_query (str): The name of the city to search for.

    Returns:
        tuple or None: A tuple containing latitude and longitude if found, else None.
    """
    try:
        geolocator = Nominatim(user_agent="city_coordinates_for_bio_lab")
        location = geolocator.geocode(city_query, timeout=10)
        
        if location:
            return (location.latitude, location.longitude)
        else:
            return np.nan, np.nan
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error: {e}")
        return np.nan, np.nan




def get_elevation(lat: float, long: float):
    """
    Retrieve the elevation of a location specified by latitude and longitude.

    Args:
        lat (float): The latitude of the location.
        long (float): The longitude of the location.

    Returns:
        float: The elevation in meters if the request is successful, \
               or np.nan if the request fails or the elevation is not available.
    """
    query = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{long}"
    response = requests.get(query)
    if response:
        return response.json()['results'][0]['elevation']
    return np.nan