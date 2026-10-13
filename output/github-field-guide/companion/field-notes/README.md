# Field Notes

A deliberately small learning project for **GitHub: From First Commit to Verified Delivery**.

Requires Python 3.10 or later; no third-party dependencies.

Run the local check:

~~~bash
python3 tools/check_site.py
~~~

Preview the site:

~~~bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs
~~~

Open http://127.0.0.1:8000/ and follow the checklist link. On Windows, use
`py` or `python` if that is the command for your Python installation.

## Practice change

Create a branch named `docs/add-release-check`. Add this list item to
`docs/checklist.html`:

~~~html
<li>Open the deployed URL and check the page and its links.</li>
~~~

Review the diff, run the checker, and inspect the local site before committing.
To see a meaningful failure, temporarily change the checklist link in
`docs/index.html` to `missing.html`. The checker should exit with code 1.
Restore `checklist.html` and check again.

## What the checker covers

It requires a nonempty title and at least one H1 on each HTML page. It checks
local href/src paths, HTML fragment IDs, and simple folder/index.html targets.
It rejects root-relative paths and paths escaping the docs directory because
this example is intended to work at a GitHub Pages project subpath.

It does not fetch external URLs, execute JavaScript, validate CSS resources,
check HTML conformance, audit accessibility, or verify a deployed service.

## Hosting

The Actions workflow checks the source files. It does not deploy them.
For a public practice repository, configure Pages to publish main /docs.
Then verify the actual URL GitHub provides.

No GitHub repository, PR, workflow run, or public deployment is included or
claimed by this local example.
