#!/usr/bin/env python3
import gzip
import json
import subprocess
import sys
from pathlib import Path
from tempfile import mkstemp


# built executable file
CLI_PATH = Path('extractors/go_trafilatura/go_trafilatura_cli')


def normalize(s: str) -> str:
    # remove all U+00AD (SOFT HYPHEN)
    return s.replace('\u00ad', '')

def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()

        result = subprocess.run(CLI_PATH, text=True, input=html, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"Error processing {path}: {result.stderr}", file=sys.stderr)

        item_id = path.stem.split('.')[0]
        output[item_id] = {'articleBody': normalize(result.stdout)}
    (Path('output') / 'go_trafilatura.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8')


if __name__ == '__main__':
    main()
