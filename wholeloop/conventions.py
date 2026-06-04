"""Bootstrap project-conventions.md from repo files (no AI)."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from wholeloop.assets import references_dir

BOOTSTRAP_MARKER = "<!-- wholeloop:cli-bootstrap -->"
IMPORTED_MARKER = "<!-- wholeloop:team-import -->"
AGENT_TODO = "<!-- TODO: confirm with project-conventions agent -->"

REQUIRED_SECTIONS = (
    "## 1. What this product is",
    "## 2. Repository layout",
    "## 3. Stack",
    "## 4. Rules agents must follow",
    "## 5. Issue tracker",
    "## 6. WholeLoop run paths",
    "## 7. Definition of Done",
    "## 8. Links",
)
PLACEHOLDER_MARKERS = ("{{PROJECT_NAME}}", "{{PRODUCT_REPO}}")

README_CANDIDATES = ("README.md", "Readme.md", "readme.md", "README.rst")
DOC_GLOBS = ("docs/**/*.md", "doc/**/*.md")


def repo_display_name(app: Path) -> str:
    name = app.name
    try:
        out = subprocess.run(
            ["git", "-C", str(app), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if out.returncode == 0 and out.stdout.strip():
            url = out.stdout.strip()
            base = url.rstrip("/").split("/")[-1]
            if base.endswith(".git"):
                base = base[:-4]
            if base:
                return base
    except (OSError, subprocess.TimeoutExpired):
        pass
    return name


def _read_text(path: Path, limit: int = 8000) -> str:
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def readme_excerpt(app: Path, max_lines: int = 12) -> str:
    for name in README_CANDIDATES:
        p = app / name
        if p.is_file():
            lines = _read_text(p).splitlines()
            body: list[str] = []
            for line in lines:
                if line.startswith("#") and body:
                    break
                if line.strip() or body:
                    body.append(line)
                if len(body) >= max_lines:
                    break
            if body:
                return "\n".join(body).strip()
    return "_No README found — describe the product with the **project-conventions** agent._"


def top_level_dirs(app: Path) -> list[str]:
    skip = {
        ".git",
        ".agents",
        ".cursor",
        ".claude",
        "node_modules",
        "workspace",
        ".venv",
        "venv",
        "__pycache__",
        "dist",
        "build",
        ".idea",
    }
    dirs: list[str] = []
    for child in sorted(app.iterdir()):
        if child.name.startswith(".") and child.name not in (".github",):
            if child.name in skip:
                continue
        if child.name in skip:
            continue
        if child.is_dir():
            dirs.append(f"{child.name}/")
        elif child.is_file() and child.suffix in (".md", ".toml", ".json", ".yaml", ".yml"):
            dirs.append(child.name)
    return dirs[:25]


def detect_stack(app: Path) -> dict[str, str]:
    stack = {
        "Runtime": AGENT_TODO,
        "Package manager": AGENT_TODO,
        "Tests": AGENT_TODO,
        "Linter / formatter": AGENT_TODO,
    }

    pkg = app / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(_read_text(pkg, 4000))
            stack["Runtime"] = "Node.js"
            if (app / "pnpm-lock.yaml").exists():
                stack["Package manager"] = "pnpm"
            elif (app / "yarn.lock").exists():
                stack["Package manager"] = "yarn"
            elif (app / "package-lock.json").exists():
                stack["Package manager"] = "npm"
            scripts = data.get("scripts") or {}
            if "test" in scripts:
                stack["Tests"] = f"`npm run test` (or {stack['Package manager']} equivalent)"
            if "lint" in scripts:
                stack["Linter / formatter"] = "`npm run lint`"
        except json.JSONDecodeError:
            pass

    pyproject = app / "pyproject.toml"
    if pyproject.is_file():
        text = _read_text(pyproject, 4000)
        stack["Runtime"] = "Python"
        if "uv" in text or (app / "uv.lock").exists():
            stack["Package manager"] = "uv"
        elif (app / "poetry.lock").exists():
            stack["Package manager"] = "poetry"
        else:
            stack["Package manager"] = "pip"
        if "pytest" in text:
            stack["Tests"] = "pytest"
        elif (app / "requirements.txt").exists():
            stack["Tests"] = AGENT_TODO + " (add test command)"
        if "ruff" in text:
            stack["Linter / formatter"] = "ruff"
        elif "black" in text:
            stack["Linter / formatter"] = "black"

    if (app / "requirements.txt").exists() and stack["Runtime"] == AGENT_TODO:
        stack["Runtime"] = "Python"
        stack["Package manager"] = "pip"

    if (app / "go.mod").exists():
        stack["Runtime"] = "Go"
        stack["Package manager"] = "go modules"
        stack["Tests"] = "`go test ./...`"

    if (app / "Cargo.toml").exists():
        stack["Runtime"] = "Rust"
        stack["Package manager"] = "cargo"
        stack["Tests"] = "cargo test"

    return stack


def doc_sources(app: Path) -> list[str]:
    found: list[str] = []
    for pattern in DOC_GLOBS:
        for p in sorted(app.glob(pattern))[:8]:
            if p.is_file() and p.stat().st_size < 100_000:
                found.append(str(p.relative_to(app)))
    return found


def render_conventions(app: Path, template: str) -> str:
    name = repo_display_name(app)
    dirs = top_level_dirs(app)
    stack = detect_stack(app)
    excerpt = readme_excerpt(app)
    docs = doc_sources(app)

    body = template.replace("{{PROJECT_NAME}}", name)
    body = body.replace("{{PRODUCT_REPO}}", name)

    banner = f"""{BOOTSTRAP_MARKER}
