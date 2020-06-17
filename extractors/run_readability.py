#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

import html_text
from readability import Document


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        doc = Document(html)
        text = html_text.extract_text(doc.summary(html_partial=True))
        output[item_id] = {'articleBody': text}
    (Path('output') / 'readability.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8')


if __name__ == '__main__':
    main()
