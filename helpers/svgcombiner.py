import re
from pathlib import Path
import os

from config import CACHE_PATH
from imageio import imopen
import imageio


def svg_combine(base: Path, svg: Path) -> str:
    with open(base, "r") as f:
        base = f.read()
    with open(svg, "r") as f:
        svg = f.read()

    # Find the index where </g><text starts in the base
    index = base.find('</g><text')

    match = re.search('(<g.*/g>)', svg, re.DOTALL)

    match.group(0)
    # Insert the svg data at the found index
    combined = base[:index] + svg  + base[index:]

    return combined


def svg_to_gif(svg_paths, gif_path):
    png_paths = [a for a in os.listdir(svg_paths) if a.endswith(".svg")]
    
    os.system("cd " + str(CACHE_PATH.absolute()) + " && for file in *.svg; do inkscape \"$file\" -o \"${file%svg}png\"; done")
    # 读取所有的PNG图片，并存储到images列表中
    images = [imopen(png_path, 'r') for png_path in png_paths]

    # 将所有图片拼接成gif
    imageio.mimsave(gif_path, images)

    # 删除临时图片
    for png_path in png_paths:
        os.remove(png_path)

    print(f'Successfully saved the gif to {gif_path}.')
