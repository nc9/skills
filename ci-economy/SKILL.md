---
name: ci-economy
description: Make a repo's CI fast and cheap, especially monorepos where coding agents open hundreds of PRs a day. Gives an audit procedure, a diff-scoped merge-queue pipeline with step budgets, an emergency lane, a test pruning procedure, a nightly lane and a rollout order. Use on "slow CI", "CI minutes", "CI cost", "merge queue", "test pruning", "speed up pipeline", "affected tests", "monorepo CI", "diff-scoped CI", or when a pipeline takes more than 10 minutes.
---

Product-neutral. Apply it to any repo, most of all a monorepo with many agent-authored PRs. These are rules, not suggestions; deviate only when the user says so.

The goal: a normal pipeline run takes 10 minutes or less, and a one-app change goes from merge to deployed in about 5 minutes. A test step of 9 to 22 minutes is a bug to fix, not a cost to accept.

## Principles

1. **No CI on PRs.** A PR's gate is the authoring agent's own verified local checks on its scope, plus review. The full pipeline runs only on the merge queue.
2. **Stacks, not single PRs.** Ready PRs are stacked and one pipeline covers the whole stack. One run, many PRs.
3. **Run only what the diff can affect.** Scope every run to the stack's combined git diff, through the workspace dependency graph.
4. **Every step has a time budget.** A step over budget is a defect with an owner.
5. **One sandbox per run.** Not one per job. Each sandbox pays boot, checkout and install again.
6. **Slow and broad suites run nightly,** outside the merge path.
7. **Measure before and after.** Report CI minutes per run, and per merged PR, for every change you make.
8. **Fast inline CI first, deploy automation second.**

## Audit

Measure first. Do not change the pipeline until you have these numbers.

1. **Per-step wall time, last 50 runs.** Use your CI runner's API or log export. Record median and p95 per step: checkout, install, classify, typecheck, lint, test, build, deploy, queue wait.
2. **What a one-app change runs.** Take three recent PRs that touched one app only. List every step that ran. Each step that is not about that app, or its dependents, is waste.
3. **Cache hit rates.** Install cache, build cache, typecheck cache (`.tsbuildinfo` or equivalent). A miss rate over 20 percent on install is a bug.
4. **Test files by duration.** Parse the test runner's per-file timing from logs, or run it with a JSON or JUnit reporter. Sort descending. The top 10 files are usually over half of test time.
5. **Failure history.** For each slow suite, count failures that caught a real bug in the last 90 days. Use revert commits, fix-forward commits and run conclusions.
6. **Cost per merged PR.** Total billed minutes divided by merged PRs over the same window. Count reruns and cancelled runs as cost.
7. **Waste events.** Runs cancelled by a newer push, runs that died on budget, reruns of the same sha, deploys cancelled by a concurrency group.

Useful git commands:

```bash
# files changed by the stack
git diff --name-only <base>...<head>
# churn per top-level dir over 90 days: where does CI need to be sharp
git log --since=90.days --name-only --pretty=format: | cut -d/ -f1-2 | sort | uniq -c | sort -rn | head -20
# reverts as a proxy for escaped bugs
git log --since=90.days --oneline --grep='^Revert'
```

Write the audit as a table: step, median, p95, budget, owner. Everything over budget goes on the fix list.

## The target pipeline

Triggered only by the merge queue. One sandbox, these stages in order:

| Stage | Budget | Notes |
|---|---|---|
| classify | 15 s | Runs inside the first job. No separate sandbox. |
| install | 60 s | Warm snapshot or cache. Frozen lockfile. Scoped to affected workspaces if the package manager supports it. |
| typecheck | 2 min | Scoped to affected projects. Incremental, with a cached `.tsbuildinfo`. |
| lint and format check | 1 min | Changed files only. |
| tests | 3 min | Affected test files only. |
| deploy | 2 min | Affected apps only, after everything above is green. |

Total for a normal run: 10 minutes or less. Single-app change, merge to deployed: about 5 minutes.

### Merge queue

- Ready PRs enter a queue. The queue builds a stack of them and runs one pipeline on the combined result.
- Green stack: merge all, then deploy the affected apps.
- Red stack: bisect. Re-run on halves of the stack, find the culprit, drop it from the queue, and merge the rest. Notify the culprit's author with the failure digest.
- Only a green stack deploys. Never deploy from an unqueued push.

### The classify step

Input: the stack's combined diff. Output: an affected set and a job matrix.

```
changed = git diff --name-only <base>...<stack-head>

# 1. map files to workspaces
owners = { workspace_of(file) for file in changed }

# 2. widen by the dependency graph
affected = owners ∪ reverse_dependents(owners)      # transitive

# 3. widen on global inputs (explicit rules, checked first)
if any(file in GLOBAL for file in changed):         # root config, lockfile, CI files, toolchain version
    affected = all_workspaces          # or a documented subset per file

# 4. derive the matrix
typecheck_targets = affected
test_files        = tests under affected, narrowed by import graph if available
deploy_targets    = affected ∩ deployable_apps
emit matrix
```

Rules for the classifier:

