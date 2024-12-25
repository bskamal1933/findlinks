import requests


def check_link_status_api(url: str):
    response = requests.get(url)
    print(response.status_code)
    assert response.status_code == 200, f"BASE LINK FAILED to access: {url}"