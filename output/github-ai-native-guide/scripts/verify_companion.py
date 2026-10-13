"""Exercise the tutorial in a disposable, local-only Git sandbox."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
records = []
env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
           GIT_TERMINAL_PROMPT="0")

with tempfile.TemporaryDirectory(prefix="github-field-guide-qa-") as scratch:
    lab = Path(scratch) / "field-notes"
    shutil.copytree(ROOT / "companion/field-notes", lab)

    def run(*args, expected=0):
        result = subprocess.run(args, cwd=lab, env=env, text=True, capture_output=True)
        records.append({"command": " ".join(args).replace(scratch, "<TEMP>"),
                        "returncode": result.returncode,
                        "stdout": result.stdout.replace(scratch, "<TEMP>").strip(),
                        "stderr": result.stderr.replace(scratch, "<TEMP>").strip()})
        assert result.returncode == expected, records[-1]
        return result.stdout.strip()

    run(sys.executable, "tools/check_site.py")
    run("git", "init", "-b", "main")
    run("git", "config", "user.name", "Field Guide QA")
    run("git", "config", "user.email", "qa@example.invalid")
    run("git", "config", "commit.gpgsign", "false")
    run("git", "config", "core.hooksPath", str(Path(scratch) / "empty-hooks"))
    run("git", "add", "README.md", ".gitignore", "docs/index.html", "docs/checklist.html",
        "tools/check_site.py", ".github/workflows/check.yml")
    run("git", "diff", "--staged", "--stat")
    run("git", "commit", "-m", "Add field notes site and local link check")
    initial = run("git", "rev-parse", "HEAD")
    run("git", "switch", "-c", "docs/add-release-check")
    checklist = lab / "docs/checklist.html"
    before = checklist.read_text()
    after = before.replace("</ol>", "<li>Open the deployed URL and check its links.</li>\n</ol>")
    assert after != before
    checklist.write_text(after)
    run(sys.executable, "tools/check_site.py")
    run("git", "add", "docs/checklist.html")
    run("git", "restore", "--staged", "docs/checklist.html")
    assert checklist.read_text() == after
    assert run("git", "diff", "--staged", "--name-only") == ""
    assert run("git", "diff", "--name-only") == "docs/checklist.html"
    run("git", "add", "docs/checklist.html")
    run("git", "commit", "-m", "Add a live-site check to the release checklist")
    feature = run("git", "rev-parse", "HEAD")
    assert initial != feature
    assert run("git", "status", "--porcelain") == ""

    index = lab / "docs/index.html"
    good = index.read_text()
    for broken, expected_message in [
        ("does-not-exist.html", "missing target"),
        ("checklist.html#missing-section", "missing fragment ID"),
        ("/checklist.html", "root-relative path"),
    ]:
        index.write_text(good.replace('href="checklist.html"', f'href="{broken}"'))
        failure = run(sys.executable, "tools/check_site.py", expected=1)
        assert expected_message in failure
    index.write_text(good)
    run(sys.executable, "tools/check_site.py")
    assert run("git", "status", "--porcelain") == ""

    remote = Path(scratch) / "remote.git"
    run("git", "init", "--bare", "--initial-branch=main", str(remote))
    run("git", "remote", "add", "origin", str(remote))
    run("git", "switch", "main")
    run("git", "push", "-u", "origin", "main")
    run("git", "switch", "docs/add-release-check")
    run("git", "push", "-u", "origin", "docs/add-release-check")
    assert run("git", "rev-parse", "origin/main") == initial
    assert run("git", "rev-parse", "origin/docs/add-release-check") == feature
    run("git", "revert", "--no-edit", feature)
    assert checklist.read_text() == before
    run(sys.executable, "tools/check_site.py")

report = {"status": "passed", "scope": "Disposable local repository and local bare remote only",
          "not_verified": ["GitHub-hosted Actions execution", "GitHub PR creation or merge",
                           "Public GitHub Pages deployment"], "records": records}
(ROOT / "research/companion-verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(f"PASS: {len(records)} command checks; valid site, three deliberate failures, Git branch/push/revert flow.")
print("All remote operations used a temporary directory on this computer. No GitHub write occurred.")
