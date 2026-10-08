from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys

from .core import SDK_VERSION, build_prompt, validate_case
from .providers import provider_from_name


def _load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dump(value, path: str | None) -> None:
    text = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if path:
        Path(path).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def _analyze(args, developer: bool) -> int:
    provider = provider_from_name(args.provider, args.model, args.base_url)
    raw = provider.generate(build_prompt(args.event, developer=developer), args.event)
    try:
        case = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"provider did not return valid JSON: {exc}", file=sys.stderr)
        return 2
    result = validate_case(case)
    if not result.valid:
        for error in result.errors:
            print(error, file=sys.stderr)
        return 2
    _dump(case, args.out)
    return 0


def _validate(args) -> int:
    result = validate_case(_load_json(args.path))
    if result.valid:
        print("EISf case valid")
        return 0
    for error in result.errors:
        print(error, file=sys.stderr)
    return 1


def _conformance(args) -> int:
    root = Path(__file__).resolve().parents[2]
    manifest_path = root / "conformance" / "manifest.json"
    if not manifest_path.exists():
        manifest_path = Path("conformance/manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    passed = 0

    for item in manifest["fixtures"]:
        case = json.loads((manifest_path.parent / item["file"]).read_text(encoding="utf-8"))
        expected = bool(item["valid"])
        if args.driver:
            proc = subprocess.run(
                shlex.split(args.driver),
                input=json.dumps({"operation": "validate", "case": case}),
                capture_output=True,
                text=True,
                timeout=30
            )
            try:
                response = json.loads(proc.stdout)
                actual = bool(response.get("valid"))
                if actual and not isinstance(response.get("case"), dict):
                    actual = False
            except json.JSONDecodeError:
                actual = False
        else:
            actual = validate_case(case).valid

        ok = actual == expected
        passed += int(ok)
        print(f"{item['id']} {'PASS' if ok else 'FAIL'}")

    total = len(manifest["fixtures"])
    print(f"CONFORMANCE: {passed} / {total} PASS")
    if passed == total:
        print("EISf Core Compatible — Self-Tested against EISf Conformance Suite v0.1")
        return 0
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eisf")
    parser.add_argument("--version", action="version", version=SDK_VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate an EISf JSON case")
    validate.add_argument("path")
    validate.set_defaults(func=_validate)

    for name, developer in (("analyze", False), ("dev", True)):
        cmd = sub.add_parser(name)
        cmd.add_argument("event")
        cmd.add_argument("--provider", choices=["mock", "openai", "responses", "ollama"], default="mock")
        cmd.add_argument("--model")
        cmd.add_argument("--base-url")
        cmd.add_argument("--out")
        cmd.set_defaults(func=lambda args, d=developer: _analyze(args, d))

    conf = sub.add_parser("conformance")
    conf.add_argument("--driver", help="external driver command; receives one JSON request on stdin")
    conf.set_defaults(func=_conformance)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
