import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.common.by import By

from utils.common import load_driver, read_path_json, write_to_json, display_progress, skip_strings, max_threads


@load_driver(headless=True)
def link_extractor(driver, link: str, ele_to_check):

    json_data = read_path_json(required_file='pages.json')
    ele_page_elements = json_data['page_elements']

    driver.get(link)

    all_links = []
    for element in ele_page_elements:
        if "href" in element:
            href_elements = driver.find_elements(By.XPATH, element)
            for link in href_elements:
                href = link.get_attribute("href")  # Get the href attribute
                if href not in all_links:
                    all_links.append(str(href))
        if "button" in element:
            btn_elements = driver.find_elements(By.XPATH, element)
            for btn in btn_elements:
                pass
            #todo this needs to be implemented
    return all_links


@load_driver()
def test_load_base_page_links(driver):

    json_data = read_path_json(required_file="pages.json")
    all_url = json_data['base_page_link']
    for url in all_url:
        print("Base Page :", url)
        driver.get(url=url)

        ele_page_elements = json_data['page_elements']['ele_links']
        all_elements = driver.find_elements(By.XPATH, ele_page_elements)
        all_links = []
        for n in range(len(all_elements)):
            href = all_elements[n].get_attribute("href")  # Get the href attribute
            if href not in all_links:
                all_links.append(str(href))
            display_progress(n, len(all_elements)-1)

        link_json = read_path_json(required_file="all_links.json")
        data = link_json['found_links']
        ignore_link_json = read_path_json(required_file="ignore_links.json")
        ignore_links = ignore_link_json['ignore_links']
        for item in all_links:
            if (item not in data and item not in ignore_links and 'jobs' not in item
                    and not any(skip in item for skip in skip_strings)):
                data.append(item)
        link_json['found_links'] = data
        update_json = write_to_json(new_data=link_json, required_file="all_links.json")
        assert update_json, "JSON updating failed with links"


def process_link(url, old_data, ignore_links):
    """
    Process a single link to extract sub-links and update the shared data.
    """
    print("link=>>> ", url)
    new_page_links = link_extractor(link=url)

    link_json = read_path_json(required_file="all_links.json")
    # old_data = link_json['found_links']

    for link in new_page_links:
        if (link not in old_data and link not in ignore_links
            and not any(skip in link for skip in skip_strings)):
            old_data.append(link)
    link_json['found_links'] = old_data
    write_to_json(new_data=link_json, required_file="all_links.json")


def test_get_all_sub_links():
    test_load_base_page_links()

    ignore_link_json = read_path_json(required_file="ignore_links.json")
    ignore_links = ignore_link_json['ignore_links']

    while True:
        link_json = read_path_json(required_file="all_links.json")
        old_data = link_json['found_links']
        for data in old_data:
            process_link(data, old_data, ignore_links)
        link_json = read_path_json(required_file="all_links.json")
        new_data = link_json['found_links']
        if old_data == new_data:
            break
    print(f"updated all_links.json page :)")



    # lock = threading.Lock()  # Lock to prevent race conditions

    # Use ThreadPoolExecutor to manage threads
    # with ThreadPoolExecutor(max_threads) as executor:
    #     try:
    #         # Submit tasks to the executor
    #         for item in range(len(old_data)):
    #             executor.submit(process_link, item, old_data, ignore_links, lock)
    #         count = 1
    #         while True:
    #             new_link_json = read_path_json(required_file="all_links.json")
    #             new_data = new_link_json['found_links']
    #             old_new_data = new_data
    #             # Submit tasks to the executor
    #             for item in range(len(old_new_data)):
    #                 executor.submit(process_link, item, old_data, ignore_links, lock)
    #             link_json = read_path_json(required_file="all_links.json")
    #             old_data = link_json['found_links']
    #             if old_data == new_data:
    #                 break
    #     except KeyboardInterrupt:
    #         print("Keyboard interrupt received. Closing all threads.")
    #         exit(0)

