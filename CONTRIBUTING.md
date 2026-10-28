# Contributing

## Setup

You may have already noticed that this repo's structure looks a little different than a typical fork.
That's because it only contains the world itself and treats Archipelago as a dependency/library.
While this removes a lot of unnecessary bloat from this repo, it requires a bit of setup.
You can find the reasoning for this in [cjmang/Archipelago#68](https://github.com/cjmang/Archipelago/issues/68).

### Prerequisites

1. A clone of [Archipelago](https://github.com/ArchipelagoMW/Archipelago) with its own virtual environment,
   set up as described
   in [Running From Source](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/running%20from%20source.md).
   Make sure you install the `requirements.txt`, `ci-requirements.txt` (and optionally the `WebHostLib/requirements.txt`).
   This gstla repo does not contain the real Archipelago code. It links to your checkout and runs everything through its
   interpreter.
   This also allows us to re-use an existing installation across multiple APWorlds. For example, the "Slay The Spire 2"
   world works similar.
2. [uv](https://docs.astral.sh/uv/) 0.13.4 or newer. For now, it is only used to install the linter
   ([ruff](https://docs.astral.sh/ruff/)), the type checker ([pyrefly](https://pyrefly.org/en/docs/)) and
   the command runner ([just](https://github.com/casey/just)) that is used for every task in this repo. The real APWorld
   requirements are still in `worlds/gstla/requirements.txt`.

### First run

1. Copy `.env.local.template` to `.env.local` and set all variables.
2. Run `uv sync`. It creates a virtual environment in `.venv` with `ruff`, `pyrefly` and `just`. All `just` commands
   below are run as `uv run just <command>`. If you have `just` installed globally, a normal `just <command>` works too.
3. Run `uv run just setup`. It creates `external/archipelago` as a link to your Archipelago checkout and links
   our `worlds/gstla` into its `worlds/` folder, so Archipelago can properly register the world.
4. Run `uv run just check` and `uv run just test`. Note: As of now, ruff and pyrefly will show some errors. This will
   be fixed in the future. New contributions should make sure to not introduce any new ones.

### Commands

| Command             | What it does                                                                                        |
|---------------------|-----------------------------------------------------------------------------------------------------|
| `just setup`        | Creates the links between the AP checkout and this repo. Every command runs this first.             |
| `just check`        | Run the linter, format and type checks via ruff and pyrefly.                                        |
| `just test`         | Run our world's tests with the Archipelago interpreter. Arguments will be passed through to pytest. |
| `just start-server` | Generates a single-player multiworld from `fixtures/gstla-test.yaml` and hosts it locally.          |
| `just start-client` | Starts the BizHawk client against the local server.                                                 |
| `just build`        | Builds a release-ready APWorld (TODO, gotta use this in github workflows)                           |

### Editors

- **PyCharm**: Use the python interpreter from the Archipelago checkout as the project interpreter and add that repos
  root directory to its interpreter paths. Otherwise imports such as `BaseClasses` show as unresolved. (If you only use
  pyrefly checking inside of PyCharm, you can probably skip this step.)
- **VSCode**: Not tested. Feel free to open an issue or Pull Request for this.

## Commit messages

Your commit messages *should* describe what you have changed and why.
You can leave out the "why" if it's immediately visible and understandable
or there is a comment directly in the code explaining it.
So no "fix stuff". A "fix typo in option XYZ" is fine.
