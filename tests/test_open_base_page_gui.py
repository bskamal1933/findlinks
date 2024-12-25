import time

from utils.driver import driver
from utils.common import read_path_json


class TestOpenBasePage:
    def test_login_base_gui(self, driver):
        json_data = read_path_json()
        url = json_data['base_page_link']
        print("Base Page :", url)
        driver.maximize_window()
        driver.get(url=url)
        driver.quit()
