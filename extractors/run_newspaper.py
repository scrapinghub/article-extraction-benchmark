#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

import newspaper

from output_util import python_dist_version, write_output_json


def main():
    output = {}
    url_by_item_id = {item_id: item['url'] for item_id, item in json.loads(
        Path('ground-truth.json').read_text('utf8')).items()}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        article = newspaper.article(url_by_item_id[item_id], input_html=html)
        article.parse()
        output[item_id] = {'articleBody': article.text}
    write_output_json(
        Path("output") / "newspaper.json",
        output=output,
        version=python_dist_version("newspaper4k"),
    )


if __name__ == '__main__':
    main()
