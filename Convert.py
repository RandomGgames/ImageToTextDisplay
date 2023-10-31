import logging
import os
import sys
import yaml
from PIL import Image

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
        logging.fatal(f'The script could not read the config file due to a {repr(e)}.')
        exit(1)
    
    try:
        image = loadImage(Config['file'])
    except Exception as e:
        logging.fatal(f'Could not load the configured image file due to {repr(e)}.')
        exit(1)
    
    try:
        #Convert image into hex array
        image = image.convert("RGBA")
        width, height = image.size
        hex_array = [[None] * width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                r, g, b, a = pixel[:4]
                if a == 0:
                    hex_array[y][x] = None
                else:
                    hex_value = "#{:02X}{:02X}{:02X}".format(r, g, b)
                    hex_array[y][x] = hex_value
        
        #Test the hex array
        for y in range(height):
            row_hex_values = hex_array[y]
            row_hex_string = ' '.join(str(hex_value) if hex_value is not None else 'None' for hex_value in row_hex_values)
            print(row_hex_string)
    
    except Exception as e:
        logging.error(f'Something went wrong while converting the image into an array due to {repr(e)}.')
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
