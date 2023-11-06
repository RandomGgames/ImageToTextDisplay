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
                    hex_value = "#{:02X}{:02X}{:02X}".format(r, g, b)
                    hex_array[y][x] = hex_value
        logging.debug(f'Done converting image to hex array.')
        return hex_array
    except Exception as e:
        logging.debug(f'Error occured while generating image hex array.')
        return e

def generateCommand(pixel_x: int, pixel_y: int, coordinates: str = '~ ~ ~', color: hex = 000000, left_rotation: list = ["0.0f", "0.0f", "0.0f", "1.0f"], right_rotation: list = ["0.0f", "0.0f", "0.0f", "1.0f"], translation: list = ["0.0f", "0.0f", "0.0f"], scale: list = ["1.0f", "1.0f", "1.0f"]):
    text = f'summon text_display {coordinates} {{billboard:"fixed",text:\'{{"text":"■","color":"#{color}"}}\',transformation:{{left_rotation:[{",".join(left_rotation)}],right_rotation:[{",".join(right_rotation)}],translation:[{",".join(translation)}],scale:[{",".join(scale)}]}}}}'
    return text
    
    pass
    #Example command I'm using to generate text:
    #/summon text_display 0 50.5 -8 {billboard:"vertical",text:'[{"text":"Your goal is to destroy whatever build is in front of you, but you can only use the TNT you are given!","color":"white"}]',transformation:{left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],translation:[0.0f,0.0f,0.0f],scale:[0.5f,0.5f,0.5f]}}
    
    #How the command should look roughly
    #/summon text_display ~ ~ ~ {billboard:"fixed",text:text:'[{"text":"■","color":"#2EFF9D"}]',transformation:{left_rotation:[0.0f,0.0f,0.0f,1.0f],right_rotation:[0.0f,0.0f,0.0f,1.0f],translation:[0.0f,0.0f,0.0f],scale:[1.0f,1.0f,1.0f]}}
    #Notes:
    #~ ~ ~ will be replaced by variables based on direction and scale. These determine pixel position.
    #scale:[0.5f,0.5f,0.5f] will be based on scale float variable, however they are not 1:1 and a formula will be needed.
    #I am unsure how to choose transformations to get a desired direction. Maybe I'll replace direction with two rotatations, one for left and right, the other for up and down.
    
def main():
    
    print(generateCommand())
    
    return
    
    logging.debug(f'Running {__name__}')
    
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
        hex_array = generateImageHexArray(image)
    except Exception as e:
        logging.fatal(f'Something went wrong while converting the image into an array due to {repr(e)}.')
        exit(1)
    
    #Test the hex array
    width, height = image.size
    for y in range(height):
        row_hex_values = hex_array[y]
        row_hex_string = ' '.join(str(hex_value) if hex_value is not None else 'None' for hex_value in row_hex_values)
        print(row_hex_string)
    
    try:
        generateCommand('North')
    except Exception as e:
        logging.error(f'Could not generate command due to {repr(e)}')
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
