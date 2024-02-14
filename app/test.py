from selenium import webdriver
import pandas as pd

import re

from utils.data import month_names_dict
from utils.functions import click_element_by_text, find_links_to_excel_files, download_excel_files_from_url
from services.sns_service import get_about

# Reading Source files
url_sources = pd.read_csv('data/sources_list.csv')
df = pd.read_csv('data/input.csv')
df = pd.merge(df, url_sources, on='nombre_corto', how='left')

CONF_HEADLESS_BROWSER = True

print(pd)

def download_sns():
    # Open in browser
    driver = webdriver.Firefox(options=options)
    driver.get(base_url)
    # Click the year
    click_element_by_text(driver, next_needed_year)

    # Click the month
    click_element_by_text(driver, next_needed_month_text)

    # Find the link to the Excel file
    content = driver.page_source
    excel_links = find_links_to_excel_files(content)

    # Download the Excel file
    download_excel_files_from_url(excel_links, folder_name)
    driver.close()
    return excel_links

print(get_about('https://sns.gob.do/sobre-nosotros/quienes-somos/'))

# main function
if __name__ == "__main__":
    for i in range(len(df)):
        print(df['nombre_corto'][i])
        # common variables
        base_url = df['portal'][i].strip()
        domain = re.findall(r'^(https?://[^/]+)', base_url)[0]
        next_needed_date = df['query_date'][i]
        next_needed_year, next_needed_month = next_needed_date.split('_')
        next_needed_month_text = month_names_dict[next_needed_month]
        folder_name = f"downloads/{next_needed_date}/{df['nombre_corto'][i]}"
        options = webdriver.FirefoxOptions()
        if CONF_HEADLESS_BROWSER:
            options.add_argument('--headless')
        # calling the download function
        eval(f"download_{df['nombre_corto'][i].lower()}")()