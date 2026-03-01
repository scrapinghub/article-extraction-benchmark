#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

import html_text
from readability import Document

from output_util import python_dist_version, write_output_json


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        doc = Document(html)
        text = html_text.extract_text(doc.summary(html_partial=True))
        output[item_id] = {'articleBody': text}
    write_output_json(
        Path("output") / "readability.json",
        output=output,
        version=python_dist_version("readability-lxml"),
    )


if __name__ == '__main__':
    main()
