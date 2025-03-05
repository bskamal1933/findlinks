import json
import os.path

from selenium import webdriver
from selenium.webdriver.common.by import By

import configs
import pytest


# Progress bar function
def display_progress(current, total, bar_length=50):
    """
    Displays a progress bar with the percentage of completion.

    Args:
        current (int): The current iteration count.
        total (int): The total number of iterations.
        bar_length (int): The length of the progress bar in characters.
    """
    percentage = (current / total) * 100
    completed_length = int(bar_length * current // total)
    bar = "=" * completed_length + "-" * (bar_length - completed_length)
    print(f"\r[{bar}] {percentage:.2f}%", end="")

def load_driver(headless = False):
    """Decorator to manage WebDriver for a test function."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Configure WebDriver options
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                # options.add_argument("--no-sandbox")
                # options.add_argument("--disable-dev-shm-usage")

            # Initialize the WebDriver
            driver = webdriver.Chrome(options=options)
            try:
                # Pass the driver to the decorated function
                return func(driver, *args, **kwargs)
            finally:
                # Quit the driver after use
                driver.quit()
        return wrapper
    return decorator


def read_path_json(required_file:str, path = configs.get_proj_path()):
    try:
        with open(os.path.join(path,"pages",required_file), 'r') as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None


ignore_str = read_path_json(required_file="ignore_links.json")
skip_strings = ignore_str["default_ignore"]

def write_to_json(new_data:dict, required_file:str, path = configs.get_proj_path()):
    try:
        with open(os.path.join(path,"pages",required_file), 'w') as json_file:
            json.dump(new_data, json_file, indent=4)
            return True
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        return None

# @load_driver
# def load_base_page(driver):
#     json_data = read_path_json()
#     url = json_data['base_page_link']
#     print("Base Page :", url)
#     driver.maximize_window()
#     return driver.get(url=url)
#
# @load_driver
# def get_all_links_in_page(driver, ele_to_check:str):
#     json_data = read_path_json(required_file="pages.json")
#     ele_page_elements = json_data['page_elements'][ele_to_check]
#     all_elements = driver.find_elements(By.XPATH, ele_to_check)
#     print("find_elements =>>>",all_elements)
#     all_links = []
#     for link in all_elements:
#         href = link.get_attribute("href")  # Get the href attribute
#         print("////",href)
#         all_links.append(href)
#     return all_links


@pytest.fixture
def max_threads(request):
    return int(request.config.getoption("--max-threads"))