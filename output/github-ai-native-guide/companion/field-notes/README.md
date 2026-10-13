# Field Notes — an AI-native Git learning lab

A deliberately small companion to **Git, the AI-Native Way: From Intent to Verified Delivery**.

The project contains two HTML pages, a local checker, an ignore file, and a GitHub Actions workflow. The starting checklist has three items. The learning task adds a fourth: verifying the delivered page and its links.

## Give the local task to your agent

This prompt assumes a tool-enabled agent with filesystem, terminal, and browser access. The agent should identify missing access instead of claiming it completed an unavailable operation.

~~~prompt
Use this field-notes project to teach me Git through one complete
local change. Inspect the project and applicable instructions first.

Prepare a separate experiment copy outside any existing repository.
Preserve unrelated files and reuse the commit identity established
for this task. Ask for missing identity details rather than inventing
them or changing my global configuration.

Confirm Python 3.10 or later is available. Run tools/check_site.py
using the appropriate Python executable. Create a passing baseline
commit on main, then a branch named docs/add-release-check.

Add an item to docs/checklist.html requiring the deployed URL and
its links to be checked. Explain working files, staging, commits,
and branches with small before/after diagrams as you use them.

Run the checker. In a disposable copy, change the checklist link
to a nonexistent file and confirm the expected failure. Restore
the good link and confirm the check passes.

Start a local preview of docs bound to this computer. Open it in
the connected browser, follow the checklist link, and inspect the
new item. Stage only the intended change, inspect the staged diff,
commit it, and verify the exact committed snapshot.

Return the workspace, branch, baseline and final commit IDs, diff,
checks, browser observations, and any remaining edits. Stop temporary
servers and clean up disposable test copies. Keep the finished project.
Keep this phase local; do not create a remote repository or deploy it.
~~~

## What the checker establishes

Python 3.10 or later is required, with no third-party dependencies.

It requires a nonempty title and at least one H1 on each HTML page. It checks
local href/src paths, HTML fragment IDs, and simple folder/index.html targets.
It rejects root-relative paths and paths escaping the docs directory because
this example is intended to work at a GitHub Pages project subpath.

It does not fetch external URLs, execute JavaScript, validate CSS resources,
check HTML conformance, audit accessibility, or verify a deployed service.

## Continue through prompts

The accompanying article provides Prompt 13 for publishing the branch and preparing a PR, Prompt 18 for inspecting automation, Prompt 19 for merging an approved revision, and Prompt 20 for publishing and checking the site. Each prompt establishes the destination and expected evidence before the agent acts.

The supplied Actions workflow checks source files. It does not deploy them.

No GitHub repository, PR, workflow run, or public deployment is included or
claimed by this local example.
