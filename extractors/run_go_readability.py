#!/usr/bin/env python3
import gzip
import json
import subprocess
import sys
from pathlib import Path

from output_util import go_mod_dep_version, write_output_json


# built executable file
CLI_PATH = Path('extractors/go_readability/go_readability_cli')


def normalize(s: str) -> str:
    # remove all U+00AD (SOFT HYPHEN)
    return s.replace('\u00ad', '')


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        item_id = path.stem.split('.')[0]

        # get extracted content from go-readadbility
        result = subprocess.run(CLI_PATH, input=html, text=True, stdout=subprocess.PIPE)
        if result.returncode != 0:
            print("failed: ",path,file=sys.stderr)

        output[item_id] = {'articleBody': normalize(result.stdout)}
    write_output_json(
        Path("output") / "go_readability.json",
        output=output,
        version=go_mod_dep_version(
            Path("extractors/go_readability/go.mod"),
            "github.com/go-shiori/go-readability",
        ),
    )


if __name__ == '__main__':
    main()
