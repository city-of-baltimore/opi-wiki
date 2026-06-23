# Git Guide

{{ page_header() }}

A quick reference for using Git so the team keeps a clear, navigable history.

## What is Git?

Git is a version control system. It tracks every change to your code and lets you revisit any earlier version.

## Install Git

1. On a City workstation, open the Company Portal and install the **Git for Windows** package under `Apps`.

2. Launch a terminal (Git Bash or Windows Terminal) and set your identity:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "youremail@baltimorecity.gov"
   ```

You are now ready to clone and work on repositories.

## Set up your first repository

1. Create a folder for your code on your workstation.

2. In that folder, run `git init` in your IDE or code editor to create the local repository.

3. On GitHub or Azure DevOps, create a repository with the same name as the folder.

4. Add the remote as `origin`:

   ```bash
   git remote add origin git@github.com:<org-name>/<repo-name>.git
   ```

5. Build out your project structure, then push your code (see below).

## Push your code

A commit is a set of file changes — additions, edits, or deletions — packaged around a single idea, such as part of a feature, a bug fix, or a variable update. Each commit is a snapshot of your code at that point in time.

1. Stage your changes. New files stage automatically; for edited files, run `git add <filename>`, or `git add .` to stage every changed file in the current directory and its subdirectories.

2. Commit the staged changes with a clear message (see [Write clear, concise commits](#write-clear-concise-commits)):

   ```bash
   git commit -m "message"
   ```

3. Run `git status` to confirm the commit is ready to push.

4. Push to the remote:

   ```bash
   git push
   ```

Your code and its history are now safely stored on the remote.

## Git etiquette

Good Git habits let solo developers and teams understand each change, add it safely to the history, and hand the code to future developers without confusion.

### Write clear, concise commits

Keep commits small and scoped to a single change. Do not commit a slew of files that change unrelated parts of the program. For features and bug fixes, break commits out by the component being changed — for example, the login page in one commit, the authentication module in another, and the build instructions in a third.

Follow the Conventional Commits specification for messages:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

`type` is `fix` (a bug fix), `feat` (a new feature), or a maintenance type such as `build`, `ci`, `docs`, `refactor`, or `test`. For a breaking change that warrants a new major or minor version, add a `!` after the type and explain the scope of the change in the description.

### Push your commits frequently

Commit often: when you finish a piece of the work, before you leave for the day, or before you hand your computer off for service. Still break commits out by area of function rather than bundling many changes into one.

Push all your commits before you leave for the day so they are not only on your computer, and pull when you come in.

### Never push directly to `main`

Never push directly to `main`, especially on a larger team. Pushing straight to `main` skips code review and merging, which limits the team's ability to audit your code, confirm it is understandable, and keep it ready to hand to someone else if you leave the team. Always work in branches checked out from `main`.

### Follow Conventional Branch naming

Use the Conventional Branch standard instead of vague names like `dev`, `develop`, or your username. The format is `<type>/<description>`, where the type is one of:

- `feat` — a feature change

- `fix` — a bug fix

- `hotfix` — an urgent bug fix

- `release` — release preparation

- `chore` — updates and documentation changes

The description should be short and specific — the feature name, the fix in broad terms, or the semantic version tag for a release. Use only lowercase letters, numbers, and dashes, and do not begin or end the description with a dash.

### Open a pull request

A branch only adds value once it merges into `main`. A pull request gets your work reviewed and merged safely, so the team can confirm the code is understandable and works.

1. Push your branch. The repository site shows a banner offering to open a pull request; click it.

2. Add a title — an expanded version of your branch description, written as a short phrase with spaces and capitalization.

3. Fill in the description using this template:

   ```markdown
   * **Please check if the PR fulfills these requirements**
   - [ ] The commit message follows our guidelines
   - [ ] Tests for the changes have been added (for bug fixes/features)
   - [ ] Docs have been added / updated (for bug fixes / features)

   * **What kind of change does this PR introduce?** (Bug fix, feature, docs update, ...)

   * **What is the current behavior?** (You can also link to an open issue here)

   * **What is the new behavior (if this is a feature change)?**

   * **Does this PR introduce a breaking change?** (What changes might users need to make in their application due to this PR?)

   * **Other information**:
   ```

4. Set the assignee to yourself and the reviewer to a senior team member, then submit.

What to put in each field:

- **Checklist** — Confirm the commit messages follow the conventions above. Tests and docs are not strict requirements yet, but add them where you can; they are best practice.

- **Kind of change** — Feature, bug fix, hotfix, release, or chore, as with branch names.

- **Current behavior** — How the program handles the functionality you are changing today.

- **New behavior** — What is changing, from the overall effect down to the components affected. List the modules and rough changes, not every file.

- **Breaking change** — Note any change to API endpoints, design, or functionality so users can prepare. A breaking change may warrant a release schedule and advance notice to customers.
