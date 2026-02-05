import json
import re
from pathlib import Path
from typing import Any, Dict, Optional


def wrap_output(*, output: Dict[str, Dict[str, Any]], version: Optional[str]) -> Dict[str, Any]:
    return {
        "version": version or "",
        "output": output,
    }


def write_output_json(path: Path, *, output: Dict[str, Dict[str, Any]], version: Optional[str]) -> None:
    path.write_text(
        json.dumps(wrap_output(output=output, version=version), sort_keys=True, ensure_ascii=False, indent=4),
        encoding="utf8",
    )


def python_dist_version(dist_name: str) -> Optional[str]:
    try:
        from importlib.metadata import PackageNotFoundError, version  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover
        try:
            from importlib_metadata import PackageNotFoundError, version  # type: ignore
        except Exception:
            return None
    try:
        return version(dist_name)
    except PackageNotFoundError:
        return None


_GO_REQUIRE_RE = re.compile(r"^\\s*require\\s+(?P<module>\\S+)\\s+(?P<version>\\S+)\\s*$")
_GO_BLOCK_ENTRY_RE = re.compile(r"^\\s*(?P<module>\\S+)\\s+(?P<version>\\S+)\\s*$")


def go_mod_dep_version(go_mod_path: Path, module_path: str) -> Optional[str]:
    if not go_mod_path.exists():
        return None
    in_block = False
    for raw_line in go_mod_path.read_text(encoding="utf8").splitlines():
        line = raw_line.split("//", 1)[0].rstrip()
        if not line:
            continue
        if line.startswith("require ("):
            in_block = True
            continue
        if in_block and line == ")":
            in_block = False
            continue
        if in_block:
            m = _GO_BLOCK_ENTRY_RE.match(line)
            if m and m.group("module") == module_path:
                return _shorten_go_version(m.group("version"))
            continue
        m = _GO_REQUIRE_RE.match(line)
        if m and m.group("module") == module_path:
            return _shorten_go_version(m.group("version"))
    return None


def _shorten_go_version(v: str) -> str:
    # Keep semver (v1.2.3) as-is; for pseudo versions, prefer the commit suffix.
    # Examples:
    # - v0.0.0-20250217085726-9f5bf5ca7612 -> 9f5bf5c
    # - v1.12.3-0.20250515093937-ae7ea0621e7c -> ae7ea06
    parts = v.split("-")
    if len(parts) >= 3 and re.fullmatch(r"[0-9a-f]{12,40}", parts[-1]):
        return parts[-1][:7]
    return v


def node_dependency_version(package_json_path: Path, dep_name: str) -> Optional[str]:
    if not package_json_path.exists():
        return None
    try:
        data = json.loads(package_json_path.read_text(encoding="utf8"))
    except Exception:
        return None
    deps = data.get("dependencies") or {}
    v = deps.get(dep_name)
    return str(v) if v is not None else None


def cargo_lock_package_version(cargo_lock_path: Path, package_name: str) -> Optional[str]:
    if not cargo_lock_path.exists():
        return None
    text = cargo_lock_path.read_text(encoding="utf8")
    blocks = text.split("[[package]]")
    for b in blocks:
        if f'name = "{package_name}"' not in b:
            continue
        version = _cargo_field(b, "version")
        source = _cargo_field(b, "source")
        if source and source.startswith("git+"):
            if "#" in source:
                rev = source.rsplit("#", 1)[-1]
                if re.fullmatch(r"[0-9a-f]{12,40}", rev):
                    return rev[:7]
            return version or source
        return version
    return None


def _cargo_field(block: str, field: str) -> Optional[str]:
    m = re.search(rf'^{re.escape(field)}\\s*=\\s*\"([^\"]+)\"\\s*$', block, flags=re.MULTILINE)
    return m.group(1) if m else None

