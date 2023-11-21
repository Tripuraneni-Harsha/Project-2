# box_office_data_fetcher.py

import requests
from bs4 import BeautifulSoup
import pandas as pd


class BoxOfficeDataFetcher:
    """
    A class to fetch and process box office data from Box Office Mojo for a range of years.

    Attributes:
        start_year (int): The starting year for the data fetching process.
        end_year (int): The ending year for the data fetching process.
    """

    def __init__(self, start_year, end_year):
        """
        Initializes the BoxOfficeDataFetcher with the specified range of years.

        Parameters:
            start_year (int): The first year in the range of years to fetch data for.
            end_year (int): The last year in the range of years to fetch data for.
        """
        self.start_year = start_year
        self.end_year = end_year

    def fetch_webpage(self, url):
        """
        Fetches the content of the webpage at the given URL.

        Parameters:
            url (str): The URL of the webpage to fetch.

        Returns:
            bytes: The content of the webpage.

        Raises:
            Exception: If the request to fetch the webpage fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Failed to retrieve the webpage: {e}")
            return None

    def extract_table_data(self, html_content):
        """
        Parses the HTML content of a webpage to extract table data.

        Parameters:
            html_content (bytes): The HTML content of the webpage.

        Returns:
            DataFrame: A DataFrame containing the parsed table data.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        div_element = soup.find("div", class_="a-section imdb-scroll-table-inner")

        if not div_element:
            print("Div element not found.")
            return None

        rows = div_element.find_all("tr")
        if not rows:
            print("No table rows found.")
            return None

        headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
        data_rows = []

        for row in rows[1:]:
            data = [td.get_text(strip=True) for td in row.find_all("td")]
            data_rows.append(data)

        return pd.DataFrame(data_rows, columns=headers)

    def fetch_all_years_data(self):
        """
        Fetches box office data for all years in the specified range and combines it into a single DataFrame.

        Returns:
            DataFrame: A DataFrame containing the combined box office data for all years.
        """
        all_data = pd.DataFrame()

        for year in range(self.start_year, self.end_year + 1):
            url = f"https://www.boxofficemojo.com/year/world/{year}/"
            print(f"Fetching data for year: {year}")

            html_content = self.fetch_webpage(url)
            if html_content:
                df = self.extract_table_data(html_content)
                if df is not None:
                    df["Year"] = year
                    all_data = pd.concat([all_data, df], ignore_index=True)

        return all_data


# Example usage:
# fetcher = BoxOfficeDataFetcher(start_year=1977, end_year=2023)
# all_data = fetcher.fetch_all_years_data()
# all_data.head()