> **CLI bootstrap** (no AI). Review every section, then run the **project-conventions** agent
> in your IDE to complete, correct, and confirm with you before relying on other WholeLoop agents.
"""

    if body.startswith("# "):
        first_nl = body.index("\n")
        body = body[:first_nl] + "\n\n" + banner + body[first_nl:]

    # Section 1 — product blurb from README
    sec1 = f"""## 1. What this product is

{excerpt}

- **Out of scope:** {AGENT_TODO}
"""
    body = re.sub(
        r"## 1\. What this product is\n\n[\s\S]*?(?=\n## 2\.)",
        sec1 + "\n",
        body,
        count=1,
    )

    # Section 2 — layout
    tree = "\n".join(f"- `{d}`" for d in dirs) if dirs else f"- {AGENT_TODO}"
    sec2 = f"""## 2. Repository layout

{tree}

- **Product repo (specs):** {AGENT_TODO} e.g. `../product-repo/specs/`
"""
    body = re.sub(
        r"## 2\. Repository layout\n\n[\s\S]*?(?=\n## 3\.)",
        sec2 + "\n",
        body,
        count=1,
    )

    # Section 3 — stack table
    rows = "\n".join(
        f"| {k} | {v} | |" for k, v in stack.items()
    )
    sec3 = f"""## 3. Stack

| Layer | Technology | Version / notes |
|-------|------------|-----------------|
{rows}
"""
    body = re.sub(
        r"## 3\. Stack\n\n[\s\S]*?(?=\n## 4\.)",
        sec3 + "\n",
        body,
        count=1,
    )

    # Section 5 — tracker placeholder
    if "**provider**" in body:
        body = re.sub(
            r"(\| \*\*provider\*\* \| )`linear` \\| `jira` \\| `manual`( \|)",
            r"\1" + AGENT_TODO + r"\2",
            body,
            count=1,
        )

    if docs:
        doc_note = "\n".join(f"- `{d}`" for d in docs)
        appendix = f"""
## CLI-detected docs (for agent review)

{doc_note}

