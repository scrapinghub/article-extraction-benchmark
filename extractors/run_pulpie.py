#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

import tqdm
import trafilatura
from pulpie import Extractor

from output_util import python_dist_version, write_output_json


def main():

    extractor = Extractor()
    output = {}
    for path in tqdm.tqdm(Path('html').glob('*.html.gz')):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        result = extractor.extract(html)
        article = trafilatura.extract(result.html, include_comments=False)
        output[item_id] = {'articleBody': article}
    write_output_json(
        Path("output") / "pulpie.json",
        output=output,
        version=python_dist_version("pulpie"),
    )


if __name__ == '__main__':
    main()
