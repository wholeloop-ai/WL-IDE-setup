"""Bootstrap project-conventions.md from repo files (no AI)."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

BOOTSTRAP_MARKER = "<!-- wholeloop:cli-bootstrap -->"
AGENT_TODO = "<!-- TODO: confirm with project-conventions agent -->"

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


def bootstrap_conventions(app: Path, *, force: bool = False) -> tuple[Path, str]:
    """Write or refresh CLI bootstrap at conventions path. Returns (path, log line)."""
    app = app.resolve()
    dest = app / ".agents" / "skills" / "references" / "project-conventions.md"
    template_path = references_dir() / "PROJECT_CONVENTIONS.template.md"

    if dest.exists() and not force:
        text = _read_text(dest)
        if BOOTSTRAP_MARKER not in text and "{{PROJECT_NAME}}" not in text:
            return dest, "keep  project-conventions.md (already customized)"
        if not force:
            pass  # allow refresh of bootstrap / template placeholders

    if not dest.parent.exists():
        raise FileNotFoundError("Run wholeloop init first — missing .agents/skills/")

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