The **project-conventions** agent should read these and ask you to confirm extracted rules.
"""
        if "## 8. Links" in body:
            body = body.replace("## 8. Links", appendix + "\n## 8. Links", 1)
        else:
            body += appendix

    return body


def validate_conventions_content(text: str) -> tuple[bool, list[str]]:
    """Check a file looks like a filled WholeLoop conventions doc (not the raw template)."""
    errors: list[str] = []
    warnings: list[str] = []

    if not text.strip():
        errors.append("file is empty")
        return False, errors

    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            errors.append(f"still contains template placeholder {marker}")

    missing = [h for h in REQUIRED_SECTIONS if h not in text]
    if missing:
        errors.append(
            "missing sections: " + ", ".join(s.replace("## ", "") for s in missing)
        )

    if BOOTSTRAP_MARKER in text:
        warnings.append("CLI bootstrap marker present — run project-conventions agent to confirm")
    if AGENT_TODO in text:
        warnings.append("TODO markers present — confirm with project-conventions agent")

    messages = errors + [f"note: {w}" for w in warnings]
    return len(errors) == 0, messages


def _conventions_dest(app: Path) -> Path:
    return app / ".agents" / "skills" / "references" / "project-conventions.md"


def ensure_conventions_layout(app: Path) -> Path:
    """Require .agents/skills/ and ensure references/ exists (older installs may lack it)."""
    skills = app / ".agents" / "skills"
    if not skills.is_dir():
        raise FileNotFoundError(
            "WholeLoop is not installed in this repo — run: wholeloop init"
        )
    refs = skills / "references"
    refs.mkdir(parents=True, exist_ok=True)
    return refs


def prompt_conventions_source() -> Path | None:
    """Ask interactively for a team WholeLoop conventions file (TTY only)."""
    if not sys.stdin.isatty():
        return None
    try:
        answer = input(
            "Do you have a WholeLoop project-conventions.md from your team? [y/N]: "
        ).strip().lower()
        if answer not in ("y", "yes"):
            return None
        path_str = input("Path to that file: ").strip()
    except (EOFError, KeyboardInterrupt):
        print(file=sys.stderr)
        return None
    if not path_str:
        return None
    return Path(path_str).expanduser()


def import_conventions(
    app: Path,
    source: Path,
    *,
    force: bool = False,
) -> tuple[Path, str]:
    """Validate and install a team conventions file as the repo's first version."""
    app = app.resolve()
    dest = _conventions_dest(app)
    source = source.expanduser().resolve()

    if not source.is_file():
        raise FileNotFoundError(f"Conventions file not found: {source}")

    if dest.exists() and not force:
        existing = _read_text(dest)
        if BOOTSTRAP_MARKER not in existing and "{{PROJECT_NAME}}" not in existing:
            return dest, "keep  project-conventions.md (already customized; use --force to replace)"

    ensure_conventions_layout(app)

    text = _read_text(source, limit=500_000)
    ok, messages = validate_conventions_content(text)
    if not ok:
        detail = "\n  ".join(messages)
        raise ValueError(
            f"{source} does not look like a filled WholeLoop conventions file:\n  {detail}"
        )

    if IMPORTED_MARKER not in text:
        note = f"""{IMPORTED_MARKER}
> **Team import** (CLI). Copied from `{source.name}`. Skim with the **project-conventions** agent
> if anything is repo-specific; approve before heavy pipeline work.

"""
        if text.startswith("# "):
            first_nl = text.index("\n")
            text = text[:first_nl] + "\n\n" + note + text[first_nl:]
        else:
            text = note + text

    dest.write_text(text, encoding="utf-8")
    return dest, f"write .agents/skills/references/project-conventions.md (imported from {source})"


def bootstrap_conventions(
    app: Path,
    *,
    force: bool = False,
    from_file: Path | None = None,
    prompt_import: bool = False,
) -> tuple[Path, str]:
    """Write CLI bootstrap or import a team conventions file. Returns (path, log line)."""
    app = app.resolve()
    dest = _conventions_dest(app)
    ensure_conventions_layout(app)

    source = from_file
    if source is None and prompt_import:
        source = prompt_conventions_source()
    if source is not None:
        return import_conventions(app, source, force=force)

    template_path = references_dir() / "PROJECT_CONVENTIONS.template.md"

    if dest.exists() and not force:
        text = _read_text(dest)
        if BOOTSTRAP_MARKER not in text and "{{PROJECT_NAME}}" not in text:
            return dest, "keep  project-conventions.md (already customized)"

    template = _read_text(template_path)
    if not template:
        raise FileNotFoundError(f"Missing template: {template_path}")

    dest.write_text(render_conventions(app, template), encoding="utf-8")
    return dest, "write .agents/skills/references/project-conventions.md (CLI bootstrap)"


