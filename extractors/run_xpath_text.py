#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

import lxml.html


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
    (Path('output') / 'xpath-text.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8')


if __name__ == '__main__':
    main()
