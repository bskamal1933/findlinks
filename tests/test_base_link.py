import requests

import pages


def check_link_status_api(base_link: str):
    response = requests.get(base_link)
    print(response.status_code)
    assert response.status_code == 200, "BASE LINK : FAILED to access"


class BaseLink:
    def __init__(self, base_link):
        self.base_link = pages.base_page_link

    def base_link_check(self):
        check_link_status_api(self.base_link)
        return f"BASE LINK ACCESSIBLE : {self.base_link}"
