import re
from pathlib import Path
import os

from config import CACHE_PATH
from PIL import Image
import glob

def svg_combine(base: Path, svg: Path, isAlert: bool) -> str:
    with open(base, "r") as f:
        base = f.read()
    with open(svg, "r") as f:
        svg = f.read()
    
    body = lambda x: re.search("""xmlns="http:\/\/www\.w3\.org\/2000\/svg" xmlns:ev="http:\/\/www\.w3\.org\/2001\/xml-events" xmlns:xlink="http:\/\/www\.w3\.org\/1999\/xlink">(.*)<\/svg>""", x, re.DOTALL)[0].removesuffix("</svg>")
    head = lambda x: """<?xml version="1.0" encoding="utf-8" ?>""" +re.search("""<svg(.*?)">""", x, re.DOTALL)[0]
    bgc = re.search("""<rect fill="#eee" height="(.*)" width="(.*)" x="0.0" y="0.0" />""", svg, re.DOTALL)[0]
    tail = "</svg>"

    alert = """<path class="st0" d="M103.2,62.5c0-24.2-20.4-43.7-45.6-43.7S11.9,38.3,11.9,62.5s20.4,43.7,45.6,43.7S103.2,86.6,103.2,62.5
	L103.2,62.5L103.2,62.5L103.2,62.5L103.2,62.5L103.2,62.5z M17.3,62.5c0-21.3,18-38.6,40.3-38.6s40.3,17.3,40.3,38.6
	s-18,38.6-40.3,38.6S17.3,83.8,17.3,62.5L17.3,62.5L17.3,62.5L17.3,62.5L17.3,62.5L17.3,62.5z" fill="#FC5143"/>
<path class="st0" d="M53.8,73.6c0,2.7,1.3,4.1,3.8,4.1c2.5,0,3.8-1.4,3.8-4.1V35.7c0-2.7-1.3-4.1-3.8-4.1c-2.5,0-3.8,1.4-3.8,4.1
	V73.6z M53.1,90.3c0.2,2.7,1.7,4.1,4.4,4.1c2.7,0,4.2-1.4,4.4-4.1c-0.2-2.7-1.7-4.2-4.4-4.4C54.8,86.1,53.4,87.6,53.1,90.3
	L53.1,90.3z" fill="#FC5143"/>"""

    # Find the index where </g><text starts in the base
    # index = base.find('</g><text')
    # match = re.search('(<g.*/g>)', svg, re.DOTALL)

    # if match is None:
    #     index = base.find('/><text')
    #     match = re.search('(<path.*/>)', svg, re.DOTALL)
    # Insert the svg data at the found index
    # combined = base[:index] + match.group(0)  + base[index:]
    # return combined

    if bgc:
        if isAlert:
            return head(base) + body(base) + body(svg).replace(bgc, "") + alert + tail
        return head(base) + body(base) + body(svg).replace(bgc, "") + tail
    if isAlert:
        return head(base) + body(base) + body(svg) + alert + tail
    return head(base) + body(base) + body(svg) + tail


def svg_to_gif(svg_paths, gif_path):
    
    os.system("cd " + str(CACHE_PATH.absolute()) + " && for file in *.svg; do inkscape \"$file\" -o \"${file%svg}png\"; done")

    # Create the frames
    frames: list[Image.Image] = []
    imgs = glob.glob("*.png", root_dir=svg_paths)
    for i in imgs:
        if not ("line" in i or "base" in i):
            new_frame = Image.open(CACHE_PATH / i)
            frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(CACHE_PATH / 'png_to_gif.gif', format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=500, loop=0)

    print(f'Successfully saved the gif to {gif_path}.')