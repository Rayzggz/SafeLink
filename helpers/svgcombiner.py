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
    
    body = lambda x: re.search("""xmlns="http:\/\/www\.w3\.org\/2000\/svg" xmlns:ev="http:\/\/www\.w3\.org\/2001\/xml-events" xmlns:xlink="http:\/\/www\.w3\.org\/1999\/xlink">(.*)<\/svg>""", x, re.DOTALL)[0].removesuffix("</svg>")
    head = lambda x: """<?xml version="1.0" encoding="utf-8" ?>""" +re.search("""<svg(.*?)">""", x, re.DOTALL)[0]
    tail = "</svg>"

    # # Find the index where </g><text starts in the base
    # index = base.find('</g><text')
    # print(index)
    # match = re.search('(<g.*/g>)', svg, re.DOTALL)

    # if match is None:
    #     index = base.find('/><text')
    #     match = re.search('(<path.*/>)', svg, re.DOTALL)
    # # Insert the svg data at the found index
    # combined = base[:index] + match.group(0)  + base[index:]

    return head(base) + body(base) + body(svg) + tail


def svg_to_gif(svg_paths, gif_path):
    
    os.system("cd " + str(CACHE_PATH.absolute()) + " && for file in *.svg; do inkscape \"$file\" -o \"${file%svg}png\"; done")

    # Create the frames
    frames = []
    imgs = glob.glob("*.png", root_dir=svg_paths)
    for i in imgs:
        if not ("line" in i or "base" in i):
            new_frame = Image.open(CACHE_PATH / i)
            frames.append(new_frame)
    print(frames)

    # Save into a GIF file that loops forever
    frames[0].save(CACHE_PATH / 'png_to_gif.gif', format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=300, loop=0)

    print(f'Successfully saved the gif to {gif_path}.')