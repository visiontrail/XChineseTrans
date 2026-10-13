# Figure order and ALT text

## 1. images/01-cover.png

Conceptual cover showing a task brief reaching an AI agent, branching version history, review, and a delivered website.

## 2. images/02-intent-loop.png

A loop connecting user intent, agent inspection, scoped execution, observed evidence, and the next decision.

Caption: The prompt defines the desired result. The agent operates the tools and returns evidence that can support the next decision.

## 3. images/03-state-map.png

A Git state map connecting working files, staging, local history, a remote branch, pull request review, and a live site.

Caption: An arrow represents one kind of change. A successful earlier arrow does not establish that a later one happened.

## 4. images/04-setup.png

Four setup paths distinguish toolchain checks, commit identity, GitHub authentication, and local repository initialization.

Caption: Version checks inspect tooling. Git configuration supplies metadata and defaults. Authentication establishes access to a remote service. Initialization creates local repository metadata.

## 5. images/05-inspection.png

Inspection tools are mapped to the questions they answer: status, differences, history, line provenance, and revision identity.

Caption: These tools inspect different evidence. None is a universal answer to “what changed?”

## 6. images/06-branches.png

A branch diverges from a shared base while an optional worktree provides a separate checkout and index for the agent.

Caption: A branch names a line of history. A worktree gives that line a separate set of working files.

## 7. images/07-staging.png

Three snapshots show HEAD at version A, the index at version B, and working files at version C; commit records B and leaves C unstaged.

Caption: The staged diff describes the proposed commit. A later working-file edit can remain outside it.

## 8. images/08-validation.png

Validation separates a valid local check, a deliberate broken-link failure, restoration, and observation in the local browser.

Caption: The checker, the browser, and the public host answer different questions. The agent should identify which one supplied each result.

## 9. images/09-remotes.png

Remote topology distinguishes an upstream repository, a GitHub fork, the local checkout, and the PR destination, with clone, fetch, and push directions.

Caption: Remote names are local labels for destinations. In a fork workflow, origin commonly points to your fork and upstream to the original project.

## 10. images/10-integration.png

Two history diagrams compare a merge joining existing histories with a rebase replaying a change as a new commit identity.

Caption: Merge connects histories. Rebase replays work onto another base and changes the identities of replayed commits.

## 11. images/11-delivery.png

Delivery proceeds from a pushed branch to PR review, merge, deployment, and a browser check, with separate evidence for each stage.

Caption: A pushed branch, merged PR, successful deployment job, and working public page are four separate observations.

## 12. images/12-recovery.png

Recovery diagrams distinguish unstaging, stashing and applying, appending a revert commit, and destructive working-file replacement.

Caption: Recovery operations have different destinations. Preserving an edit, reversing a commit, and replacing a file are different goals.
