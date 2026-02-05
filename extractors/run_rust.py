#!/usr/bin/env python3
import gzip
import json
import subprocess
import sys
from pathlib import Path

from output_util import cargo_lock_package_version, write_output_json


CLI_PATH = Path("extractors/rust_extractors/target/release/rust_extractors_cli")
LOCK_PATH = Path("extractors/rust_extractors/Cargo.lock")

BACKENDS = [
    ("august", "august.json"),
    ("boilerpipe", "boilerpipe_rs.json"),
    ("dom_smoothie", "dom_smoothie.json"),
    ("fast_html2md", "fast_html2md.json"),
    ("htmd", "htmd.json"),
    ("html2md-rs", "html2md_rs.json"),
    ("html2text", "html2text_rs.json"),
    ("llm_readability", "llm_readability.json"),
    ("mdka", "mdka.json"),
    ("nanohtml2text", "nanohtml2text.json"),
    ("readability", "readability_rs.json"),
    ("readable-readability", "readable_readability.json"),
    ("rs_trafilatura", "rs_trafilatura.json"),
    ("readabilityrs", "readabilityrs.json"),
]

BACKEND_TO_PACKAGE = {
    "august": "august",
    "boilerpipe": "boilerpipe",
    "dom_smoothie": "dom_smoothie",
    "fast_html2md": "fast_html2md",
    "htmd": "htmd",
    "html2md-rs": "html2md-rs",
    "html2text": "html2text",
    "llm_readability": "llm_readability",
    "mdka": "mdka",
    "nanohtml2text": "nanohtml2text",
    "readability": "readability",
    "readabilityrs": "readabilityrs",
    "readable-readability": "readable-readability",
    "rs_trafilatura": "rs-trafilatura",
}


def normalize(s: str) -> str:
    return s.replace("\u00ad", "")


def load_urls() -> dict:
    path = Path("ground-truth.json")
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf8"))
    return {item_id: payload.get("url") for item_id, payload in data.items()}


def run_backend(backend: str, output_name: str, urls: dict) -> None:
    if not CLI_PATH.exists():
        raise SystemExit(
            f"Missing Rust CLI at {CLI_PATH}. Run `make -C extractors/rust_extractors build` first."
        )
    output = {}
    for path in Path("html").glob("*.html.gz"):
        with gzip.open(path, "rt", encoding="utf8") as f:
            html = f.read()
        item_id = path.stem.split(".")[0]
        cmd = [str(CLI_PATH), backend]
        url = urls.get(item_id)
        if url:
            cmd.extend(["--url", url])
        result = subprocess.run(
            cmd, text=True, input=html, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            print(
                f"Error processing {path} with {backend}: {result.stderr.strip()}",
                file=sys.stderr,
            )
            content = ""
        else:
            content = normalize(result.stdout)
        output[item_id] = {"articleBody": content}
    package_name = BACKEND_TO_PACKAGE.get(backend)
    version = cargo_lock_package_version(LOCK_PATH, package_name) if package_name else None
    write_output_json(Path("output") / output_name, output=output, version=version)


def main() -> None:
    urls = load_urls()
    for backend, output_name in BACKENDS:
        run_backend(backend, output_name, urls)


if __name__ == "__main__":
    main()
