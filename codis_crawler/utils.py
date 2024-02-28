from typing import Callable, Tuple
from selenium.webdriver.common.by import By

def create_connection(driver: Callable) -> Callable:
    driver.get("https://codis.cwb.gov.tw/StationData")
    return driver

def get_element(
    driver_obj: Callable, 
    match_ref: str, 
    target: str, 
    multiple: bool=False
) -> Tuple[Callable, Callable]:
    
    match match_ref:
        case 'XPATH':
            ref = By.XPATH
        case 'CLASS_NAME':
            ref = By.CLASS_NAME
        case _:
            raise ValueError('Invaild match reference!')
    
    if multiple:
        target_driver_object = driver_obj.find_elements(
            ref,
            target
        )
    else:
        target_driver_object = driver_obj.find_element(
            ref,
            target
        )
    
    return driver_obj, target_driver_object

