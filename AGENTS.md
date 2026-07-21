# AGENTS.md

## Cursor Cloud specific instructions

This repository is the Felix-Pago organization's special `.github` repository for
GitHub "Community Health Files". It is **not an application** — it contains only
Markdown documentation and GitHub issue/PR templates.

Key facts for future agents:

- There is **no source code, no package manifest, no build system, and no runnable
  service**. There is nothing to install, build, run, or serve (no ports, no
  databases, no external dependencies). Environment "setup" is a no-op.
- The only machine-checkable content is the YAML issue forms in
  `.github/ISSUE_TEMPLATE/*.yml`. You can sanity-check them by parsing with a YAML
  loader (e.g. `python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/ISSUE_TEMPLATE/*.yml')]"`).
  GitHub validates these forms against its issue-form schema when rendering them.
- Files placed here act as org-wide defaults for every repo in the org that lacks
  its own equivalent (see `README.md`). The actual Felix-Pago products live in other
  repositories, not here.
