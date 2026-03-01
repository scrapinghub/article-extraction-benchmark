#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

import lxml.html

from output_util import python_dist_version, write_output_json


def xpath_text(html: str) -> str:
    root = lxml.html.fromstring(html)
    bodies = root.xpath('//body')
    if bodies:
        root = bodies[0]
    return ' '.join(root.xpath('.//text()'))


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        output[item_id] = {'articleBody': xpath_text(html)}
    write_output_json(
        Path("output") / "xpath-text.json",
        output=output,
        version=python_dist_version("lxml"),
    )


if __name__ == '__main__':
    main()
