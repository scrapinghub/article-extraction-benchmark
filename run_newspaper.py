#!/usr/bin/env python3
import gzip
import json
from pathlib import Path

from newspaper import Article


def main():
    output = {}
    url_by_item_id = {item_id: item['url'] for item_id, item in json.loads(
        Path('ground-truth.json').read_text('utf8')).items()}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]
        article = Article(url_by_item_id[item_id])
        article.set_html(html)
        article.parse()
        output[item_id] = {'articleBody': article.text}
    Path('output-newspaper.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8')


if __name__ == '__main__':
    main()
