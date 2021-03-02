#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

from goose3 import Goose


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        g = Goose()
        article = g.extract(raw_html=html)
        output[item_id] = {'articleBody': article.cleaned_text}
    (Path('output') / 'goose3.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8')


if __name__ == '__main__':
    main()
