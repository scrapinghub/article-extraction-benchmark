#!/usr/bin/env python2
import codecs
import gzip
import json
import glob
import os.path

from boilerpipe.extract import Extractor


def main():
    output = {}
    for path in glob.glob('html/*.html.gz'):
        with gzip.open(path, 'rb') as f:
            html = f.read().decode('utf8')
        item_id = os.path.basename(path).split('.')[0]
        extractor = Extractor(extractor='ArticleExtractor', html=html)
        output[item_id] = {'articleBody': extractor.getText()}
    with codecs.open(os.path.join('output', 'boilerpipe.json'),
                     'wt', encoding='utf8') as f:
        json.dump(output, f, sort_keys=True, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
