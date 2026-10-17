# ChatGPT Work on the web

**palate** has an experimental plugin package for ChatGPT Work. It contains the same skill, design rules and helpers as the Codex package. Browser installation, activation and a complete slide-editing task have **not yet been tested**. The steps below provide a setup and testing path, not a claim of verified compatibility or an existing public directory listing.

## Set up a private plugin

Open ChatGPT on the web in the workspace where the slides will be processed and choose Work. Type `@` and select **Plugin Creator**, if it is available. OpenAI documents conversational plugin creation for workspaces with the necessary permissions; availability varies by account and workspace. See [Build plugins](https://learn.chatgpt.com/docs/build-plugins).

Send this request:

```text
Set up a private palate plugin from https://github.com/sherryyan1/palate-by-sherry.

Follow docs/chatgpt-work.md. Use scripts/package_plugin.py to build the allowlisted plugin package. Keep its SKILL.md, references and scripts unchanged; do not summarize or regenerate the design rules. Keep the plugin private.

Check whether this workspace can register the complete package, preserve its relative file paths and make its resources available to the skill. If it cannot, explain the missing capability and leave installation pending. Do not replace the scripts with prose or claim that attaching a ZIP installs a plugin.

Verify that palate appears in the @ picker in a new Work conversation. Report installation, resource access and available slide-editing tools separately. Ask before replacing an existing palate plugin and preserve any local changes.
```

If the setup conversation cannot fetch the repository, download the [source archive](https://github.com/sherryyan1/palate-by-sherry/archive/refs/heads/main.zip) in the browser and attach it, then ask Plugin Creator to build only the allowlisted package from that source. A previously built plugin ZIP is another option. Neither route requires running Python on the computer used to chat, provided the Work session can execute the builder. If it cannot, the package can be built in another authorized environment using the commands below.

Plugin Creator may need further input or may be unable to register the package in that workspace. Finish only when it has preserved the complete runtime and confirmed discovery. This repository does not assume a universal ZIP-import button or an automatic GitHub-to-ChatGPT install.

If Plugin Creator or the necessary permission is absent, ask the workspace administrator about access. Codex remains the existing installation route. Pasting `SKILL.md` into a conversation can supply instructions for that conversation, but does not install **palate** or make its other files available.

## Start a slide task

In a new Work conversation, type `@` and **select palate from the menu**. Attach an existing deck or paper, or paste text, notes or an outline. For an existing deck, ask:

```text
Polish my slides.
```

For new slides, ask `Create slides from these notes.` or `Create a research presentation from this paper.` There is no requirement to upload a deck first.

**palate** asks for missing presentation context, then checks the files and tools available to that conversation. The same audience, time, screen-format, depth and scientific safeguards apply as in Codex. For a new deck, it also confirms PowerPoint or Keynote when the delivery application has not been specified. If the venue ratio is unknown, existing slides retain their proportions; new slides start at a provisional 16:9, explicitly identified as a design assumption. Missing scientific evidence prompts a focused question, not invented results or citations. Question cards depend on the host's tools; ordinary choices in chat provide the fallback.

| Available access | What can proceed |
| :--- | :--- |
| Uploaded deck, code execution and the required dependencies | Source inspection and supported file-level edits. New or rebuilt content also needs a suitable editable-slide authoring tool. |
| Readable paper, manuscript or notes and a suitable native slide-authoring tool | Source analysis and a new editable candidate deck in the agreed application. The object-preservation helpers alone cannot create new slides. |
| Authoring and preview tools, without the delivery application | Candidate creation or editing and available previews. The report identifies the native appearance, editability and playback checks still needed. |
| Authorized access to PowerPoint | Native PowerPoint work and review, within the actual tools and permissions available. |
| Authorized access to Keynote on a Mac | The experimental native Keynote route. Its Mac integration remains untested in this project. |
| No suitable file-editing tool | Content analysis, a proposed narrative or slide content, with file creation or editing left pending. No editable-file delivery is claimed. |

A web session does not automatically control applications on a computer. If the account offers local computer access, configure it through that product's supported flow and verify the connection before relying on it. Otherwise, continue native work in an environment that has the required application. The [host workflow](../references/host-workflows.md) defines the private handoff and review requirements.

## Build the package

From a trusted checkout of the desired revision, run:

```text
python scripts/package_plugin.py --output dist/palate-work-plugin.zip
```

The builder requires Python 3.11+ and the standard library. It does not need the slide-processing dependencies to package the files. Choose a fresh output name for each build; existing outputs are preserved. To also create a fresh plugin folder for local testing:

```text
python scripts/package_plugin.py --output dist/palate-work-plugin-next.zip --directory dist/palate-work-plugin-next
```

The generated plugin has this structure:

```text
plugin.json
skills/
  palate/
    SKILL.md
    agents/
    references/
    scripts/
    requirements.txt
    package-manifest.json
```

`scripts/package_skill.py` remains the Codex builder and managed installer. Both builders use its explicit `FILES` allowlist. The plugin builder copies the reviewed metadata from `packaging/plugin.json` and places the unchanged runtime under `skills/palate/`. It includes no research, interviews, README assets, tests, Git history, MCP server or lifecycle hooks. The root manifest follows [OpenAI's portable plugin layout](https://developers.openai.com/plugins/build/plugins).

These commands create files only. They do not install a plugin, replace an installed skill, change account settings, submit a package for review or publish it. Local marketplace testing through the desktop app is a separate route; local discovery alone does not establish browser availability. Workspace or public-directory distribution requires its own authorized setup and checks.

## Verify before relying on it

| Check | Evidence to retain privately |
| :--- | :--- |
| Installation and discovery | The revision installed, the workspace used, and palate selected from the `@` picker in a new Work conversation. |
| Resource access | Every file in `package-manifest.json` is available at its relative path and matches the recorded hash. |
| Brief and routing | Short requests from slides, notes or a paper obtain only missing context; a supplied brief is reused; new decks confirm the delivery application; PowerPoint and Keynote keep their separate native routes. |
| Editing and delivery | A synthetic deck produces a new editable file with a clear report. Review scientific content, native editability and rendered appearance separately. |
| Missing native access | Any output requiring unfinished application checks is labeled as a candidate, with a specific handoff. |

Do not use confidential research for the first compatibility test. Keep test files and results private and record which checks actually ran. The [validation record](validation.md#chatgpt-work-distribution) distinguishes local package checks from browser and native-application testing.

## Updates and research privacy

Use the revision recorded for the installed package when reporting a result. A Git push, rebuilt ZIP or local Codex update does not update the private ChatGPT plugin automatically. Before replacing a plugin, preserve its existing instructions and resources, compare local changes, rebuild from the intended source revision and repeat discovery and affected task checks.

Uploads are processed in the selected ChatGPT workspace. Use research material only where its handling is authorized. **palate** preserves original files, saves revisions separately and asks before publishing research or sending it to an additional service. Keep research and task reports out of the plugin package and repository.
