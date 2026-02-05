#!/usr/bin/env python3
import gzip
import json
import subprocess
import sys
from pathlib import Path

from output_util import node_dependency_version, write_output_json


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        item_id = path.stem.split('.')[0]

        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()
        
        # get extracted content from Readability.js
        result = subprocess.run(
            ["node", "cli.js"],
            input=html,
            cwd=Path(__file__).parent / "readability_js",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"Error processing {path}: {result.stderr}", file=sys.stderr)
            continue

        output[item_id] = {'articleBody': result.stdout}
    write_output_json(
        Path("output") / "readability_js.json",
        output=output,
        version=node_dependency_version(
            Path(__file__).parent / "readability_js" / "package.json",
            "@mozilla/readability",
        ),
    )


if __name__ == '__main__':
    main()
