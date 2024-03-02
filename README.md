# CODiS Crawler 

**CODiS Crawler** is an open source web crawler. This package can help you to download the data from [CODiS](https://codis.cwb.gov.tw/StationData) platform. You may download the data via `selenium`-based or `httpx`-based approach. 

## Installation

### Install Dependencies

```
pip install -r requirements.txt
```

### Install package

* Editable mode

```
pip install -e .
```

* Install to system

```
pip install build
python -m build 
python -m pip install dist/codis_crawler-0.1.0-py3-none-any.whl
```

### Install Web Drive 

Currently, we provide a command to install the chrome web driver.

```
python -m codis_crawler install-driver
```

## Usage

### Download vis selenium-based approach

When using this approach, the script will interact with CODiS via web driver and selenium. The script will input the informations, open the popup dashboard, then click the download button. A `csv` file will be downlaoded if the script executed without error.

* current date

```
python -m codis_crawler selenium-crawler --station 467490
```

* Given a specific date

```
python -m codis_crawler selenium-crawler --station 467490 --date 2023-10-01
```

### Run in headless mode

```
python -m codis_crawler selenium-crawler --station 467490 --headless
```

### Download vis httpx-based approach

When using httpx-based approach, target date must be provided.

```
 python -m codis_crawler httpx-crawler  --station 467490 --date <target date>
```

The script will download a json from the CODiS API.

Caution: The JSON data contains the raw information response by the API. The raw data is much different compare to the data shown in dashboard.