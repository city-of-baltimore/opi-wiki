# Git Guide

{{ page_header() }}

A guide to using Git, with best practices and procedures to ensure an
easy-to-understand and navigable Git history.

## Introduction

### What is Git?

Git is a version control system (VCS) that is popularly used in many
development teams in tracking changes done to code in a decentralized manner.
With Git, one can build an entire history of their application/code from start
and easily refer to those prior versions for further improvements.

### How does one install Git?

On a City workstation, head to the Company Portal and install the Git for
Windows package available under `Apps.` Once it's installed, launch a terminal
(it can be Git Bash or Windows Terminal) and make sure to execute the following
commands:

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@baltimorecity.gov"
```

This will get your setup basically complete in Git and allow you to start using
it right away to clone and work on new repositories.

### Now it's installed, what do I do?

Make a folder that will contain your code on your workstation. In your
integrated development environment (IDE) or code editor of choice that supports
Git, execute `git init` in that folder to set up your initial repository on
your computer. On GitHub/Azure DevOps, create a repository with the same name as
the folder you just created and copy the command to add the remote repository as
your `origin` (where the changes will live long-term) - this will typically be
in the form of `git remote add origin git@github.com:<org name>/<repo name>.git`
. After executing this, start coding/setting up your project structure. Once the
bones are sufficiently in place, it's time to push your code.

### How do I push my code?

To push your code, you first need to make a commit. A commit is a set of changes
to files, whether that's adding files, editing them, or even deleting them, in
a compact manner that focuses on a specific idea you're tackling - whether
that's a part of a new feature (or a complete feature depending on how many file
changes that requires), a bug fix, or simple updating of variables. By
committing these changes, you're creating a snapshot in time of your code as it
stands. Refer to the diagram below:

Figure 1. The lifecycle of the status of your files. From `Pro Git, Version
2.1.448, 2025-07-25` by Scott Chacon and Ben Straub.

Any positive change to a file (addition or edits) sets the file to be staged -
either automatically as in the case of new files, or to be staged after being
modified in the case of file edits. To stage edited files, execute
`git add <filename>` or if you have multiple files being edited in a single
commit and don't want to individually add each one, `git add .` which will add
all files in the current directory and all its children directories. Once all
the files you want to commit are staged, execute `git commit -m "message"` with
an appropriate message (more on that in a section further below). If you
execute `git status` now, you'll see that all the files you had staged earlier
have seemingly disappeared, with a new message appearing stating that you have 1
commit to push. That commit contains all the changes you just made, staged, and
packed up with a message. From here, you're ready for the final step in Git
tracking - pushing your code to your Git repository. To do this, simply execute
`git push` to have the commit get sent to the remote repository. Once you
complete this step, the code is up there, and its history is safely stored.

### Is that really all there is to tracking my code with Git?

Definitely not. There's a lot of etiquette involved with managing your code with
Git that we're going to cover here to make sure that both solo developers and
development teams are able to easily understand the changes being made and allow
them to be safely added to the history so that the program the code represents
runs without issue and that the code itself can be understood by future
developers who might take on editing the code.

The first thing that's going to be covered is making clear and concise commits.
This is discussed in the section directly below.

## Etiquette

### Make your commits clear and concise

Concise commits are succinct - that is to say, small - and scoped to a specific
change. We should not be committing a slew of files that change a bunch of
operations of the program in varied ways. For new features and bugfixes, we
should break out commits by the component being changed in the code - this would
be like changing the login/out page in one commit, the authentication module
itself in another, and the build/instructions in another again (ideally when the
feature is complete so that the developer has a full understanding of their
changes).

For clear messages attached to the commits, we're going to follow the
Conventional Commits specification to allow for easy understanding of
specifically what the commit changed and its importance. Conventional Commits
requires the following format for each commit message:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Where `type` could be `fix` or `feat`, to represent a bugfix or a new feature,
or a bunch of others related to git repo maintenance, such as `build`, `ci`,
`docs`, `refactor`, or even `test`. To signify a breaking change that would call
for this software to be a new major or minor version, put a `!` after the type
and in the description, explain briefly how big the change is.

Now that we have a format for commit messages, let's talk about commit
frequency.

### Push your commits frequently

You should be committing often. When you get that one piece of the puzzle done,
commit. Leaving for the day? Commit. About to get your computer worked on?
Commit, commit, commit. Of course, still follow the prior section's guidelines -
don't commit a huge number of changes in one commit, but break them out
according to area of function. Once you have that all sorted, push those changes
out. A good rule of thumb is to push all your commits before you leave for the
day (so they're not only on your computer) and pull once you come in (just in
case).

Now the question remains - what about branches? Are we meant to push everything
to `main` and not worry about stepping on the toes of other developers and
making the Git history of the repo a convoluted mess? Of course, the answer is
absolutely not. Let's break down good branching etiquette as well.

### Never push directly to main (if you can help it)

One of the golden rules of Git version control management of code is to never,
ever push anything to `main` directly, especially when working inside a larger
software development team. By sidestepping code review/merging (discussed
further on), you're limiting the ability of your team to audit your code and
make sure it is understandable and easily able to be given to someone else to
work on, lest you be hit by a bus or leave the team (and we all know which is
the worse scenario of the two). So, please, please use branches and only
checkout branches based on `main`. As to what they should be named.

### Follow standard Git naming conventions for branches too

Rather than making short and useless names for branches like `dev`, `develop`,
or `<your username>`, we're going to follow the Conventional Branch standard.
This will be very similar to the conventional commits section from earlier but
be a bit tighter in choices given the scope of a branch is to include multiple
commits scoped toward a single feature (more on this later.) The format is
`<type>/<description>`, where the type is one of the following:

- `feat` (for a feature change)

- `fix` (for a bugfix)

- `hotfix` (for an urgent bugfix)

- `release` (for release preparation)

- `chore` (for updates and documentation changes)

Hopefully, the types are straightforward enough. The next part, which will have
to be closely watched, is the description. The description should be short and
succinct in describing the specific change it is making, as it is a culmination
of changes via commits. Whether that's the name of the feature, the fix (in a
broad sense), or the semantic version tag for a release, the description
provides the developer with a bit more flexibility, but it is still reined in
to something the wider team can understand. It should also only be a combination
of lowercase letters, numbers, and dashes, with dashes not beginning or ending
the description.

OK, so now we have a good idea about how to be responsible Git committers and
branchers, but what about when the branch is feature complete and is ready to go
into `main`? We don't simply execute `git merge main` and let whatever code get
written into `main` without a second look to make sure we're not forgetting
something. We simply...

### Open a pull request

A core component of Git history management, after commits and branches, is the
almighty merge. Without a merge, you'll have branches just... sitting there.
Menacingly. Code of varying qualities rotting on the vine for no good reason but
because they couldn't find a way be included in the great history of `main`.
Since we do eventually want all good code to stand in the line of its repo's
history, we have to merge the code in. But as mentioned before, we can't just
tell Git to merge the code in, oh no big deal, it's fine. We need the changes
to be reviewed by our team so everyone can guarantee they understand the code
and that it'll actually work. So, we open a pull request. This is usually done
on the website of the repo you're working on - you'll see a banner saying that
recent changes were pushed to the branch you were working on and offer the
option to open a pull request. Once you click that button, it'll take you to a
page that asks for a title and description for your pull request.

The title will be a more expansive version of your branch name's description (as
in, it can use spaces and uppercase characters so it should be like a short
phrase.) For the description however, we're going to follow a template from this
blog to talk about its format. While there are a great many ways that one could
write their changes in their pull request, the following is helpful enough to
let a developer know they're doing things the right way and let their teammates
know just what the change will be:

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

(The above uses markdown, which is why there are so many asterisks.)

While at first glance this may seem like a lot for a pull request, let's break
it down to see how it's pretty straightforward and actually a good idea to fill
out. First, we have a small checklist asking three questions - do the commit
messages follow the conventions we discussed earlier? Are there tests that run
to ensure the changes work before merging? If docs need to be updated due to the
changes, are they? Now, while the commit message check is necessary, the test
ones are not requirements just yet. However, they are essential checks to make
sure whether we are following all best practices surrounding software
development, so if you can get some tests in there, all the better.

Next, what kind of change does this PR introduce? As we talked about earlier
with branch names, is it a feature, bugfix, hotfix, release, or chore?

With that, what is the current behavior? How exactly does the program currently
execute the functionality you are changing?

Further, what is the new behavior (for a feature change)? We need to state
exactly what is changing - from the overall change to the program to a broad
statement on the components being changed as well. You don't need to
individually list every file or folder, but the overarching modules/components
and the rough changes should be listed.

Finally, does this PR introduce a breaking change? With all the things you may
be changing, it could warrant setting up a release schedule and notifying our
customers of the impending change, so they have time to prepare. If any API
endpoints change or the design changes or even a new tab/section is added to the
main page that adds new functionality to the program, it's good practice to let
users know early so they can anticipate the change and even offer input if
necessary to help steer the program's development in a way that maintains its
usability.

Once we have all of these questions answered, it's time to submit the request.
Set the assignee to yourself and the reviewer to a senior member of the team and
then the review can begin.