- **Reverse dependents are mandatory.** A change to a shared package runs the typecheck and tests of every app that imports it. Build the graph from the workspace manifests, not from folder names.
- **Global inputs need an explicit widening rule.** A lockfile change widens to the workspaces whose resolved dependencies changed, or to everything if you cannot compute that. Root tsconfig, lint config, toolchain version and CI definition changes widen to everything. Write these rules down in one file.
- **Unknown file means everything.** If a changed file maps to no workspace and matches no ignore rule, widen. Docs-only and asset-only paths go on an explicit skip list.
- **An admin-only change never runs the dashboard or CLI tests.** Test this: keep a table of example diffs and the expected matrix, and run it in the classifier's own unit tests.
- **Fail open.** If the classifier errors, run the full set and file an issue. Never skip silently.
- **Print the decision.** Log the affected set and the reason each workspace is in it.

### Deploy jobs and concurrency

Deploy jobs never share a `cancel-in-progress` concurrency group with CI. Back-to-back merges would each cancel the previous run, so the earlier deploys never execute and services stay on stale code. Use `cancel-in-progress` only for side-effect-free jobs. Give deploys their own group, queued, not cancelled.

## Emergency lane

For a small fix to one app that must ship now:

1. typecheck that app and its direct dependencies;
2. run that app's tests;
3. deploy that app.

No unrelated suites, no other apps, no nightly checks. The lane is a mode of the same pipeline (an app name as input that forces the affected set), not a second pipeline to maintain. Require a named human or merge agent to trigger it, and log every use. Target: under 5 minutes.

## Pruning procedure

Run this once, then every quarter.

1. **Rank.** From the audit, list test files by wall time. Add total time per suite and failure catches in the last 90 days.
2. **Delete tests that restate the implementation.** A test that mocks every collaborator and asserts the call sequence, or recomputes the expected value with the same formula, catches nothing. Delete it.
3. **Remove duplicated coverage.** If a unit test and an integration test exercise the same behaviour, keep the integration test.
4. **Drop slow suites with no recent failures.** Over 60 seconds and zero real catches in 90 days: move to nightly, or delete if the behaviour is covered elsewhere.
5. **Prefer a few integration tests per behaviour.** One test through the real boundary (HTTP handler, real database, real parser) per user-visible behaviour beats ten isolated unit tests.
6. **Fix the slow ones that stay.** Shared setup instead of per-test setup, no sleeps, no network, one database per worker instead of per test.
7. **Report.** Show CI minutes per run, test step median, and number of test files, before and after. A prune that does not move these numbers did nothing.

Do not delete a test just because it is slow if it has caught a real bug. Move it, do not drop it.

## Nightly

Long suites run on a schedule, concurrently, and outside the merge path: golden-output suites, end-to-end browsers, corpus and fuzz runs, full-repo typecheck and lint, dependency audits.

- Shard across runners. Wall time should stay under an hour.
- Each failure files an issue with the failing test, the sha range since last green and a log excerpt. Dedupe by test name.
- A red nightly does not block merges. It creates work, with an owner.
- Track nightly flake rate. A test that flakes twice in a week gets quarantined or fixed.

## Rollout order

1. Run the audit. Write the baseline table.
2. Build the classifier and its example-diff tests. Run it in report-only mode beside the current CI for a week and compare the affected sets with what actually broke.
3. Move checks to the merge queue and turn off PR-triggered pipelines. Authors run local scoped checks and get review.
4. Cut the pipeline to the step budgets. Fix the slowest step first.
5. Prune tests, move slow suites to nightly.
6. Add the emergency lane.
7. Measure for two weeks against the baseline.
8. Only then turn on continuous delivery for any app, one app at a time, starting with the lowest risk.

Do not enable continuous delivery on a pipeline that is slow or flaky. A fast deploy of a bad build is worse than a slow one.

## Money hygiene

- **Push once per review round,** after local gates pass. Intermediate pushes that need no pipeline say so in the commit message if your runner honours skip markers, or stay local.
- **Open PRs as drafts.** Mark ready once, at the final sha.
- **Never rerun a run that died on budget or was cancelled.** Let exactly one run happen at the final sha.
- **Merge test-only deltas without a fresh review pass.**
- **Cancel superseded runs** for side-effect-free jobs only (see the deploy rule above).

## Test memory

Test runners that boot a database in-process, one per test file, use roughly 700 to 850 MB each. Many at once will exhaust a laptop or a small runner.

- Run tests with explicit file paths, about 5 files per invocation, sequentially.
- Never run a bare suite or a whole directory locally. A sharded full suite is still the full suite.
- Kill any test process that runs over 2 minutes, then narrow the paths.
- In CI, size the worker count to memory, not to cores.

## Checklist

- [ ] Baseline table exists: per-step median and p95, minutes per run, cost per merged PR
- [ ] PRs trigger no pipeline; the authoring agent's scoped local checks and review gate them
- [ ] Merge queue stacks PRs, runs one pipeline per stack, bisects on red
- [ ] Classifier uses the workspace graph, includes reverse dependents, has explicit global-input rules, fails open
- [ ] Classifier has example-diff tests (an app-only change excludes unrelated apps)
- [ ] Classify takes 15 s or less, install 60 s, typecheck 2 min, tests 3 min, deploy 2 min
- [ ] One sandbox per run
- [ ] Typecheck is incremental with a cached build-info file
- [ ] Normal run is 10 minutes or less; one-app merge to deploy is about 5
- [ ] Emergency lane exists and is logged
- [ ] Deploy jobs have their own concurrency group with no cancel-in-progress
- [ ] Slow suites moved to nightly; nightly files issues
- [ ] Low-value tests pruned; before and after minutes reported
- [ ] Continuous delivery enabled only after all of the above
