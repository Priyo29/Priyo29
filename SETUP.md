# Setup

This repo renders your GitHub profile card. `README.md` is only a `<picture>`
tag; everything you see is drawn in `dark_mode.svg` / `light_mode.svg`, and
`today.py` rewrites the numbers in both on a schedule.

## 1. Create the profile repo

The repo **must** be named exactly `Priyo29` — a repo matching your username is
what GitHub renders on your profile page. Make it **public** and do not let
GitHub add a README for you.

```bash
git init -b main
git add .
git commit -m "Terminal-style profile card"
git remote add origin https://github.com/Priyo29/Priyo29.git
git push -u origin main
```

## 2. Create a token

`today.py` needs to read your commit history through the GraphQL API.

Go to **Settings → Developer settings → Personal access tokens → Fine-grained
tokens → Generate new token**, with:

- Repository access: **All repositories**
- Account permissions: `Followers: read`, `Starring: read`, `Watching: read`
- Repository permissions: `Commit statuses: read`, `Contents: read`,
  `Issues: read`, `Metadata: read`, `Pull requests: read`

Copy the token once — GitHub will not show it again.

## 3. Add the two secrets

In `Priyo29/Priyo29` → **Settings → Secrets and variables → Actions → New
repository secret**:

| Name | Value |
| --- | --- |
| `ACCESS_TOKEN` | the token from step 2 |
| `USER_NAME` | `Priyo29` |

Paste the token directly into GitHub — never commit it to a file here.

## 4. Run it

**Actions → README build → Run workflow.** The first run is the slow one: it
walks every commit in every repo to count lines of code, then writes
`cache/<hash>.txt` so later runs only look at what changed. After that it runs
itself daily at 04:00 UTC.

If the run fails on `git push`, check **Settings → Actions → General → Workflow
permissions** is set to *Read and write permissions*.

## Editing the card

Do not hand-edit the SVGs. Change `tools/build_svg.py` and regenerate:

```bash
python3 -m pip install pillow
python3 tools/build_svg.py . tools/avatar.jpg
```

To swap the portrait, drop a new image in and point the command at it.

The art separates the subject from the background by **hue, not brightness**:
in this avatar the hair and the window behind it are the same luminance
(~23/255), so a brightness threshold erases the head. The window is blue (red
chromaticity ~0.14) and the hair is warmer (~0.21), so dark cells below
`bg_chroma` become background stipple (`.`) and the rest stay empty. A
different photo will want a different `bg_chroma` — print the art with
`python3 tools/asciify.py <image>` and adjust until the silhouette reads.

Every panel row is padded to a **60-column grid**. `build_svg.py` computes the
dots for static rows automatically. For the rows `today.py` rewrites, the width
identity is:

```
len(label) + 2 + length + 2 == 60
```

so if you rename a label, change that row's `length` in `today.py`'s
`svg_overwrite` by the same amount in the opposite direction, or the column of
values will step out of line.

The "Uptime" row counts from a date near the bottom of `today.py` — it is
currently your GitHub join date, so change it to your birthday if you want it
to mean what it says.
