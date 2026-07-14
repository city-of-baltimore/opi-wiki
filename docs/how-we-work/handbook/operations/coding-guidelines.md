# Coding Guidelines

{{ page_header(summary="How we write code at OPI.", category="SERIES · OPI FOUNDATIONS") }}

The team is small but demand is proportionally bigger. We need to create and
maintain software that current and future administrations rely on. Devs will
have to jump between projects to build new features or fix bugs.

Having clear guidelines help devs context switch quickly, get in flow and focus
on building features instead of relearning conventions for different projects.


AUDIENCE
:   All OPI Devs

OWNER
:   Director’s Office

VERSION
:   v0.1 · July 2026

## Formatting
`.editorconfig` file, it should be supported by most editors [https://editorconfig.org](https://editorconfig.org).

other settings might come up. add them here.
```
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
indent_style = space
indent_size = 4
```

## File Structure

Keep the file structure as flat as possible, break things up when there is a
clear hierarchy. To start, keep everything in one file, when it gets big enough
refactor to group items in different files, then when a structure emerges, group
files into folders/directories.

## Naming Things

Things should be names should describe exactly what it represents. They can be
long but minimal, enough to describe what it is. Avoid one-letter variables if
possible.

### Variables

Prefer `snake_case` for long variable names for readability, like
`unique_item_key` instead of `uniqueItemKey`. Constants should be
`SCREAMING_SNAKE_CASE`.

### Classes/Structs/Types

These should be `PascalCase` if describing an item. If it's a variant, use
a combination of pascal case and snake case `PascalCase_TypeA`.

This is useful in cases like:

```
Vehicle_Owned :: struct {
    owner: string,
    make: string,
    model: string,
}

Vehicle_Rental :: struct {
    owner: string,
    renter: string,
    price_rate: int,
    make: string,
    model: string,
}
```

### Function

Prefer verbs that communicate what it does. If it accepts any arguments, it
should describe what it does to the argument. It should be readable as English:
instead of `normalize(x)` or `normalize(word)` it should read
`normalize(username)` be specific. This also applies for function definitions.

Add parameter and return types if the language allows it.

### Git Branches

Branch naming is undecided. At the very least, it should be descriptive of the
changes in the branch. Commit granularity and good commit messages are more
important! Unclear branch names can be supplemented in PR description and by
reading commit messages (and code changes).


## Misc

### No magic numbers

If a value is used multiple times in different places,
refactor them into a constant variable and use the variables instead of putting
in raw values. This helps when refactoring since there's only one place to
change. It also prevents using incorrect values caused by typos. Misspelled
variables are errors! So it's easy to know when there's a mistake.

### Comments

Leave comments for yourself or others tagged with:
- TODO:
- NOTE:
- WARN:
- HACK:

These are just the common ones. Feel free to come up with other tags. It's just
to make things easy to search pending tasks or improve "hacks". Do not explain
what the code does in comments. The code should be self-explanatory, else the
naming might need improvement.


# Collaboration

## Source-Control Workflow

We use [trunk based development](https://trunkbaseddevelopment.com/) flow. 

> A source-control branching model, where developers collaborate on code in a
> single branch called ’trunk’* and resist any pressure to create other
> long-lived development branches by employing documented techniques. They
> therefore avoid merge hell, do not break the build, and live happily ever
> after.

In our case, the trunk is the `main` branch. When developing, create a branch
off of main write changes then create a pull request (PR) for review and run
tests. The project should have tests!

Use a merge-queue to make sure no changes are merged that are incompatible with
any of the previous PRs. New changes should be **rebased** on the `main` branch
so that new work is built on top of the latest state of trunk. 

### Pull Requests

A PR does not have to be a complete "feature", think of it as a group of
commits. It could just be whatever work has been done during the day.
Preferably, all changes in a PR should be related to make it easy to review.

The **commits** are the unit of work. Make commits often and write descriptive
commit messages. All changes/files should be related to the message. Fun fact,
you can write multi-line commit messages:

```
git commit -m "Message Title[press Enter]
[press Enter]
Start of a paragraph[press Enter]
paragraph body[press Enter]
paragraph body[press Enter]
paragraph body[press Enter]" #<- finish the message with a closing quotation mark 

# Finally, press Enter again to run the command.
```


### Releases

When making a release, `trunk/main` should be stabilized first. Then make a new
branch for the release named as `release-year-month-day`. No changes should be 
made to this branch! If there needs to be fixes, publish it to a new release.

## Testing

Tests should not be written by AI (if you are using it for development). Would
you let students write the questions for their final exam? Tests are there to
prevent changes by your future self or other collaborators from breaking your
past work. 

Treat tests as documentation. It should show how pieces of code are meant to be
used and when they should break. Include failure states in tests when a state
should not be possible in the project.

Ideally, every major feature should have a set of tests verifying its
functionality. If a bug is discovered, write a test that reproduces it, then
write necessary changes that fixes the bug and pass the test.

We do this work to allow us to build quickly and confidently.

## Scripting

Write scripts for routine tasks to do in a project. (I) prefer using
[just](https://just.systems/). Save some brainspace and keystrokes. There should
be a script to setup a project from scratch to be used when someone just
cloned the repository. Make it easy to get started and start building.

They should be cross-platform (Windows/Mac/Linux), if some terminal commands are
not available on all platforms, there should be a platform-specific script that
does the same thing. Or better yet, a script that is conditional (platform
aware) and just runs the platform specific commands. 

Example:
```
set shell := ["bash", "-cu"]

env_activated := env("VIRTUAL_ENV", "")

warn := '\033[31mWARN\033[0m'
todo := '\033[31mTODO\033[0m'

[private]
@default:
  just --list

[private]
[no-exit-message]
@check-virtual-env:
  if [[ -z "{{env_activated}}" ]]; then echo -e "{{todo}}: activate virtualenv" && exit 1; fi

@setup:
  if [[ ! -d ".venv" ]]; then uv venv; else echo -e "{{warn}}: '.venv/' already exists"; fi

@install-deps: check-virtual-env
  uv sync

alias i := install
@install py_package section='': check-virtual-env
    uv add {{py_package}} {{section}}

@migrate: check-virtual-env (erd "-a")
  python manage.py makemigrations
  python manage.py migrate

@run: check-virtual-env migrate
  python manage.py runserver

@test arg='-s': check-virtual-env
  pytest {{arg}}

# run tests in watch mode
@watch: check-virtual-env
  watchexec -e py just test

new-app name: check-virtual-env
  python manage.py startapp {{name}}

manage *command: check-virtual-env
  python manage.py {{command}}

# generate ERD diagram for an app
erd *app='-a': check-virtual-env
  python manage.py graph_models {{app}} -o docs/erd/{{app}}.png
```

## Owner and review

Owned by Director’s Office. Reviewed semi-annually or after any significant incident.
