#!/usr/bin/env python3
import gzip
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

from output_util import write_output_json

logger = logging.getLogger(__name__)

MODEL_ID = "jinaai/ReaderLM-v2"

STRIP_PATTERNS = [
    re.compile(r"<\s*script.*?/\s*script\s*>", re.IGNORECASE | re.DOTALL),
    re.compile(r"<\s*style.*?/\s*style\s*>", re.IGNORECASE | re.DOTALL),
    re.compile(r"<\s*meta.*?>", re.IGNORECASE | re.DOTALL),
    re.compile(r"<\s*link.*?>", re.IGNORECASE | re.DOTALL),
    re.compile(r"<\s*!--.*?--\s*>", re.IGNORECASE | re.DOTALL),
]

JSON_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "articleBody": {
                "type": "string",
                "description": "The main article body text",
            }
        },
        "required": ["articleBody"],
    },
    indent=2,
)

INSTRUCTION = (
    "Extract the specified information from the given HTML"
    " and present it in a structured JSON format."
)


def clean_html(html: str) -> str:
    for pattern in STRIP_PATTERNS:
        html = pattern.sub("", html)
    return html


def build_prompt(html: str, tokenizer: AutoTokenizer) -> str:
    content = (
        f"{INSTRUCTION}\n"
        f"```html\n{html}\n```\n"
        f"The JSON schema is as follows:\n```json\n{JSON_SCHEMA}\n```"
    )
    messages = [{"role": "user", "content": content}]
    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )


_FENCE_RE = re.compile(r"```(?:json)?\s*\n?(.*?)\n?\s*```", re.DOTALL)


def parse_article_body(raw_output: str) -> str:
    text = raw_output.strip()
    m = _FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "articleBody" in data:
            return data["articleBody"]
    except json.JSONDecodeError:
        pass
    # Fallback: try to find the first JSON object in the raw output
    for match in re.finditer(r"\{.*?\}", raw_output, re.DOTALL):
        try:
            data = json.loads(match.group())
            if isinstance(data, dict) and "articleBody" in data:
                return data["articleBody"]
        except json.JSONDecodeError:
            continue
    return ""


def get_model_version(model: AutoModelForCausalLM) -> str:
    cfg = model.config
    name = getattr(cfg, "_name_or_path", MODEL_ID)
    rev = getattr(cfg, "_commit_hash", None)
    if rev:
        return f"{name}@{rev[:7]}"
    return name


def _cuda_failure_help() -> str:
    lines = [
        "ERROR: CUDA is not available. This extractor requires a working GPU + CUDA PyTorch build.",
        "",
    ]
    cvd = os.environ.get("CUDA_VISIBLE_DEVICES")
    if cvd == "":
        lines.append(
            "CUDA_VISIBLE_DEVICES is set to an empty string, which hides all GPUs. Unset it or set e.g. 0."
        )
        lines.append("")
    try:
        proc = subprocess.run(
            ["nvidia-smi", "-L"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        smi = (proc.stdout or "").strip()
        if proc.returncode == 0 and smi:
            lines.append(
                "nvidia-smi reports GPUs, but PyTorch could not initialize CUDA. Typical causes:"
            )
            lines.append(
                "  - PyTorch was built for a different CUDA than your driver (reinstall from pytorch.org)."
            )
            lines.append(
                "  - Docker: pass --gpus all and install the NVIDIA Container Toolkit so /dev/nvidia* is visible."
            )
            lines.append(
                "  - Do not change CUDA_VISIBLE_DEVICES after the process has started importing torch."
            )
            lines.append("")
            lines.append("nvidia-smi -L:")
            lines.append(smi[:800])
        else:
            lines.append(
                "nvidia-smi did not list GPUs (or failed). Install NVIDIA drivers or enable GPU passthrough."
            )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        lines.append("Could not run nvidia-smi (not in PATH or failed).")
    lines.append("")
    lines.append(
        f"PyTorch {torch.__version__}, torch.version.cuda={getattr(torch.version, 'cuda', None)!r}"
    )
    return "\n".join(lines)


def main():
    if not torch.cuda.is_available():
        print(_cuda_failure_help(), file=sys.stderr)
        sys.exit(1)

    device = "cuda"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float16
    ).to(device)
    version = get_model_version(model)

    html_paths = sorted(Path("html").glob("*.html.gz"))
    output = {}
    for path in tqdm(html_paths, desc="readerlmv2"):
        with gzip.open(path, "rt", encoding="utf8") as f:
            html = f.read()
        item_id = path.stem.split(".")[0]
        cleaned = clean_html(html)
        prompt = build_prompt(cleaned, tokenizer)
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            generated = model.generate(
                inputs,
                max_new_tokens=4096,
                temperature=0,
                do_sample=False,
                repetition_penalty=1.08,
            )
        raw = tokenizer.decode(
            generated[0][inputs.shape[-1]:], skip_special_tokens=True
        )
        body = parse_article_body(raw)
        if not body:
            logger.warning("failed to parse articleBody for %s", item_id)
        output[item_id] = {"articleBody": body}

    write_output_json(
        Path("output") / "readerlmv2.json",
        output=output,
        version=version,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
