from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib3.exceptions import NewConnectionError
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from typing import Callable, Tuple, Any, Dict, Union


def install_web_driver():
    try:
        webdriver_path = ChromeDriverManager().install()
    except Exception as e:
        raise e


def create_webdriver(mode: str, headless=False, remote_url=None) -> Callable:

    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    try:
        match mode:
            case "local":
                driver = webdriver.Chrome(options=chrome_options)
            case "remote":
                driver = webdriver.Remote(
                    command_executor=remote_url, options=chrome_options
                )
            case _:
                raise ValueError("Invalid web driver running mode!")
    except NewConnectionError:
        raise NewConnectionError
    except WebDriverException:
        raise WebDriverException(
            "Web Driver not found! Please install driver before trying to run."
        )

    return driver


def create_connection(driver: Callable) -> Callable:
    driver.get("https://codis.cwa.gov.tw/StationData")
    return driver


def get_element(
    driver_obj: Callable, match_ref: str, target: str, multiple: bool = False
) -> Tuple[Callable, Callable]:

    match match_ref:
        case "XPATH":
            ref = By.XPATH
        case "CLASS_NAME":
            ref = By.CLASS_NAME
        case _:
            raise ValueError("Invaild match reference!")

    if multiple:
        target_driver_object = driver_obj.find_elements(ref, target)
    else:
        target_driver_object = driver_obj.find_element(ref, target)

    return target_driver_object

def parse_sub_dict(hourly_data: Dict[str, Union[float, Any]]) -> Dict: 
    
    del hourly_data['DataTime']
    
    parsed_dict = {}
    
    for obs_name, obs_value in hourly_data.items():
        if len(obs_value.keys()) > 1:
            for obs_sub_key, obs_sub_value in obs_value.items():
                parsed_dict[f"{obs_name}_{obs_sub_key}"] = obs_sub_value
        else:
            parsed_dict[obs_name] = list(obs_value.values())[0]
            
    return parsed_dict