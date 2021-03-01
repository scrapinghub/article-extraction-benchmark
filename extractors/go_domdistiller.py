#!/usr/bin/env python3
import gzip
import json
import os
import subprocess
from pathlib import Path
from tempfile import mkstemp


# built executable file
CLI_PATH = Path('extractors/go_domdistiller/go_domdistiller_cli')


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]

        # save html to temp file
        temp_filepath = mkstemp()[1]
        with open(temp_filepath, 'wt') as fw:
            fw.write(html)

        # get extracted content from go-readadbility
        result = subprocess.run([CLI_PATH, temp_filepath], stdout=subprocess.PIPE)

        # destroy temp file
        os.remove(temp_filepath)

        output[item_id] = {'articleBody': result.stdout.decode('utf-8')}
    (Path('output') / 'go_domdistiller.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8')


if __name__ == '__main__':
    main()
