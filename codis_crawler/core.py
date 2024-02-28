from typing import Callable

def create_connection(driver: Callable):
    driver.get("https://codis.cwb.gov.tw/StationData")
    return driver

def 