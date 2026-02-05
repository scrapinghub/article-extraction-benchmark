#!/usr/bin/env python3
import gzip
import json
import subprocess
import sys
from pathlib import Path

from output_util import go_mod_dep_version, write_output_json


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
    write_output_json(
        Path("output") / "go_trafilatura.json",
        output=output,
        version=go_mod_dep_version(
            Path("extractors/go_trafilatura/go.mod"),
            "github.com/markusmobius/go-trafilatura",
        ),
    )


if __name__ == '__main__':
    main()
