# Contributing

Issues and pull requests are welcome, for example a new model, a wrong dimension, or a fix to the skill's documents and scripts.

## What is accepted

- New models in `models/` (format: [`models/README.md`](models/README.md)). They must be original designs: do not copy the shape, name or logo of a specific product.
- Fixes and additions to the skill (`skills/fdm-minimal-design/`), the tools in `tools/`, the website in `site/` and the documentation.
- Do not add code or data copied from another project unless its licence allows it. Say where it comes from in the pull request.
- Do not commit generated 3D files (STEP, STL); they are regenerated from the scripts.

## Before you open a pull request

- Set up the environment as described in the [README](README.md#environment) and run the checks that `.github/workflows/ci.yml` runs. The pull request runs them too and must pass.
- Keep one change per pull request.

## Licence of your contribution

Your contribution is published under the licence of the part it changes: [MIT](LICENSE) for code and documents, [CC BY 4.0](LICENSE-CC-BY-4.0.txt) for models and images. Open a pull request only with work you made yourself and may publish that way. By opening a pull request you agree to that. There is no contributor licence agreement.

## Security problems

Report them privately as described in [`SECURITY.md`](SECURITY.md), not in an issue.
