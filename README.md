# CODiS Crawler 

## Introduction 

This is a `selenium`` based web crawler. This crawler aim to download the weather data from CODiS platform.

> A `httpx` based solution will also be provided in future version.

## Quick Start

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

### Download a record of specific station

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
