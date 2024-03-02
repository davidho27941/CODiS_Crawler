import time
import json
import httpx
import calendar
import pandas as pd
from typing import Any
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common import NoSuchElementException

from .utils import (
    create_webdriver,
    create_connection,
    get_element,
)


class seleniumCrawler:
    def __init__(
        self,
        *,
        mode: str = "local",
        headless=False,
        targte_date: str = None,
        target_area: str = None,
        target_city: str = None,
        target_station: str = None,
        remote_url: str = None,
    ) -> None:
        self.targte_date = targte_date

        if targte_date is not None:
            self.target_year = targte_date.split("-")[0]
            self.target_month = calendar.month_name[int(targte_date.split("-")[1])]
            self.target_day = int(targte_date.split("-")[2])

        self.target_area = target_area if target_city is not None else ""
        self.target_city = target_city
        self.target_station = target_station

        driver = create_webdriver(mode, headless=headless, remote_url=remote_url)

        self.driver = create_connection(driver)
        self.wait = WebDriverWait(self.driver, timeout=5)

    def setup_area(self):
        area_row = get_element(
            self.driver,
            "XPATH",
            "//div[@class='row' and .//*[contains(text(), '區域')]]",
        )
        area_selector = get_element(
            area_row,
            "CLASS_NAME",
            "form-control",
        )

        select_obj = Select(area_selector)
        select_obj.select_by_value(self.target_area)
        area_selector.click()

    def setup_city(self):
        city_parent_element = get_element(
            self.driver,
            "XPATH",
            "//div[@class='row' and .//*[contains(text(), '縣市')]]",
        )

        city_selector = get_element(
            city_parent_element,
            "XPATH",
            ".//select[@class='form-control' and @id='station_area']",
        )

        select = Select(city_selector)
        select.select_by_value(self.target_city)
        city_selector.click()

    def setup_station(self):
        station_parent_element = get_element(self.driver, "CLASS_NAME", "input-group")

        station_input_element = get_element(
            station_parent_element,
            "CLASS_NAME",
            "form-control",
        )

        station_input_element.send_keys(self.target_station)

    def click_map_icon(self):
        map_icon = get_element(
            self.driver, "XPATH", "//div[contains(@class, 'leaflet-interactive')]"
        )
        map_icon.click()

    def click_open_dashboard(self):
        open_button = get_element(
            self.driver,
            "XPATH",
            f"//button[contains(@class, 'show_stn_tool') and contains(@data-stn_id, '{self.target_station}')]",
        )
        dashboard = get_element(
            self.driver, "XPATH", "//section[@class='lightbox-tool']"
        )

        open_button.click()

        # if dashboard.get_attribute("style") == "display: none;":
        #     open_button.click()

    def get_download_panel(self):
        download_parent = get_element(
            self.driver,
            "XPATH",
            "//div[contains(@class, 'lightbox-tool-type-container') and not(contains(@style, 'display: none;'))]",
        )
        return download_parent

    def setup_datetime(self, download_panel):
        datetime_panel = get_element(download_panel, "CLASS_NAME", "vdatetime")

        self.driver.implicitly_wait(2)

        actions = ActionChains(self.driver)
        actions.move_to_element(datetime_panel).click().perform()

        self.driver.implicitly_wait(2)

        year_selector = get_element(
            download_panel, "XPATH", "//div[contains(@class, 'vdatetime-popup__year')]"
        )

        year_selector.click()

        year_picker = get_element(
            download_panel,
            "XPATH",
            f"//div[contains(@class, 'vdatetime-year-picker__item') and contains(text(), '{self.target_year}')]",
        )

        year_picker.click()

        month_selector = get_element(
            download_panel, "XPATH", "//div[contains(@class, 'vdatetime-popup__date')]"
        )

        month_selector.click()

        month_picker = get_element(
            download_panel,
            "XPATH",
            f"//div[contains(@class, 'vdatetime-month-picker__item') and contains(text(), '{self.target_month}')]",
        )

        month_picker.click()

        day_picker = get_element(
            download_panel,
            "XPATH",
            f"//div[contains(@class, 'vdatetime-calendar__month__day') and .//*[contains(text(), '{self.target_day}')]]",
        )

        day_picker.click()

    def download(self, download_panel):
        download_btn = get_element(
            download_panel,
            "XPATH",
            "//div[@class='lightbox-tool-type-ctrl-btn' and .//img]",
        )
        download_btn.click()

    def setup_websit(self):
        self.setup_area()
        if self.target_city is not None:
            self.setup_city()
        self.setup_station()

    def open_dashboard(self):
        self.click_map_icon()
        self.click_open_dashboard()

    def choose_and_download(self):

        # Try to get download panel from dashboard, if dashboard not exits
        # execute the `self.click_open_dashboard()` again.
        try:
            download_panel = self.get_download_panel()
        except NoSuchElementException:
            self.click_open_dashboard()

        if self.targte_date is not None:
            self.setup_datetime(download_panel)

        self.download(download_panel)

    def get_weather_data(self):
        try:
            self.setup_websit()
            print("Stage 1 done.")
            time.sleep(2)
            self.open_dashboard()
            print("Stage 2 done.")
            self.choose_and_download()
            time.sleep(3)
            print("Stage 3 done.")
            self.driver.quit()
        except Exception as e:
            raise (e)


class httpxCrawler:
    def __init__(self, *, target_station: str, target_date: str) -> None:
        self.url = "https://codis.cwb.gov.tw/api/station"

        stn_prefix = target_station[:2]

        self.target_station = target_station
        self.target_date = target_date

        date = f"{target_date}T00:00:00.000+08:00"
        start = f"{target_date}T00:00:00"
        end = f"{target_date}T23:59:59"

        match stn_prefix:
            case "46":
                stn_type = "cwb"
            case "C1":
                stn_type = "auto_C1"
            case "C0":
                stn_type = "auto_C0"
            case _:
                stn_type = "agr"

        self.data = {
            "type": "report_date",
            "more": "",
            "item": "",
            "stn_type": stn_type,
            "date": date,
            "start": start,
            "end": end,
            "stn_ID": self.target_station,
        }

    def get_weather_data(self):
        with httpx.Client() as client:
            client.get(self.url)

            response: httpx.Response = client.post(self.url, data=self.data)

            with open(
                f"{self.target_station}_{self.target_date}.json", "w", encoding="utf-8"
            ) as file:
                json.dump(response.json(), file, ensure_ascii=True, indent=4)
