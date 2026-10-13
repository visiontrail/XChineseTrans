# Codex: A Practical Guide to Getting Real Work Done

*Leo Guo · LeoGuoLabs*

![Codex: A practical field guide. Define the work. Let it run. Verify the result.](images/01-cover.png)

A useful Codex task ends with something you can inspect: a working page, a fixed bug, a clean dataset, or a document that answers the brief.

My starting point is simple: define the result, give the agent enough room to work, and check the evidence at the end.

You can begin before you understand every command or acronym. Pick a small task whose outcome you can judge. Learn the tools as the work requires them.

This guide covers that first task, the settings worth understanding, and the habits that make larger projects easier to manage.

## 1. Start with a folder and one useful task

For a first session, I would use the desktop app. OpenAI currently documents Codex as a workspace within the ChatGPT desktop app; the terminal CLI and IDE extension are other ways to work with it. Start from the [official desktop guide](https://learn.chatgpt.com/docs/app), install the app, sign in, and choose Codex.

Create a dedicated folder for your experiment. Open that folder as the project. Keeping the inputs and outputs together makes it easier to see what changed.

A good first task is small enough to inspect manually:

> Build a simple reading-list page in this folder. Each entry needs a title, URL, and read/unread status. Save the list locally so it survives a refresh. Use a clean layout that works on a phone. Run it locally and verify adding an item, changing its status, and refreshing the page. Tell me how to open it and what you could not verify.

For an existing codebase, begin with orientation:

> Read the project instructions and README. Explain how the app starts, where its main features live, and which checks are available. Report any existing local changes. Do not edit files yet.

Once you understand the starting point, assign one focused change. Save a Git checkpoint before changing a repository you care about.

## 2. Learn the few controls that affect the work

Before sending the first prompt, check the selected project, execution location, model, and permissions. These determine what Codex can see and what it can do.

In the desktop app, ChatGPT includes Chat and Work modes, while Codex provides a workspace for software tasks. My practical preference is to use Codex when the work revolves around a repository, commands, diffs, and tests. Use the surface that gives the task the right context; complexity alone is a poor way to choose.

The [official quickstart](https://learn.chatgpt.com/docs/app) shows the current entry points. Interface labels can change between releases.

I would also resist choosing a model from an old “best model” screenshot. Check the models actually available in your account. Start with an available default and judge it on a real task: quality of the result, time taken, and how much correction it needs.

You do not need to install every integration or tune every setting before you begin.

## 3. Write a brief Codex can execute

The prompt is where you define the job. Four pieces of information usually matter most:

- **Outcome:** What should be different when the task is finished?
- **Context:** Which files, examples, errors, or references matter?
- **Boundaries:** What may Codex change, and what requires a decision from you?
- **Acceptance:** What evidence will show that the result works?

![Four parts of an executable brief: outcome, context, boundaries, and acceptance; followed by inspect, build, and verify.](images/02-task-brief.png)

For example:

```text
Fix the settings page so the selected language survives a refresh.

First inspect how preferences are stored and how the page restores them.
Keep the existing design and support every language already available.

Make the necessary changes and run the relevant checks.
If browser access is available, change the language, refresh the page,
and reopen settings to verify that the saved choice is still selected.

Do not deploy this change or modify production data.
At handoff, report the cause, the changes, the checks you ran,
and anything you could not verify.
```

That gives the agent a destination and a way to test whether it arrived. It also leaves room to investigate the implementation.

For a larger task, ask Codex to inspect the project and identify the important decisions before editing. For a small, well-defined fix, let it proceed through implementation and verification.

When the same failure appears in several places, ask it to investigate the shared cause. Repeatedly patching individual symptoms is a good way to accumulate fragile code.

## 4. Put lasting instructions in the right place

Some preferences apply across projects: be direct, distinguish facts from assumptions, and explain what remains uncertain. Other instructions belong to one repository: build commands, test commands, architecture constraints, and files that must stay untouched.

Codex supports persistent instructions through `AGENTS.md`. Its default global location is `~/.codex/AGENTS.md`. Project instructions are discovered along the path from the project root to the working directory, with more specific guidance taking precedence. At a given level, `AGENTS.override.md` takes precedence over `AGENTS.md`. See the [instruction discovery rules](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Here is a compact starting point for a project:

```markdown
# Working instructions

- Read the existing code and project documentation before editing.
- Keep changes focused on the requested outcome.
- Preserve unrelated work already present in the checkout.
- Run the relevant checks and name any checks you could not run.
- Fix shared causes when several failures come from the same mechanism.
- Report code changes, test results, deployment, and live verification
  as separate claims.
- Ask before publishing, deploying, or changing production data
  unless the current task already authorizes it.
```

Add the project's actual setup and test commands. In the CLI, `/init` can generate a starting file; read and refine it before relying on it.

Keep these instructions short enough to maintain. A rule that helped on one unusual task may be unnecessary for every future task.

## 5. Choose the workspace, then set its permissions

**Local** works directly in the selected checkout. It is useful when you need the current files, local services, or an existing debugging environment.

**Worktree** creates a separate Git working directory. It is useful for parallel changes or a feature you want to develop without editing the checkout you are using. Worktrees require a Git repository and share repository metadata. They separate working files; they are not security sandboxes. The [worktree guide](https://learn.chatgpt.com/docs/environments/git-worktrees) explains setup and handoff.

**Cloud** runs a task in a remote environment configured for the repository. Prepare its dependencies and required access, then review the returned changes. A cloud task does not automatically inherit services or files from your laptop. See [Codex cloud setup](https://learn.chatgpt.com/docs/cloud).

![Comparison of Local, Worktree, and Cloud, with a reminder that worktrees are not security sandboxes and a distinction between Plan, Goal, and Schedule.](images/04-workspaces.png)

Permissions are a separate decision. The sandbox controls filesystem and network access; the approval policy determines how actions that need review are handled. OpenAI recommends starting with **Ask for approval** for most work. **Approve for me** routes approval requests through automatic review while retaining the same workspace boundary. See the [permissions guide](https://learn.chatgpt.com/docs/permission-modes).

My rule is to grant the access the task needs and keep the boundary understandable. A clear request to fix a local bug can authorize inspection, editing, and relevant tests. Publishing the result or changing a production service deserves an explicit instruction.

If an approval request appears, read the action and its target. Broad access affects your machine and data, so choose it deliberately.

## 6. Add skills and connections when they solve a real problem

The terminology becomes easier when each piece has a job:

- A **model** reasons about the task and generates responses.
- An **agent** uses a model and tools to carry out work across steps.
- A **skill** packages instructions, resources, and optional scripts for a repeatable workflow.
- **MCP**, the Model Context Protocol, connects an agent to tools and data exposed by servers.
- A **plugin** is an installable package that can bundle skills and connections.
- A **CLI** is a command-line interface. An **IDE** is the development environment around your code. A **shell**, such as Bash, zsh, or PowerShell, interprets commands.

![Six tools and their roles: model, agent, skill, MCP, plugin, and CLI.](images/03-toolbox.png)

Suppose you regularly produce technical reports. A skill could hold the report structure, source requirements, and review process. A connection could provide the source documents. A plugin could package those capabilities for installation.

Start by doing the task once. When the workflow proves useful and repeats, turn the stable parts into a skill. OpenAI's [skills guide](https://learn.chatgpt.com/docs/build-skills) explains the format; its [plugin overview](https://learn.chatgpt.com/docs/skills-and-plugins) explains how the pieces fit together.

More installed tools also mean more choices and more access to understand. Add them for a reason you can name.

## 7. Learn a small set of terminal commands

The desktop app is enough to begin. The CLI becomes useful when you prefer a terminal or want to integrate Codex into scripts.

If Node.js and npm are already installed, one official installation method is:

```bash
npm install -g @openai/codex
```

Then open your project and launch Codex:

```bash
cd /path/to/your/project
codex
```

Follow the sign-in flow. Alternative installation methods are in the [official CLI guide](https://learn.chatgpt.com/docs/codex/cli).

These commands cover a useful starting set:

```bash
codex --version
codex --help
codex --cd /path/to/your/project
codex resume --last
codex --worktree
codex --search
codex -i screenshot.png "Investigate this layout problem"
codex exec "Summarize the repository structure without editing files"
```

Inside an interactive session:

| Command | Purpose |
| --- | --- |
| `/status` | Inspect session configuration and usage |
| `/model` | Choose a model and available reasoning settings |
| `/permissions` | Inspect or adjust permissions |
| `/plan` | Plan a change before implementation |
| `/diff` | Inspect the Git diff |
| `/review` | Request a code review |
| `/compact` | Summarize a long conversation |
| `/exit` | Exit the CLI |

Use the [current command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) and your installed `codex --help` when a flag differs. The examples above were checked against local CLI help during preparation; they were not all executed as tasks.

You can learn these gradually. Understanding paths, Git changes, logs, dependencies, and tests will still help you make better decisions about the work Codex produces.

## 8. Use plans, goals, and schedules for different needs

A **plan** helps settle the approach before implementation. For example: inspect the authentication flow, compare two fixes, and identify the behavior that could regress.

A **goal** gives a longer task a persistent finish line. A useful objective might be: “Resolve the failing import workflow and verify it against the provided sample files.” It needs an observable completion condition. A goal is not a guarantee of success; missing access, ambiguous requirements, and external dependencies can still block it. See [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex).

A **scheduled task** runs at a chosen time or cadence. An example is a daily review of test failures that produces a short report with links to the evidence. Test the prompt manually before scheduling it. Tasks that need local files require the computer to stay on and the desktop app to remain running. See the [scheduled tasks guide](https://learn.chatgpt.com/docs/automations).

Choose the mechanism that fits the work. A one-line edit rarely needs a persistent goal or a recurring automation.

## 9. Review the evidence before accepting the handoff

This is the habit I care about most.

Ask for a handoff that tells you what changed, why it changed, how it was checked, and what remains unresolved. Then inspect the result that matters to you.

A useful report might say:

> The saved language preference is now restored when settings opens. The relevant automated checks passed. Browser verification confirmed that the choice survives a refresh and re-entry. The change is local; deployment has not been performed.

Different claims need different evidence:

| Claim | Evidence to look for |
| --- | --- |
| The change was implemented | The relevant diff or output files |
| The checks passed | Commands, results, and any skipped coverage |
| The release was deployed | The target environment and deployed revision |
| The user workflow works | A functional check in that environment |

If browser access was unavailable, the handoff should say so. A build passing does not establish that a page works after refresh. A process starting does not establish that its service is healthy.

For documents and media, apply the same standard: open the file, inspect the layout, check the sources, or play the final output. The artifact has to survive contact with the way it will actually be used.

## Your first useful session

Choose one small task you have been putting off. Put it in a dedicated folder, describe the outcome and boundaries, and specify how you will check it.

Let Codex do the work. Review the result. Keep the instructions that helped.

That is a practical way to build confidence: one completed task, with evidence you understand.

