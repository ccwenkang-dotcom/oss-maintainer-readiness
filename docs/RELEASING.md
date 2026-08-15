# Release Process

This checklist keeps releases reproducible and makes maintainer responsibility visible.

## Before Tagging

1. Confirm the working branch is based on the latest `main`.
2. Review open issues and pull requests that target the release.
3. Update the version in `pyproject.toml`.
4. Update `CHANGELOG.md` with user-visible changes and the release date.
5. Run the full local validation:

   ```bash
   python -m pip install -e ".[dev]"
   python -m pytest -q
   python -m build
   ```

6. Open a pull request and wait for all CI jobs to pass.
7. Merge the pull request using a traceable merge or squash commit.

## Create the Release

1. Create an annotated tag matching the package version, for example `v0.1.0`.
2. Create a GitHub Release from that tag.
3. Use the matching changelog section as the release notes.
4. Attach the source distribution and wheel produced by CI when available.
5. Verify the tagged GitHub Action example in `README.md` resolves correctly.

## After Release

1. Install the tagged version in a clean environment.
2. Run one public-repository check and verify both report files are generated.
3. Open issues for deferred work rather than silently changing release scope.
4. Record regressions and security concerns through the normal issue or security process.

## Versioning

The project follows semantic versioning where practical:

- Patch releases fix defects without intentionally changing the evidence model.
- Minor releases add compatible evidence sources, report fields, or workflow features.
- Major releases may change score semantics, report schemas, or command-line compatibility.

Scoring changes must be documented because they can change repository status even when the inspected repository has not changed.
