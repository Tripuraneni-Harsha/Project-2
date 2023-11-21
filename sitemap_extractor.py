import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


class NFLSitemapExtractor:
    """
    A class dedicated to extracting and organizing sitemap URLs from the NFL website.

    Attributes:
        site_url (str): The base URL of the NFL website to be scraped.
        sitemaps (dict): A dictionary to store the URLs from each sitemap along with their dataframes.

    Methods:
        fetch_content(url): Fetches content from a given URL.
        parse_sitemap(sitemap_url): Parses a given sitemap URL and extracts all contained URLs.
        gather_sitemaps(): Gathers and processes all sitemaps from the website's robots.txt.
        refine_urls(): Refines each URL in the sitemaps, extracting subdirectories.
        save_csv(directory): Saves all sitemap dataframes to CSV files in the specified directory.
    """

    def __init__(self, site_url):
        """
        Initializes the NFLSitemapExtractor with a given website URL.

        Parameters:
            site_url (str): The base URL of the NFL website to be scraped.
        """
        self.site_url = site_url
        self.sitemaps = {}
        self.gather_sitemaps()

    def fetch_content(self, url):
        """
        Fetches content from a given URL using HTTP GET request with custom headers.

        Parameters:
            url (str): The URL to fetch the content from.

        Returns:
            str: The content of the webpage, or an empty string if an error occurs.
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return ""

    def parse_sitemap(self, sitemap_url):
        """
        Parses a sitemap URL, extracts all URLs contained within it, and stores them.
        Recursively processes nested sitemaps.

        Parameters:
            sitemap_url (str): The URL of the sitemap to be parsed.
        """
        xml_content = self.fetch_content(sitemap_url)
        soup = BeautifulSoup(xml_content, "xml")
        urls = []

        for loc in soup.find_all("loc"):
            url = loc.get_text()
            urls.append(url)
            if url.endswith(".xml"):
                self.parse_sitemap(url)

        self.sitemaps[sitemap_url] = pd.DataFrame(urls, columns=["URLs"])

    def gather_sitemaps(self):
        """
        Gathers and processes all sitemaps listed in the website's robots.txt file.
        """
        robots_txt = self.fetch_content(f"{self.site_url}/robots.txt")
        for line in robots_txt.splitlines():
            if line.startswith("Sitemap:"):
                self.parse_sitemap(line.split(": ")[1].strip())

    def refine_urls(self):
        """
        Refines URLs in the sitemaps, extracting and storing subdirectories from each URL.
        """
        for key, df in self.sitemaps.items():
            df["Subdirectories"] = df["URLs"].apply(
                lambda x: x.replace(self.site_url, "").split("/")
            )

    def save_csv(self, directory="sitemap_data"):
        """
        Saves all sitemap dataframes to CSV files in the specified directory.
        Creates the directory if it does not exist.

        Parameters:
            directory (str): The directory where the CSV files will be saved.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

        for name, df in self.sitemaps.items():
            filename = f"{directory}/{name.split('/')[-1]}.csv"
            df.to_csv(filename, index=False)
