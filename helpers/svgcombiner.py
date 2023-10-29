import re
from pathlib import Path
import os

import cairosvg
import imageio


def svg_combine(base: Path, svg: Path) -> str:
    with open(base, "r") as f:
        base = f.read()
    with open(svg, "r") as f:
        svg = f.read()

    # Find the index where </g><text starts in the base
    index = base.find('</g><text')

    match = re.search('(<p.*\/p>)', svg, re.DOTALL)

    match.group(0)
    # Insert the svg data at the found index
    combined = base[:index] + "<p" + svg + "/p>" + base[index:]

    return combined


def svg_to_gif(svg_paths, gif_path):
    # 创建一个临时文件夹
    if not os.path.exists('temp'):
        os.makedirs('temp')

    png_paths = []
    for i, svg_path in enumerate(svg_paths):
        png_path = f'cache/{i}.png'
        png_paths.append(png_path)

        # 将SVG转换为PNG
        cairosvg.svg2png(url=svg_path, write_to=png_path)

    # 读取所有的PNG图片，并存储到images列表中
    images = [imageio(png_path) for png_path in png_paths]

    # 将所有图片拼接成gif
    imageio.mimsave(gif_path, images)

    # 删除临时图片
    for png_path in png_paths:
        os.remove(png_path)

    print(f'Successfully saved the gif to {gif_path}.')
