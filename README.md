# Image to Text Display

This is a python script that reads image files and generates a function that creates the image in minecraft using text display entities and a colored ■ character (ALT+254).

Please note, each pixel in the image will be its own entity in game, so the higher the resolution, the more entities that will be summoned. A 10x10 image will have 100 text_display entities summoned for example!

![image](https://github.com/RandomGgames/ImageToTextDisplay/assets/17207260/d916a850-666f-4741-9495-dc54fd79cc9e)

## How to use it

### Requirements
This python script relies on the yaml lib for the config file. `pip install pyyaml` https://pypi.org/project/PyYAML/

### Edit the `config.yaml` file
1. Set the `image_file` to the path of the image you want to generate.
2. Set the `output_file` to the path of the .mcfunction file that will be generated, containing the list of summon commands.
3. Run the `Convert.py` script , place your `output_file` into a datapack, and run the function.
