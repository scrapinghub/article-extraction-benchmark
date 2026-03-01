#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

from html2text import HTML2Text

from output_util import python_dist_version, write_output_json


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        h = HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        content = h.handle(html)
        output[item_id] = {'articleBody': content}
    write_output_json(
        Path("output") / "html2text.json",
        output=output,
        version=python_dist_version("html2text"),
    )


if __name__ == '__main__':
    main()
