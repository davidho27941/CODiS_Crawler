import click

from .utils import install_web_driver

@click.group()
def main():
    ...
    

@click.command()
def install_driver():
    install_web_driver()
    
if __name__ == '__main__':
    main()