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
        raise e

def readYAML(path: str) -> dict:
    logging.debug(f'Reading the YAML file at "{path}".')
    try:
        with open(path, 'r') as f:
            data = yaml.load(f, yaml.SafeLoader)
            logging.debug(f'Done reading the YAML file.')
            return data
    except Exception as e:
        raise e

def generateImageHexArray(image: Image) -> list:
    logging.debug(f'Converting image to hex array...')
    try:
        image = image.convert("RGBA")
        width, height = image.size
        logging.debug(f'Image size: {width}x{height}')
        hex_array = [[None] * width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                r, g, b, a = pixel[:4]
                if a == 0:
                    hex_array[y][x] = None
                else:
                    hex_value = '#{:02X}{:02X}{:02X}'.format(r, g, b)
                    hex_array[y][x] = hex_value
        logging.debug(f'Done converting image to hex array.')
        return hex_array
    except Exception as e:
        raise e

def generateCommand(color_hex: hex = '#000000', coordinates: str = '~ ~ ~', scale: list = ["1.0f", "1.0f", "1.0f"], translation: list = ["0.0f", "0.0f", "0.0f"], left_rotation: list = ["0.0", "0.0", "0.0", "1.0"], right_rotation: list = ["0.0f", "0.0f", "0.0f", "1.0f"]) -> str:
    logging.debug(f'Generating command...')
    try:
        left_rotation = f'{",".join(left_rotation)}'
        right_rotation = f'{",".join(right_rotation)}'
        translation = f'{",".join(translation)}'
        scale = f'{",".join(scale)}'
        nbt = f'{{billboard:"fixed",text:\'{{"text":"■","color":"{color_hex}"}}\',background:0,transformation:{{left_rotation:[{left_rotation}],right_rotation:[{right_rotation}],translation:[{translation}],scale:[{scale}]}}}}'
        command = f'summon minecraft:text_display {coordinates} {nbt}'
        logging.debug(f'Generated command.')
        return command
    except Exception as e:
        raise e

def generateCommands(width: int, height: int, hex_array: list, scale: float) -> list:
    logging.debug(f'Generating commands...')
    try:
        commands = []
        for y in range(height):
            for x in range(width):
                logging.debug(f'Generating command for ({x}, {height - y})')
                if hex_array[y][x] != None:
                    translation = [
                        f"{0.125 * x * scale}f",
                        f"{0.125 * (height - y) * scale}f",
                        "0.0f"
                    ]
                    scale = [
                        f"{scale}f",
                        f"{scale}f",
                        f"{scale}f"
                    ]
                    logging.debug(f'{x = }')
                    logging.debug(f'{y = }')
                    logging.debug(f'{hex_array[y][x] = }')
                    logging.debug(f'{scale = }')
                    logging.debug(f'{translation = }')
                    command = generateCommand(color_hex=hex_array[y][x], scale=scale, translation=translation)
                    commands.append(command)
        logging.debug(f'Done generating commands.')
        return commands
    except Exception as e:
        raise e

def main():
    logging.debug(f'Running {__name__}')
    
    try:
        config = readYAML('config.yaml')
        logging.debug(f'{config = }')
    except Exception as e:
        logging.fatal(f'The script could not read the config file due to a {repr(e)}.')
        exit(1)
    
    try:
        image = loadImage(config['file'])
        width, height = image.size
    except Exception as e:
        logging.fatal(f'Could not load the configured image file due to {repr(e)}.')
        exit(1)
    
    try:
        #Convert image into hex array
        hex_array = generateImageHexArray(image)
    except Exception as e:
        logging.fatal(f'Something went wrong while converting the image into an array due to {repr(e)}.')
        exit(1)
    
    
    ##Test the hex array
    #for y in range(height):
    #    row_hex_values = hex_array[y]
    #    row_hex_string = ' '.join(str(hex_value) if hex_value is not None else 'None' for hex_value in row_hex_values)
    #    print(row_hex_string)
    

    try:
        generateCommand()
    except Exception as e:
        logging.error(f'Could not generate command due to {repr(e)}')
        exit(1)
    
    #try:
    #    logging.debug(f'{width = }')
    #    logging.debug(f'{height = }')
    #    logging.debug(f'{config["scale"] = }')
    #    commands = generateCommands(width, height, hex_array, config['scale'])
    #except Exception as e:
    #    logging.fatal(f'An error occured while generating the list of commands due to {repr(e)}')
    
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
