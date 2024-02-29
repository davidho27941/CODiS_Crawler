import time
import httpx
import calendar
from typing import Any
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

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
        open_button.click()

        dashboard = get_element(
            self.driver, "XPATH", "//section[@class='lightbox-tool']"
        )

        # Click button again if dashboard not displayed.
        # TODO: change to explicit waits
        if dashboard.get_attribute("style") == "display: none;":
            open_button.click()

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
        self.driver.implicitly_wait(5)
        if self.target_city is not None:
            self.setup_city()
            self.driver.implicitly_wait(5)
        self.setup_station()
        self.driver.implicitly_wait(5)

    def open_dashboard(self):
        self.click_map_icon()
        self.driver.implicitly_wait(2)
        self.click_open_dashboard()
        self.driver.implicitly_wait(2)

    def choose_and_download(self):

        download_panel = self.get_download_panel()
        self.driver.implicitly_wait(2)

        if self.targte_date is not None:
            self.setup_datetime(download_panel)

        self.driver.implicitly_wait(2)
        self.download(download_panel)

    def get_weather_data(self):
        try:
            self.setup_websit()
            print("Stage 1 done.")
            self.driver.implicitly_wait(2)
            self.open_dashboard()
            print("Stage 2 done.")
            self.driver.implicitly_wait(2)
            self.choose_and_download()
            time.sleep(3)
            print("Stage 3 done.")
            self.driver.quit()
        except Exception as e:
            raise (e)
