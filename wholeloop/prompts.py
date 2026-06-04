"""Tiny interactive TTY helpers for WholeLoop wizards (no third-party deps).

Every prompt has a sensible default so pressing Enter advances. Wizards must
check `no_prompt()` first and fall back to flags / defaults in CI and pipes.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


class PromptAborted(Exception):
    """Raised when the user presses Ctrl-C / Ctrl-D mid-wizard."""


def no_prompt() -> bool:
    """True when we must not ask questions (non-TTY or explicit opt-out)."""
    if os.environ.get("WHOLELOOP_NO_PROMPT"):
        return True
    return not (sys.stdin.isatty() and sys.stdout.isatty())


def _read(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print(file=sys.stderr)
        raise PromptAborted from None


def banner(title: str, subtitle: str | None = None) -> None:
    print()
    print(f"  WholeLoop · {title}")
    if subtitle:
        print(f"  {subtitle}")
    print()


def info(msg: str) -> None:
    print(f"  {msg}")


def success(msg: str) -> None:
    print(f"  \u2713 {msg}")


def hint(msg: str) -> None:
    print(f"  \u2192 {msg}")


def ask_yes_no(question: str, *, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        raw = _read(f"? {question} {suffix} ").strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("    Please answer y or n.")


def ask_text(question: str, *, default: str | None = None, required: bool = False) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        raw = _read(f"? {question}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        if not raw and not required:
            return ""
        if raw:
            return raw
        print("    A value is required.")


def ask_choice(
    question: str,
    options: list[tuple[str, str]],
    *,
    default_index: int = 0,
) -> str:
    """Render a numbered menu. `options` is a list of (value, label). Returns value."""
    print(f"? {question}")
    for i, (_, label) in enumerate(options):
        marker = "\u203a" if i == default_index else " "
        print(f"  {marker} {i + 1}. {label}")
    while True:
        raw = _read(f"  Choose 1-{len(options)} [{default_index + 1}]: ").strip()
        if not raw:
            return options[default_index][0]
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][0]
        print(f"    Enter a number between 1 and {len(options)}.")


def ask_path(
    question: str,
    *,
    default: str | None = None,
    must_exist: bool = False,
) -> Path:
    while True:
        raw = ask_text(question, default=default, required=True)
        path = Path(raw).expanduser()
        if must_exist and not path.exists():
            print(f"    Path does not exist: {path}")
            continue
        return path
