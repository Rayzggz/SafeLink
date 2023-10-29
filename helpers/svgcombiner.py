import re
from pathlib import Path
import os

from config import CACHE_PATH
from PIL import Image
import glob

def svg_combine(base: Path, svg: Path) -> str:
    with open(base, "r") as f:
        base = f.read()
    with open(svg, "r") as f:
        svg = f.read()

    # Find the index where </g><text starts in the base
    index = base.find('</g><text')

    match = re.search('(<g.*/g>)', svg, re.DOTALL)


    # Insert the svg data at the found index
    combined = base[:index] + match.group(0)  + base[index:]

    return combined


def svg_to_gif(svg_paths, gif_path):
    
    os.system("cd " + str(CACHE_PATH.absolute()) + " && for file in *.svg; do inkscape \"$file\" -o \"${file%svg}png\"; done")

    # Create the frames
    frames = []
    imgs = glob.glob("*.png", root_dir=svg_paths)
    for i in imgs:
        new_frame = Image.open(CACHE_PATH / i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(CACHE_PATH / 'png_to_gif.gif', format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=300, loop=0)

    print(f'Successfully saved the gif to {gif_path}.')