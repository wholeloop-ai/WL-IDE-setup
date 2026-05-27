# VS Code / other IDEs

WholeLoop **skills** are plain Markdown with YAML frontmatter. Any IDE that supports:

- **Custom instructions** or **rules files**, or  
- **Copilot / Chat** with workspace context  

…can follow the same prompts by referencing `agents/skills/<agent>/SKILL.md` in the chat or as a snippet.

There is no first-party VS Code extension in this template. Recommended approach:

1. Store skills under `.agents/skills/` in the repo.
2. Add a short **`.vscode/extensions.json`** recommendation list for your stack (optional).
3. Document in team wiki: “For ticket X, paste the contents of `planner/SKILL.md` and attach `context.json`.”

For automation parity with Cursor, prefer the **Python orchestrator** path.
