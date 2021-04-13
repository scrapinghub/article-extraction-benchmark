#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

import justext


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        article = ' '.join(
            [p.text for p in justext.justext(html, justext.get_stoplist("English"), 50, 200, 0.1, 0.2, 0.2, 200, True)
             if not p.is_boilerplate])
        output[item_id] = {'articleBody': article}
    (Path('output') / 'justext.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8')


if __name__ == '__main__':
    main()
