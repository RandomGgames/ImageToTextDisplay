import logging
import os
import sys
import yaml
from PIL import Image

from typing import TypedDict
Config = TypedDict("Config", {
    "file": str,
    "scale": float
})

def loadImage(path: str) -> Image:
    logging.debug(f'Reading the image file at "{path}".')
    try:
        image = Image.open(path)
        logging.debug(f'Done reading the image file.')
        return image
    except Exception as e:
        logging.debug(f'There was an error reading the image file due to {repr(e)}.')
        raise e

def readYAML(path: str) -> dict:
    logging.debug(f'Reading the YAML file at "{path}".')
    try:
        with open(path, 'r') as f:
            data = yaml.load(f, yaml.SafeLoader)
            logging.debug(f'Done reading the YAML file.')
            return data
    except Exception as e:
        logging.debug(f'There was an error reading the YAML file due to {repr(e)}.')
        raise e

def main():
    logging.debug(f'Running main body of script')
    
    try:
        Config = readYAML('config.yaml')
        logging.debug(f'{Config = }')
    except Exception as e:
        logging.fatal(f'The script could not read the config file due to a {repr(e)}')
        exit(1)
    
    try:
        image = loadImage(Config['file'])
    except Exception as e:
        logging.fatal(f'Could not load the configured image file due to {repr(e)}')
        exit(1)
    
    logging.info('Done.')

if __name__ == '__main__':
    # Clear latest.log if it exists
    if os.path.exists('latest.log'):
        open('latest.log', 'w').close()
    
    # Set up logging
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt = '%Y/%m/%d %H:%M:%S',
        encoding = 'utf-8',
        handlers = [
            logging.FileHandler('latest.log', encoding = 'utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.debug(f'Running "{os.path.basename(__file__)}"')
    logging.getLogger('PIL').setLevel(logging.WARNING)
    
    # Call main function
    try:
        main()
    except Exception as e:
        logging.error(e)
        input(f'The script could no longer continue to function due to the error described above. Please fix the issue described or go to https://github.com/RandomGgames/RMMUD to request help/report a bug')
        exit(1)
