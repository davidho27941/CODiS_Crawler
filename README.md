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

Due to the network latency and other issues, sometime the element will not appears as expected. If there is an error occur, try to execute the script again.

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

## Remote Executor via docker 

We provide an alternative way for selenium-based approch: execute via remote chrome executor. To use this method, you must install docker and run a `selenium/standalone-chrome` container as a remote executor.

### Prepare executor

To get your file, you must mount a folder into the container. Create a folder and change its permission before start a container:

```
mkdir /home/ubuntu/files
chown 1200:1201 /home/ubuntu/files
```

Then start a container using the following command:

```
docker run -d -p 4444:4444 --shm-size="2g" -v /home/ubuntu/files:/home/seluser/Downloads selenium/standalone-chrome:4.18.1-20240224
```


Please make sure you change the permission, otherwise the file cannot be writed into the correct place.

### Download via remote executor

Run the script with the following command for remote executor:

```
python -m codis_crawler selenium-crawler --station 467490 --mode remote --url http://127.0.0.1/wd/hub
```

> For more information, please visit the selenium [repository](https://github.com/SeleniumHQ/docker-selenium).