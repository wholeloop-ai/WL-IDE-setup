"""WholeLoop command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from wholeloop import __version__
from wholeloop.doctor import run_doctor
from wholeloop.install import install_app, update_skills
from wholeloop.conventions import bootstrap_conventions, import_conventions


def _print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)


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
    print("WholeLoop installed (Cursor, Claude Code, VS Code).")
    print(f"  App:         {app}")
    print("  Next steps:")
    print("    1. Run project-conventions agent in IDE (confirm CLI bootstrap)")
    print("    2. Read WHOLELOOP.md in this repo")
    print("    3. wholeloop doctor")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    try:
        lines = update_skills(
            app,
            keep_conventions=args.keep_conventions,
            copy_ide_skills=args.copy_ide_skills,
        )
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    _print_lines(lines)
    print()
    print(f"Skills updated in {app}")
    print("  If conventions changed: wholeloop conventions bootstrap")
    print("  Then: project-conventions agent in IDE → approve")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    ok, lines = run_doctor(app)
    print("\n".join(lines))
    return 0 if ok else 1


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
    print(f"wholeloop {__version__}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wholeloop",
        description="Install WholeLoop agent skills into your app repository.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
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

    p_up = sub.add_parser("update", help="Refresh skills from the installed CLI bundle")
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
    p_up.set_defaults(func=cmd_update)

    p_doc = sub.add_parser("doctor", help="Check WholeLoop installation")
    p_doc.add_argument("path", nargs="?", default=".", help="Path to app repository")
    p_doc.set_defaults(func=cmd_doctor)

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
