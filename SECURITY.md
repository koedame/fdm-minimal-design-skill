# Security Policy

## Reporting a vulnerability

Please report security problems privately through
[GitHub's private vulnerability reporting](https://github.com/koedame/fdm-minimal-design-skill/security/advisories/new).
Do not open a public issue for them.

We will reply within 7 days to confirm that we received your report, and keep you updated until it is fixed.

## Supported versions

Only the latest commit on `main`, the latest release and the website (https://fdm-minimal-design.koeda.me) get
security fixes.

## What counts as a vulnerability

- A script of the skill or a tool in this repository that runs code, writes files outside its output folder or reads
  the network when given a design, a model or an option it accepts
- A viewer page (`viewer.py`) or the website running script that is not its own, or loading anything from another
  server
- A secret or personal information in the repository, a release or the website

The dimensions and the strength of printed parts are not security problems; see "No warranty and safety" in the
README.