def is_bootstrap_pending(path: Path) -> bool:
    if not path.is_file():
        return True
    text = path.read_text(encoding="utf-8")
    return BOOTSTRAP_MARKER in text or "{{PROJECT_NAME}}" in text or AGENT_TODO in text


PRODUCT_LINK_MARKER = "<!-- wholeloop:product-link -->"


def _is_product_url(ref: str) -> bool:
    return ref.startswith(("http://", "https://", "git@", "ssh://"))


def normalize_product_ref(app: Path, product_ref: str) -> tuple[str, str, str]:
    """Return (config_value, display, spec_inbox) for a product reference.

    config_value: absolute path or URL stored in global config.
    display: what we write into conventions (relative path when local + sibling).
    spec_inbox: where spec-review looks for ARTIFACT-WAL copies.
    """
    if _is_product_url(product_ref):
        return product_ref, product_ref, f"{product_ref} (clone, then re-run wholeloop link <local-path>)"

    resolved = Path(product_ref).expanduser().resolve()
    try:
        rel = os.path.relpath(resolved, app.resolve())
        display = rel if not rel.startswith(os.pardir + os.pardir) else str(resolved)
    except ValueError:
        display = str(resolved)
    return str(resolved), display, f"{display}/inbox/"


def set_product_link(app: Path, product_ref: str) -> tuple[Path, list[str]]:
    """Write the product repo reference into project-conventions.md (§2, §5, §8)."""
    app = app.resolve()
    dest = _conventions_dest(app)
    if not dest.is_file():
        raise FileNotFoundError(
            f"{dest} not found — run: wholeloop init (or wholeloop app init)"
        )

    _, display, spec_inbox = normalize_product_ref(app, product_ref)
    text = dest.read_text(encoding="utf-8")
    changed: list[str] = []

    # §2 — Product repo line
    line2 = (
        f"- **Product repo (specs):** `{display}` — spec inbox: `{spec_inbox}` "
        f"{PRODUCT_LINK_MARKER}"
    )
    new_text, n = re.subn(r"- \*\*Product repo.*", line2, text, count=1)
    if n:
        text = new_text
        changed.append("conventions §2 — product repo path")
    else:
        text = re.sub(
            r"(## 2\. Repository layout\n)",
            r"\1\n" + line2 + "\n",
            text,
            count=1,
        )
        changed.append("conventions §2 — product repo path (inserted)")

    # §5 — Default spec path row
    new_text, n = re.subn(
        r"(\| \*\*Default spec path\*\* \| )`[^`]*`( \|)",
        rf"\1`{spec_inbox}{{spec_id}}.md`\2",
        text,
        count=1,
    )
    if n:
        text = new_text
        changed.append("conventions §5 — default spec path")

    # §8 — Links
    new_text, n = re.subn(
        r"- Product repo URL\.?",
        f"- Product repo: {product_ref}",
        text,
        count=1,
    )
    if n:
        text = new_text
        changed.append("conventions §8 — product repo link")

    dest.write_text(text, encoding="utf-8")
    return dest, changed


def product_link_status(app: Path) -> tuple[bool, str | None]:
    """(linked, display_value) — linked is True once a real path/URL replaced the TODO."""
    dest = _conventions_dest(app)
    if not dest.is_file():
        return False, None
    text = dest.read_text(encoding="utf-8")
    m = re.search(r"- \*\*Product repo \(specs\):\*\* `([^`]+)`", text)
    if m and PRODUCT_LINK_MARKER in text:
        return True, m.group(1)
    return False, None
