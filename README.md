# VRC-A Image Store

Public files the VRC-A app downloads at run time, so they aren't bundled in the APK.

## Layout

| Path | What | Written by |
|---|---|---|
| `images/<group>/<name>.<ext>` | Pictures the app shows. | People (edit freely) |
| `manifest.json` | Every picture's key, path, SHA-256 and size. **The app reads this.** | The `Rebuild manifest` Action (don't edit by hand) |
| `tools/build_manifest.py` | Builds `manifest.json` from `images/`. | |
| `avatars/db.json` | The avatar catalog backup. | The avatar catalog bots (don't touch) |
| `osc_tutorial_1..4.png`, `vrchat-1102x620.jpg` (root) | Old paths, still loaded by app versions from before the manifest. Delete once nobody runs those versions. | |

Groups the app uses today:

- `images/tutorial/1..4` — the OSC tutorial's step pictures (keys `tutorial/1` … `tutorial/4`).
- `images/tos/` — the Terms of Service pictures (keys `tos/<name>`; the terms refer to them by name).
- `images/discord/default` — the Discord Rich Presence default image.

Rich-content media (announcements, What's New) isn't here as files: the admin editor uploads it as assets of the `rich-media` release.

## Updating a picture

- **Replace** a file with one of the same name: every user gets the new one the next time that screen loads (the app compares the SHA-256 in the manifest).
- **Add** a file to `images/tos/`: it's available to the terms as `tos/<name>` without an app update.
- **Remove or rename**: make sure nothing still asks for the old key first (an app screen or the terms).

Each push that changes `images/` runs the `Rebuild manifest` Action, which commits the new `manifest.json` within a minute or so. The raw CDN can take up to ~5 minutes to show the change.
