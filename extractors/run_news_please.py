#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

from newsplease import NewsPlease

from output_util import python_dist_version, write_output_json


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        article = NewsPlease.from_html(html, url=None)
        output[item_id] = {'articleBody': article.maintext}
    write_output_json(
        Path("output") / "news_please.json",
        output=output,
        version=python_dist_version("news-please"),
    )


if __name__ == '__main__':
    main()
