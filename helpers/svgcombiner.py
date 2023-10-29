import re
from pathlib import Path


def svgcombiner(base: Path, svg: Path) -> str:
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
