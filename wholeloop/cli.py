"""WholeLoop command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from wholeloop import __version__
from wholeloop.assets import skills_src
from wholeloop.doctor import run_doctor
from wholeloop.install import install_app, update_skills
from wholeloop.conventions import bootstrap_conventions, import_conventions
from wholeloop.pipeline import (
    OPTIONAL_SKILL_DIRS,
    PIPELINE_LINE,
    PIPELINE_VERSION,
    REMOVED_SKILL_DIRS,
    REQUIRED_SKILL_DIRS,
    list_installed_skills,
)


def _print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)


def _next_steps_v02() -> None:
    print("  Next steps:")
    print("    1. Run project-conventions agent in IDE (confirm CLI bootstrap)")
    print("    2. Read WHOLELOOP.md — pipeline v0.2")
    print("    3. wholeloop doctor")
    print("    4. Start a run: spec-review (ARTIFACT-WAL and/or epic ref)")


def cmd_init(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    try:
        lines = install_app(
            app,
            force=args.force,
            copy_ide_skills=args.copy_ide_skills,
            conventions_from=getattr(args, "conventions_from", None),
        )
    except (FileExistsError, FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    _print_lines(lines)
    print()
    print(f"WholeLoop {__version__} installed (Cursor, Claude Code, VS Code).")
    print(f"  App:         {app}")
    _next_steps_v02()
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    try:
        lines = update_skills(
            app,
            keep_conventions=args.keep_conventions,
            copy_ide_skills=args.copy_ide_skills,
            refresh_docs=not args.no_refresh_docs,
        )
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    _print_lines(lines)
    print()
    print(f"Skills updated to WholeLoop v{PIPELINE_VERSION} in {app}")
    if args.no_refresh_docs:
        print("  Docs unchanged (--no-refresh-docs). Consider refreshing WHOLELOOP.md manually.")
    print("  If conventions changed: wholeloop conventions bootstrap")
    print("  Then: wholeloop doctor")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    ok, lines = run_doctor(app)
    print("\n".join(lines))
    return 0 if ok else 1


def cmd_skills(_: argparse.Namespace) -> int:
    root = skills_src()
    installed = list_installed_skills(root)
    print(f"wholeloop {__version__} — bundled skills ({len(installed)})")
    print(f"Pipeline v{PIPELINE_VERSION}: {PIPELINE_LINE}")
    print()
    print("Required:")
    for name in REQUIRED_SKILL_DIRS:
        mark = "✓" if name in installed else "✗"
        print(f"  {mark} {name}")
    print()
    print("Optional:")
    for name in OPTIONAL_SKILL_DIRS:
        mark = "✓" if name in installed else "·"
        print(f"  {mark} {name}")
    print()
    print("Removed in v0.2 (should not appear after update):")
    for name in REMOVED_SKILL_DIRS:
        mark = "✗ STALE" if name in installed else "—"
        print(f"  {mark} {name}")
    return 0


def cmd_conventions_bootstrap(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    try:
        _, line = bootstrap_conventions(
            app,
            force=args.force,
            from_file=getattr(args, "from_file", None),
            prompt_import=not getattr(args, "no_prompt", False),
        )
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(line)
    print()
    if "imported" in line:
        print("Validated structure against the WholeLoop template and installed the file.")
        print("Next: skim with **project-conventions** agent if anything is repo-specific.")
    else:
        print("CLI filled name, README excerpt, layout, and detected stack (no AI).")
        print("Next: run the **project-conventions** agent in your IDE and approve.")
    return 0


def cmd_conventions_import(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    try:
        _, line = import_conventions(
            app,
            Path(args.source),
            force=args.force,
        )
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(line)
    print()
    print("Next: skim with **project-conventions** agent if anything is repo-specific.")
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    print(f"wholeloop {__version__} (pipeline v{PIPELINE_VERSION})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wholeloop",
        description="Install WholeLoop v0.2 agent skills into your app repository.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__} (pipeline v{PIPELINE_VERSION})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser(
        "init",
        help="Install skills, WHOLELOOP.md, IDE symlinks (default: current directory)",
    )
    p_init.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to app repository (default: .)",
    )
    p_init.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing .agents/skills and templated files",
    )
    p_init.add_argument(
        "--copy-ide-skills",
        action="store_true",
        help="Copy into .cursor/.claude instead of symlinks (Windows without symlink support)",
    )
    p_init.add_argument(
        "--conventions-from",
        metavar="FILE",
        type=Path,
        help="Use a team WholeLoop project-conventions.md instead of CLI README bootstrap",
    )
    p_init.set_defaults(func=cmd_init)

    p_up = sub.add_parser(
        "update",
        help="Refresh skills and IDE docs (WHOLELOOP.md, rules) from the CLI bundle",
    )
    p_up.add_argument("path", nargs="?", default=".", help="Path to app repository")
    p_up.add_argument(
        "--no-keep-conventions",
        action="store_false",
        dest="keep_conventions",
        help="Reset project-conventions.md from template",
    )
    p_up.set_defaults(keep_conventions=True)
    p_up.add_argument(
        "--copy-ide-skills",
        action="store_true",
        help="Copy IDE skill dirs instead of symlinks",
    )
    p_up.add_argument(
        "--no-refresh-docs",
        action="store_true",
        help="Do not overwrite WHOLELOOP.md, CLAUDE.md, Copilot instructions, Cursor rules",
    )
    p_up.set_defaults(func=cmd_update)

    p_doc = sub.add_parser("doctor", help="Check WholeLoop installation (v0.2 skills + docs)")
    p_doc.add_argument("path", nargs="?", default=".", help="Path to app repository")
    p_doc.set_defaults(func=cmd_doctor)

    p_sk = sub.add_parser(
        "skills",
        help="List skills bundled in this CLI install and the v0.2 pipeline",
    )
    p_sk.set_defaults(func=cmd_skills)

    p_conv = sub.add_parser(
        "conventions",
        help="Project conventions helpers (CLI bootstrap, no AI)",
    )
    conv_sub = p_conv.add_subparsers(dest="conventions_cmd", required=True)
    p_cb = conv_sub.add_parser(
        "bootstrap",
        help="Re-extract basics from README/package files into project-conventions.md",
    )
    p_cb.add_argument("path", nargs="?", default=".", help="Path to app repository")
    p_cb.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite conventions file with fresh CLI bootstrap",
    )
    p_cb.add_argument(
        "--from",
        dest="from_file",
        metavar="FILE",
        type=Path,
        help="Import a team WholeLoop project-conventions.md (validates template sections)",
    )
    p_cb.add_argument(
        "--no-prompt",
        action="store_true",
        help="Do not ask interactively for a team conventions file",
    )
    p_cb.set_defaults(func=cmd_conventions_bootstrap)

    p_ci = conv_sub.add_parser(
        "import",
        help="Install a team project-conventions.md (same validation as bootstrap --from)",
    )
    p_ci.add_argument("source", type=Path, help="Path to the conventions file")
    p_ci.add_argument("path", nargs="?", default=".", help="Path to app repository")
    p_ci.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Replace existing project-conventions.md",
    )
    p_ci.set_defaults(func=cmd_conventions_import)

    sub.add_parser("version", help="Print version").set_defaults(func=cmd_version)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
