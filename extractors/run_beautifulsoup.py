#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

from bs4 import BeautifulSoup

from output_util import python_dist_version, write_output_json


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        bs = BeautifulSoup(html, 'html.parser')
        article = bs.get_text(separator=' ', strip=True)
        output[item_id] = {'articleBody': article}
    write_output_json(
        Path("output") / "beautifulsoup.json",
        output=output,
        version=python_dist_version("beautifulsoup4"),
    )


if __name__ == '__main__':
    main()
