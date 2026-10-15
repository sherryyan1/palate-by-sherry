# Installation

Open Codex in the environment where you want to work on your slides, then paste:

```text
Install the palate Codex skill from https://github.com/sherryyan1/palate-by-sherry.

Check the environment where Codex runs, follow docs/installation.md, and verify that $palate is available. If palate is already installed, ask before replacing it.
```

Codex can inspect the environment, select an appropriate runtime and install the small runtime package described below. You do not need to choose an installation directory or run the advanced commands yourself. It may need your approval to write outside the current project, install a missing dependency or authenticate to a private repository. Use the available secure GitHub sign-in; never paste a password or token into the conversation.

Installation makes **palate** available to Codex. Editing and reviewing a particular deck also depend on the tools available in that environment. Codex should explain any missing capability before promising a finished file.

## Install in the environment that will do the work

The computer displaying Codex and the environment running its tools may be different. A remote or cloud session needs the skill and its dependencies in that execution environment; installing them on your laptop does not automatically install them there.

| Environment | What Codex should check |
| :--- | :--- |
| Windows | A discoverable skills directory, Python and the helper dependencies. The included slide-rendering script also needs desktop Microsoft PowerPoint. Windows cannot complete native Keynote save and review. |
| macOS | A discoverable skills directory, Python and the helper dependencies. Native Keynote delivery needs Keynote on the Mac. The included Windows rendering script does not run here. |
| Linux or a remote execution environment | A discoverable skills directory, Python and the helper dependencies. Check for a compatible presentation editor and rendering workflow separately; installing the skill does not supply desktop PowerPoint or Keynote. |
| iPhone or iPad | Do not treat these as supported native installation environments. A client may connect to another execution environment, whose installation and editing capabilities must be checked separately. |

The [usage guide](usage.md) explains which files and application checks a slide task needs. A successful installation does not establish native application access or complete a deck's scientific, editability or visual checks.

## Procedure for Codex

Follow these steps when handling the installation request. They apply to the execution environment, including when the user is working through a remote client.

1. **Inspect the source and existing installation.** Read this repository's `SKILL.md`, `requirements.txt` and `scripts/package_skill.py` from an existing trusted checkout or a small temporary checkout of the requested revision. If access is private, use the environment's configured authentication. Identify the active Codex skills directories and look for both `palate` and the legacy `palate-by-sherry` before writing anything. Ask before replacing an existing installation, even if its managed files are unchanged. Preserve local edits and do not create a second discoverable copy to bypass that decision.
2. **Select the runtime and destination.** Reuse a bundled Python runtime when available; otherwise check for Python 3.11 or later. Check `lxml` and Pillow in that same interpreter. If either is missing, explain the required setup and obtain any necessary environment permission before installing the repository's requirements. Choose a directory the running Codex actually scans, rather than assuming the bundled installer default matches this host. Current Codex supports `.agents/skills` discovery; some environments also use a configured or legacy `$CODEX_HOME/skills` directory. Reuse a recognized existing location when updating, and keep the install directory named `palate` so the invocation remains `$palate`.
3. **Build and install the explicit runtime package.** Use `scripts/package_skill.py` with a fresh output filename and the chosen `palate` destination. Its `FILES` allowlist is the package contract. Do not recursively copy the repository root or include development documents, research material, README assets, tests or Git metadata. For an approved update, the installer verifies the complete managed tree and archives its previous contents outside skill discovery. If it reports edits, an unmanaged tree or a linked destination, stop and preserve that installation while agreeing on the resolution with the user.
4. **Verify the installed files and discovery.** Compare every installed runtime file with `package-manifest.json`, check that `SKILL.md` declares `name: palate`, and confirm that Codex lists or offers the installed skill as enabled. Use an available skill-listing interface or the `$` skill picker. File presence alone does not confirm discovery. Codex normally detects skill changes automatically; if the skill is absent, reload or restart Codex and check again. Report an unconfirmed installation as pending discovery rather than ready to use.
5. **Report what is available.** Identify the installed revision, discovery result, dependency checks and any application-dependent limits. The user can then attach a deck and ask `Use $palate to polish my slides.` Keep native application access and final-deck validation separate from the installation result.

For current discovery and invocation guidance, see [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Why the repository uses a runtime package

The skill entrypoint lives at the repository root, with its runtime references and scripts in sibling directories. The standard Codex Skill Installer can select that root only when the caller supplies the root path and the destination name explicitly. Selecting it does not enforce this repository's runtime allowlist.

An isolated Windows test of the bundled installer's Git method with `--path . --name palate` produced a directory containing `SKILL.md` and Git metadata but omitted the runtime subdirectories because of its sparse checkout. The download method copies the selected tree without applying the package allowlist. Neither is the recommended installation route for this repository. Codex should use the existing package builder and managed installer rather than claiming that an ordinary root install is complete.

The managed route was tested on Windows in a disposable destination: runtime hashes matched the package, edited and unmanaged installations were preserved, and the installed skill was discovered as enabled from a repository-scoped `.agents/skills/palate` directory. These checks did not replace an existing user installation or exercise native slide editing. macOS and Linux installation were not executed in that test; Codex must verify their environment and discovery when installing there.

## Advanced manual setup

These commands are for users or agents who want to run the existing installer directly. Work from the repository root, use the Python executable selected for the execution environment, and replace the destination placeholder with its actual absolute path. Typical modern locations are the user's `~/.agents/skills/palate` or a project's `.agents/skills/palate`; an environment may instead recognize a configured `$CODEX_HOME/skills/palate`. Check discovery before choosing.

If the selected interpreter does not already provide the helper dependencies:

```text
python -m pip install -r requirements.txt
```

Build and install using a fresh package filename:

```text
python scripts/package_skill.py --output dist/palate-install.zip --install "<absolute-skills-directory>/palate"
```

The installer refuses to overwrite an existing package archive. For an update approved by the user, choose a new filename such as `dist/palate-update.zip`. An unchanged managed installation is recoverably archived; a modified or unmanaged installation is left intact.

An approved migration from the earlier directory name must identify the exact sibling explicitly:

```text
python scripts/package_skill.py --output dist/palate-migration.zip --install "<absolute-skills-directory>/palate" --migrate-legacy "<absolute-skills-directory>/palate-by-sherry"
```

The same preservation checks apply to the legacy installation. Do not rename or delete a user-edited skill to get around a refusal. Repository updates, package builds and installed skills are synchronized explicitly; a Git pull alone does not update the installed copy.
