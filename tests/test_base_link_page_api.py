import pytest

from utils.api.base_api import check_link_status_api
from utils import common


class TestBaseLink:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Initialize `base_link` before each test
        json_data = common.read_path_json(required_file="pages.json")
        self.base_link = json_data['base_page_link']
        print(f"Base Link Initialized: {self.base_link}")

    def test_base_link_check(self):
        # Use an assertion to validate the link status
        check_link_status_api(self.base_link)

# class TestAllLinks:

