import time

import pytest
import selenium
from selenium import webdriver


# Fixture to initialize WebDriver
@pytest.fixture
def driver():
    # Set up WebDriver (e.g., using Chrome)
    # Initialize the WebDriver (Chrome in this case)
    sel_driver = webdriver.Chrome()

    return sel_driver
