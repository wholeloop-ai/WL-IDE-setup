"""WholeLoop command-line interface.

Command shape is noun-verb (product / app), with init, init-product and update
kept as backward-compatible aliases.

  wholeloop setup                 guided: product repo + app repo(s)
  wholeloop product init|update   PM — system of record
  wholeloop app init|update       Dev — delivery pipeline (+ product link)
  wholeloop link <product>        connect an existing app to its product repo
  wholeloop doctor                verify an app repo (incl. product link)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from wholeloop import __version__
from wholeloop.assets import skills_src
from wholeloop.conventions import (
    bootstrap_conventions,
    import_conventions,
    product_link_status,
)
from wholeloop.doctor import run_doctor
from wholeloop.install import update_skills
from wholeloop.link import link_app_to_product
from wholeloop.pipeline import (
    OPTIONAL_SKILL_DIRS,
    PIPELINE_LINE,
    PIPELINE_VERSION,
    REMOVED_SKILL_DIRS,
    REQUIRED_SKILL_DIRS,
    list_installed_skills,
)
from wholeloop.setup import (
    run_app_init,
    run_product_init,
    run_product_update,
    run_setup,
)
from wholeloop.version_check import print_upgrade_notice


def _print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)


# --------------------------------------------------------------------------- #
# command handlers
# --------------------------------------------------------------------------- #

def cmd_app_init(args: argparse.Namespace) -> int:
    return run_app_init(
        path=args.path,
        product=args.product,
        force=args.force,
        copy_ide_skills=args.copy_ide_skills,
        conventions_from=args.conventions_from,
        interactive=not args.yes,
    )


def cmd_app_update(args: argparse.Namespace) -> int:
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
        print("  Docs unchanged (--no-refresh-docs). Refresh WHOLELOOP.md manually if needed.")
    linked, val = product_link_status(app)
    if linked:
        print(f"  Product link: {val}")
    else:
        print("  Product link: not set — run: wholeloop link <product-path-or-url>")
    print("  Then: wholeloop doctor")
    print_upgrade_notice(app, allow_network=True)
    return 0


def cmd_product_init(args: argparse.Namespace) -> int:
    return run_product_init(
        path=args.path,
        name=args.name,
        force=args.force,
        do_git=args.git,
        interactive=not args.yes,
    )


def cmd_product_update(args: argparse.Namespace) -> int:
    return run_product_update(path=args.path, interactive=not args.yes)


def cmd_setup(args: argparse.Namespace) -> int:
    return run_setup(
        product=args.product,
        new_product=args.new_product,
        name=args.name,
        apps=args.app,
        interactive=not args.yes,
    )


def cmd_link(args: argparse.Namespace) -> int:
    app = Path(args.app or ".").resolve()
    try:
        lines = link_app_to_product(app, args.product)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    _print_lines(lines)
    print()
    linked, val = product_link_status(app)
    if linked:
        print(f"Linked {app}\n  → product repo: {val}")
    print("  Verify: wholeloop doctor")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    app = Path(args.path or ".").resolve()
    ok, lines = run_doctor(app)
    print("\n".join(lines))
    print_upgrade_notice(app, allow_network=True)
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
    print_upgrade_notice(Path.cwd(), allow_network=True)
    return 0


def print_welcome() -> None:
    print(f"wholeloop {__version__} — agentic delivery around a product repo")
    print()
    print("First time? One guided flow for everything:")
    print("  wholeloop setup              product repo + app repo(s)")
    print()
    print("By role:")
    print("  wholeloop product init       PM  — scaffold the product repo (truth)")
    print("  wholeloop app init           Dev — install delivery + link to product")
    print("  wholeloop link <product>     Dev — connect an existing app to product")
    print()
    print("Maintain:")
    print("  wholeloop app update         refresh delivery skills + IDE docs")
    print("  wholeloop product update     refresh PM skills (keeps your content)")
    print("  wholeloop doctor             verify an app repo (incl. product link)")
    print()
    print("  wholeloop <command> --help   ·   wholeloop skills   ·   wholeloop version")
    print_upgrade_notice(Path.cwd(), allow_network=False)


# --------------------------------------------------------------------------- #
# argument wiring
# --------------------------------------------------------------------------- #

def _add_app_init_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("path", nargs="?", default=None, help="App repo path (default: cwd)")
    p.add_argument(
        "--product",
        metavar="REF",
        help="Product repo path or git URL to link (closes the loop)",
    )
    p.add_argument("--force", "-f", action="store_true", help="Overwrite existing install")
    p.add_argument(
        "--copy-ide-skills",
        action="store_true",
        help="Copy into .cursor/.claude instead of symlinks (Windows)",
    )
    p.add_argument(
        "--conventions-from",
        metavar="FILE",
        help="Team project-conventions.md instead of CLI bootstrap",
    )
    p.add_argument("--yes", "-y", action="store_true", help="No prompts; use defaults")
    p.set_defaults(func=cmd_app_init)


def _add_app_update_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("path", nargs="?", default=".", help="App repo path")
    p.add_argument(
        "--no-keep-conventions",
        action="store_false",
        dest="keep_conventions",
        help="Reset project-conventions.md from template",
    )
    p.add_argument(
        "--copy-ide-skills",
        action="store_true",
        help="Copy IDE skill dirs instead of symlinks",
    )
    p.add_argument(
        "--no-refresh-docs",
        action="store_true",
        help="Skills only; leave WHOLELOOP.md and IDE instructions",
    )
    p.set_defaults(keep_conventions=True, func=cmd_app_update)


def _add_product_init_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("path", nargs="?", default=None, help="Target dir for the product repo")
    p.add_argument("--name", metavar="NAME", help="Product name (README + path hint)")
    p.add_argument("--force", "-f", action="store_true", help="Replace non-empty dir (destructive)")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--git", dest="git", action="store_true", default=None, help="git init + first commit")
    g.add_argument("--no-git", dest="git", action="store_false", help="Do not init git")
    p.add_argument("--yes", "-y", action="store_true", help="No prompts; use defaults")
    p.set_defaults(func=cmd_product_init)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wholeloop",
        description="WholeLoop — product repo (truth) + app repos (delivery). v0.3.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__} (pipeline v{PIPELINE_VERSION})",
    )
    sub = parser.add_subparsers(dest="command")

    # setup (founder one-shot)
    p_setup = sub.add_parser("setup", help="Guided setup: product repo + app repo(s)")
    p_setup.add_argument("--product", metavar="PATH", help="Use an existing product repo")
    p_setup.add_argument("--new-product", metavar="PATH", help="Create a new product repo here")
    p_setup.add_argument("--name", metavar="NAME", help="Product name (with --new-product)")
    p_setup.add_argument("--app", metavar="PATH", action="append", help="App repo to install (repeatable)")
    p_setup.add_argument("--yes", "-y", action="store_true", help="No prompts; use flags")
    p_setup.set_defaults(func=cmd_setup)

    # product <init|update>
    p_product = sub.add_parser("product", help="Product repo (PM — system of record)")
    prod_sub = p_product.add_subparsers(dest="product_cmd", required=True)
    _add_product_init_args(
        prod_sub.add_parser("init", help="Scaffold a new product repo")
    )
    p_pu = prod_sub.add_parser("update", help="Refresh PM skills (keeps your content)")
    p_pu.add_argument("path", nargs="?", default=".", help="Product repo path")
    p_pu.add_argument("--yes", "-y", action="store_true")
    p_pu.set_defaults(func=cmd_product_update)

    # app <init|update|doctor>
    p_app = sub.add_parser("app", help="App repo (Dev — delivery pipeline)")
    app_sub = p_app.add_subparsers(dest="app_cmd", required=True)
    _add_app_init_args(app_sub.add_parser("init", help="Install skills + link to product"))
    _add_app_update_args(app_sub.add_parser("update", help="Refresh skills and IDE docs"))
    p_ad = app_sub.add_parser("doctor", help="Check this app repo")
    p_ad.add_argument("path", nargs="?", default=".", help="App repo path")
    p_ad.set_defaults(func=cmd_doctor)

    # link
    p_link = sub.add_parser("link", help="Connect an app repo to its product repo")
    p_link.add_argument("product", help="Product repo path or git URL")
    p_link.add_argument("app", nargs="?", default=".", help="App repo (default: cwd)")
    p_link.set_defaults(func=cmd_link)

    # doctor (top-level alias of app doctor)
    p_doc = sub.add_parser("doctor", help="Check WholeLoop installation in an app repo")
    p_doc.add_argument("path", nargs="?", default=".", help="App repo path")
    p_doc.set_defaults(func=cmd_doctor)

    # skills
    sub.add_parser("skills", help="List bundled skills and the v0.2 pipeline").set_defaults(
        func=cmd_skills
    )

    # conventions
    p_conv = sub.add_parser("conventions", help="Project conventions helpers (no AI)")
    conv_sub = p_conv.add_subparsers(dest="conventions_cmd", required=True)
    p_cb = conv_sub.add_parser("bootstrap", help="Re-extract basics into project-conventions.md")
    p_cb.add_argument("path", nargs="?", default=".", help="App repo path")
    p_cb.add_argument("--force", "-f", action="store_true", help="Overwrite with fresh bootstrap")
    p_cb.add_argument(
        "--from", dest="from_file", metavar="FILE", type=Path,
        help="Import a team project-conventions.md",
    )
    p_cb.add_argument("--no-prompt", action="store_true", help="Do not ask for a team file")
    p_cb.set_defaults(func=cmd_conventions_bootstrap)
    p_ci = conv_sub.add_parser("import", help="Install a team project-conventions.md")
    p_ci.add_argument("source", type=Path, help="Path to the conventions file")
    p_ci.add_argument("path", nargs="?", default=".", help="App repo path")
    p_ci.add_argument("--force", "-f", action="store_true", help="Replace existing file")
    p_ci.set_defaults(func=cmd_conventions_import)

    # version
    sub.add_parser("version", help="Print version").set_defaults(func=cmd_version)

    # backward-compatible aliases
    _add_app_init_args(sub.add_parser("init", help="Alias of: app init"))
    _add_app_update_args(sub.add_parser("update", help="Alias of: app update"))
    _add_product_init_args(sub.add_parser("init-product", help="Alias of: product init"))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "func", None) is None:
        print_welcome()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
