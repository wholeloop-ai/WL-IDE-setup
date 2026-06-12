"""Guided setup wizards for WholeLoop.

Three audiences, one mental model (product repo is the center):

  * PM        — wholeloop product init      (scaffold the system of record)
  * Dev       — wholeloop app init          (install delivery + link to product)
  * Founder   — wholeloop setup             (product + one or more apps at once)

All wizards degrade gracefully: with --yes or in a non-TTY they use flags and
safe defaults instead of asking.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from wholeloop import __version__, config as cfg
from wholeloop import prompts as P
from wholeloop.doctor import run_doctor
from wholeloop.install import install_app, update_skills
from wholeloop.link import link_app_to_product
from wholeloop.product_install import (
    install_product_repo,
    is_product_repo,
    update_product_skills,
)
from wholeloop.version_check import print_upgrade_notice


def _print(lines: list[str]) -> None:
    for line in lines:
        print(f"  {line}")


def _git_init(path: Path) -> bool:
    try:
        r = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode == 0:
            return False  # already a repo
        subprocess.run(["git", "-C", str(path), "init", "-q"], check=False)
        subprocess.run(["git", "-C", str(path), "add", "-A"], check=False)
        subprocess.run(
            ["git", "-C", str(path), "commit", "-q", "-m", "WholeLoop product repo"],
            check=False,
            capture_output=True,
        )
        return True
    except OSError:
        return False


def _slug(name: str) -> str:
    return name.strip().replace(" ", "-").lower() or "product"


def _product_folder(name: str) -> str:
    slug = _slug(name)
    return slug if slug.endswith("-product") else f"{slug}-product"


def choose_product_location(name: str) -> Path:
    """Menu-driven product location. Avoids free-text confusion; confirms custom paths."""
    folder = _product_folder(name)
    cwd = Path.cwd()
    while True:
        choice = P.ask_choice(
            "Where should the product repo live?",
            [
                ("here", f"{folder}/  — here in {cwd}   (recommended)"),
                ("home", f"{folder}/  — in your home: {Path.home() / folder}"),
                ("custom", "another location (I'll ask for a path)"),
            ],
        )
        if choice == "here":
            return cwd / folder
        if choice == "home":
            return Path.home() / folder
        raw = P.normalize_path_input(
            P.ask_text(
                "Full path to the new repo (or an existing folder to create it inside)",
                required=True,
            )
        )
        dest, nested = resolve_product_dest(raw, name)
        if nested:
            P.info(f"That folder exists — I'll create {dest.name}/ inside it.")
        if P.ask_yes_no(f"Create the product repo at  {dest}  ?", default=True):
            return dest


def choose_app_path() -> Path:
    """Menu-driven app repo location. 'here' = current directory."""
    cwd = Path.cwd()
    while True:
        choice = P.ask_choice(
            "Which folder is the app repo?",
            [
                ("here", f"this folder — {cwd}   (recommended)"),
                ("custom", "another path (I'll ask for it)"),
            ],
        )
        if choice == "here":
            return cwd
        raw = P.normalize_path_input(P.ask_text("App repo path", required=True))
        p = Path(raw).expanduser()
        shown = p.resolve() if p.exists() else p
        if P.ask_yes_no(f"Install WholeLoop in  {shown}  ?", default=True):
            return p


def resolve_product_dest(raw: str, name: str) -> tuple[Path, bool]:
    """Interpret a user-supplied product path.

    Returns (dest, nested). If `raw` is an existing **non-empty** directory, we
    treat it as a parent workspace and create `<name>-product` inside it; this
    matches the common expectation of pointing at a workspace folder. A new or
    empty path is used directly as the repo directory.
    """
    p = Path(raw).expanduser()
    if not p.exists():
        return p, False
    if p.is_dir():
        try:
            empty = not any(p.iterdir())
        except OSError:
            empty = False
        if empty:
            return p, False
        return p / _product_folder(name), True
    return p, False


def _share_snippet(product_path: Path) -> None:
    print()
    P.info("Share with your devs so their app repo feeds this product repo:")
    print()
    print(f"      wholeloop link {product_path}")
    print("      # or, once pushed:")
    print("      wholeloop link https://github.com/your-org/your-product")
    print()


# --------------------------------------------------------------------------- #
# product init / update
# --------------------------------------------------------------------------- #

def run_product_init(
    *,
    path: str | None,
    name: str | None,
    force: bool,
    do_git: bool | None,
    interactive: bool,
) -> int:
    if interactive and not P.no_prompt():
        P.banner("product repo (system of record)",
                 "scope · specs · interviews · inbox · delivery history")
        try:
            if name is None:
                name = P.ask_text("Product name (e.g. acme)", default="product")
            if path is None:
                path = str(choose_product_location(name))
            else:
                # path passed in but still interactive: be forgiving about existing dirs
                dest, nested = resolve_product_dest(path, name)
                if nested:
                    P.info(f"That folder exists — creating {dest.name}/ inside it.")
                path = str(dest)
            if do_git is None:
                do_git = P.ask_yes_no("Initialize a git repo here?", default=True)
        except P.PromptAborted:
            print("aborted.", file=sys.stderr)
            return 1
    else:
        if path is None:
            print("error: path required (e.g. wholeloop product init ~/Projects/acme-product)",
                  file=sys.stderr)
            return 1
        do_git = bool(do_git)

    dest = Path(path).expanduser()
    try:
        lines = install_product_repo(dest, force=force, product_name=name)
    except (FileExistsError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    _print(lines)
    if do_git:
        if _git_init(dest.resolve()):
            P.success("git init + first commit")

    cfg.set_product_repo(str(dest.resolve()))

    print()
    P.success(f"Product repo ready at {dest.resolve()}")
    _share_snippet(dest.resolve())
    P.hint("Next in Cursor: fill Context/icp-profiles.md → build-spec")
    return 0


def run_product_update(*, path: str | None, interactive: bool) -> int:
    dest = Path(path or ".").expanduser().resolve()
    try:
        lines = update_product_skills(dest)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    _print(lines)
    print()
    P.success(f"PM skills updated in {dest}")
    P.info("Your product content (Features/, Interviews/, Progress/, …) was not touched.")
    print_upgrade_notice(dest, allow_network=True)
    return 0


# --------------------------------------------------------------------------- #
# app init (with product link)
# --------------------------------------------------------------------------- #

def _run_app_update_then_link(
    app: Path, product: str | None, copy_ide_skills: bool, interactive: bool
) -> int:
    try:
        lines = update_skills(app, keep_conventions=True, copy_ide_skills=copy_ide_skills)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    _print(lines)
    product_ref = _resolve_product_ref(interactive, product)
    if product_ref:
        try:
            _print(link_app_to_product(app, product_ref))
        except FileNotFoundError as e:
            print(f"warn: could not link product repo: {e}", file=sys.stderr)
    else:
        cfg.add_app_repo(str(app))
    print()
    P.success(f"WholeLoop {__version__} refreshed in {app}")
    P.hint("Then: wholeloop doctor")
    return 0


def _resolve_product_ref(interactive: bool, product: str | None) -> str | None:
    if product:
        return product
    known = cfg.get_product_repo()
    if not (interactive and not P.no_prompt()):
        return known  # non-interactive: use config default if any
    options = []
    if known:
        options.append(("known", f"use {known} (from your last setup)"))
    options.append(("path", "enter a product repo path or git URL"))
    options.append(("skip", "skip for now (link later with: wholeloop link)"))
    try:
        choice = P.ask_choice("Link this app to a product repo?", options)
        if choice == "known":
            return known
        if choice == "path":
            return P.ask_text("Product repo path or git URL", required=True)
        return None
    except P.PromptAborted:
        return None


def run_app_init(
    *,
    path: str | None,
    product: str | None,
    force: bool,
    copy_ide_skills: bool,
    conventions_from: str | None,
    interactive: bool,
) -> int:
    if interactive and not P.no_prompt():
        P.banner("app repo (delivery)",
                 "code · agents · gated pipeline · workspace/runs/")
        try:
            if path is None:
                path = str(choose_app_path())
        except P.PromptAborted:
            print("aborted.", file=sys.stderr)
            return 1

    app = Path(path or ".").expanduser().resolve()
    already_installed = (app / ".agents" / "skills").is_dir()

    if already_installed and not force and interactive and not P.no_prompt():
        try:
            action = P.ask_choice(
                f"WholeLoop already exists in {app}. What now?",
                [
                    ("update", "update — refresh skills + docs, keep conventions (recommended)"),
                    ("force", "reinstall — overwrite everything"),
                    ("skip", "skip this repo"),
                ],
            )
        except P.PromptAborted:
            return 1
        if action == "skip":
            P.info(f"Skipped {app}")
            return 0
        if action == "force":
            force = True
        else:
            return _run_app_update_then_link(app, product, copy_ide_skills, interactive)

    product_ref = _resolve_product_ref(interactive, product)

    try:
        lines = install_app(
            app,
            force=force,
            copy_ide_skills=copy_ide_skills,
            conventions_from=Path(conventions_from) if conventions_from else None,
        )
    except (FileExistsError, FileNotFoundError, ValueError, NotADirectoryError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    _print(lines)

    if product_ref:
        try:
            link_lines = link_app_to_product(app, product_ref)
            _print(link_lines)
        except FileNotFoundError as e:
            print(f"warn: could not link product repo: {e}", file=sys.stderr)
    else:
        cfg.add_app_repo(str(app))

    print()
    P.success(f"WholeLoop {__version__} installed in {app}")
    if not product_ref:
        P.hint("Link the product repo so handoff can close the loop:")
        print(f"        wholeloop link <product-path-or-url>   {app}")
    P.hint("Next: run project-conventions agent in IDE → approve")
    P.hint("Then: spec-review with product spec or epic · wholeloop doctor")
    return 0


# --------------------------------------------------------------------------- #
# founder one-shot setup
# --------------------------------------------------------------------------- #

def run_setup(
    *,
    product: str | None,
    new_product: str | None,
    name: str | None,
    apps: list[str] | None,
    interactive: bool,
) -> int:
    apps = list(apps or [])
    product_ref: str | None = product

    # Non-interactive (flags / CI)
    if not interactive or P.no_prompt():
        if new_product:
            rc = run_product_init(
                path=new_product, name=name, force=False, do_git=False, interactive=False
            )
            if rc != 0:
                return rc
            product_ref = str(Path(new_product).expanduser().resolve())
        if not apps:
            print("error: --app required (or run in a terminal for the wizard)",
                  file=sys.stderr)
            return 1
        for a in apps:
            rc = run_app_init(
                path=a, product=product_ref, force=False, copy_ide_skills=False,
                conventions_from=None, interactive=False,
            )
            if rc != 0:
                return rc
        cfg.mark_setup_complete()
        return 0

    # Interactive founder flow
    P.banner("setup", "product repo first, then your app repos — closes the loop")
    try:
        # Step 1 — product
        choice = P.ask_choice(
            "Product repo (the system of record)",
            [
                ("new", "create a new product repo"),
                ("existing", "use an existing product repo"),
                ("skip", "skip — I'll set it up later"),
            ],
        )
        if choice == "new":
            pname = name or P.ask_text("Product name (e.g. acme)", default="product")
            dest = choose_product_location(pname)
            rc = run_product_init(
                path=str(dest), name=pname, force=False, do_git=True, interactive=False
            )
            if rc != 0:
                return rc
            product_ref = str(dest.expanduser().resolve())
        elif choice == "existing":
            ppath = P.ask_path("Path to your product repo", must_exist=True)
            if not is_product_repo(ppath):
                P.info("Note: that folder doesn't look like a product repo (no Features/). Continuing anyway.")
            product_ref = str(ppath.resolve())
            cfg.set_product_repo(product_ref)

        # Step 2 — apps
        while True:
            if not P.ask_yes_no("Install WholeLoop in an app repo now?", default=True):
                break
            apath = choose_app_path()
            # interactive=True so an existing install offers update/reinstall/skip;
            # path is already chosen, so run_app_init won't re-prompt for it.
            rc = run_app_init(
                path=str(apath), product=product_ref, force=False,
                copy_ide_skills=False, conventions_from=None, interactive=True,
            )
            if rc != 0:
                return rc
            apps.append(str(apath.resolve()))
            if not P.ask_yes_no("Set up another app repo?", default=False):
                break
    except P.PromptAborted:
        print("aborted.", file=sys.stderr)
        return 1

    cfg.mark_setup_complete()

    # Summary
    print()
    P.success("Setup complete")
    if product_ref:
        P.info(f"product : {product_ref}")
    for a in apps:
        P.info(f"app     : {a}")
    print()
    for a in apps:
        ok, _ = run_doctor(Path(a))
        mark = "\u2713" if ok else "\u2717"
        print(f"  {mark} doctor {a}")
    print()
    P.hint("Product (Cursor): fill Context/ → build-spec")
    P.hint("App (Cursor): project-conventions agent → spec-review")
    P.hint("Anytime: wholeloop --help · wholeloop doctor")
    print_upgrade_notice(Path.cwd(), allow_network=True)
    return 0
