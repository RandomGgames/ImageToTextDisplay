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
        logging.debug(f'Error occured while reading image file.')
        raise e

def readYAML(path: str) -> dict:
    logging.debug(f'Reading the YAML file at "{path}".')
    try:
        with open(path, 'r') as f:
            data = yaml.load(f, yaml.SafeLoader)
            logging.debug(f'Done reading the YAML file.')
            return data
    except Exception as e:
        logging.debug(f'Error occured while reading YAML file.')
        raise e

def generateImageHexArray(image):
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
        logging.debug(f'Error occured while generating image hex array.')
        return e

def generateCommand(color_hex: hex = '#000000', coordinates: str = '~ ~ ~', scale_transform: list = ["1.0f", "1.0f", "1.0f"], translation_transform: list = ["0.0f", "0.0f", "0.0f"]):
    logging.debug(f'Generating command...')
    try:
        left_rotation_transform: list = ["0.0", "0.0", "0.0", "1.0"]
        left_rotation_transform = f'{",".join(left_rotation_transform)}'
        
        right_rotation_transform: list = ["0.0f", "0.0f", "0.0f", "1.0f"]
        right_rotation_transform = f'{",".join(right_rotation_transform)}'
        
        translation_transform = f'{",".join(translation_transform)}'
        
        scale_transform = f'{",".join(scale_transform)}'
        
        nbt = f'{{billboard:"fixed",text:\'{{"text":"■","color":"{color_hex}"}}\',background:0,transformation:{{left_rotation:[{left_rotation_transform}],right_rotation:[{right_rotation_transform}],translation:[{translation_transform}],scale:[{scale_transform}]}}}}'
        
        command = f'summon minecraft:text_display {coordinates} {nbt}'
        logging.debug(f'Generated command.')
        return command
        
    except Exception as e:
        raise e

def generateCommands(width: int, height: int, hex_array: list, scale: float, coordinates: str = '~ ~ ~') -> list:
    logging.debug(f'Generating commands...')
    try:
        commands = []
        for y in range(height):
            for x in range(width):
                color = hex_array[y][x]
                if color != None:
                    translation_transform = [
                        f"{round( (0.125 * scale * x) - (0.125 * scale * width)/2 + (0.125 * scale)/2.5,             6)}f",
                        f"{round( (0.125 * scale * (height - y)) - (0.125 * scale * 1.875) + (0.125 * scale * 0.08), 6)}f",
                        "0.0f"]
                    scale_transform = [
                        f"{scale}f",
                        f"{scale}f",
                        f"{scale}f"]
                    command = generateCommand(color_hex = color, scale_transform = scale_transform, translation_transform = translation_transform, coordinates = coordinates)
                    commands.append(command)
        return commands
    except Exception as e:
        raise e

def main():
    logging.debug(f'Running {__name__}')
    
    try:
        config = readYAML('config.yaml')
        image_location = config['image_file']
        output_file = config['output_file']
        scale = config['scale']
        coordinates = config['coordinates']
        logging.debug(f'{config = }')
    except Exception as e:
        logging.fatal(
            f'The script could not read the config file due to a {repr(e)}.')
        exit(1)
    
    try:
        image = loadImage(image_location)
        width, height = image.size
    except Exception as e:
        logging.fatal(
            f'Could not load the configured image file due to {repr(e)}.')
        exit(1)
    
    try:
        # Convert image into hex array
        hex_array = generateImageHexArray(image)
    except Exception as e:
        logging.fatal(
            f'Something went wrong while converting the image into an array due to {repr(e)}.')
        exit(1)
    
    try:
        commands = generateCommands(
            width=width, height=height, hex_array=hex_array, scale=scale, coordinates=coordinates)
    except Exception as e:
        logging.fatal(
            f'An error occured while generating summon commands due to {repr(e)}')
        exit(1)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for string in commands:
            f.write(string + '\n')
    
    logging.info('Done.')

if __name__ == '__main__':
    # Clear latest.log if it exists
    if os.path.exists('latest.log'):
        open('latest.log', 'w').close()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        encoding='utf-8',
        handlers=[
            logging.FileHandler('latest.log', encoding='utf-8'),
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
