#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

from inscriptis import get_text

from output_util import python_dist_version, write_output_json


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        content = get_text(html)
        output[item_id] = {'articleBody': content}
    write_output_json(
        Path("output") / "inscriptis.json",
        output=output,
        version=python_dist_version("inscriptis"),
    )


if __name__ == '__main__':
    main()
