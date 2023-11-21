import requests
import pandas as pd


class CountryDataFetcher:
    """
    A class to fetch and process country data from a REST API.

    Attributes:
        url (str): The URL of the API to fetch country data.
        countries_data (list): A list to store processed country data.
    """

    def __init__(self):
        """
        Initializes the CountryDataFetcher with the API URL and an empty list for countries' data.
        """
        self.url = "https://restcountries.com/v3.1/all"
        self.countries_data = []

    def fetch_data(self):
        """
        Fetches data from the API.

        Returns:
            list: A list of dictionaries containing country data.

        Raises:
            Exception: If the API request fails.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data from the API.")

    def process_data(self, data):
        """
        Processes the raw data fetched from the API.

        Args:
            data (list): The raw data from the API as a list of dictionaries.
        """
        for country in data:
            country_info = {
                "Country": country.get("name", {}).get("common", "Unknown"),
                "Capital": country.get("capital", [None])[0],
                "Population": country.get("population", None),
                "Area": country.get("area", None),
                "Region": country.get("region", None),
                "Subregion": country.get("subregion", None),
                "Languages": country.get("languages", None),
                "Currencies": country.get("currencies", None),
                "Timezones": country.get("timezones", None),
            }
            self.countries_data.append(country_info)

    def create_dataframe(self):
        """
        Creates a pandas DataFrame from the processed country data.

        Returns:
            DataFrame: A pandas DataFrame containing the country data.
        """
        return pd.DataFrame(self.countries_data)
