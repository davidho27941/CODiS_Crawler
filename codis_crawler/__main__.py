import click

from .core import (
    seleniumCrawler,
    httpxCrawler,
)
from .utils import install_web_driver


@click.group()
def main(): ...


@main.command()
def install_driver():
    install_web_driver()


@main.command()
@click.option(
    "--mode",
    "mode",
    default="local",
    type=click.Choice(["remote", "local"]),
    help="Specify to run in remote or local environment.",
)
@click.option(
    "--url",
    "url",
    default=None,
    type=str,
    help="Specify the url of remote chrome executor.",
)
@click.option(
    "--headless",
    is_flag=True,
    default=False,
    help="Run in headless mode. Default: False.",
)
@click.option(
    "--area",
    "area",
    default=None,
    type=click.Choice(["北區", "中區", "南區", "東區", "外島"]),
    help="The city where weathre station located.",
)
@click.option(
    "--city",
    "city",
    type=str,
    default=None,
    help="The city where weathre station located.",
)
@click.option("--date", "date", type=str, default=None, help="The date to download.")
@click.option(
    "--station", "station", type=str, required=True, help="The id of station."
)
def selenium_crawler(
    mode: str,
    url: str,
    area: str,
    city: str,
    date: str,
    station: str,
    headless: bool,
):
    if mode == "remote" and url is None:
        raise ValueError("Select to run in remote mode but no URL provided!")

    crawler = seleniumCrawler(
        mode=mode,
        target_area=area,
        targte_date=date,
        target_station=station,
        headless=headless,
        target_city=city,
        remote_url=url,
    )
    crawler.get_weather_data()


@main.command()
@click.option(
    "--station", "station", type=str, required=True, help="The id of station."
)
@click.option("--date", "date", type=str, default=None, help="The date to download.")
def httpx_crawler(station, date):
    crawler = httpxCrawler(target_station=station, target_date=date)

    crawler.get_weather_data()


if __name__ == "__main__":
    main()
