# Contributing to Learn FASTER

Thank you for your interest in contributing to Learn FASTER!

## Conventional Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated changelog generation and semantic versioning.

### Commit Message Format

Each commit message should follow this structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature (triggers minor version bump)
- **fix**: A bug fix (triggers patch version bump)
- **docs**: Documentation only changes
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **build**: Changes to build system or dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Breaking Changes

To trigger a major version bump, add `BREAKING CHANGE:` in the footer or append `!` after the type:

```
feat!: change API interface

BREAKING CHANGE: The /learn command now requires a topic parameter
```

### Examples

```
feat: add quiz generation for learned concepts

This allows users to test their knowledge after completing a topic.
```

```
fix: correct review schedule calculation

Previously the schedule was doubling instead of using fibonacci intervals.
```

```
docs: update README with new installation instructions
```

```
refactor: simplify progress tracking logic
```

## Release Process

This project uses [release-please](https://github.com/googleapis/release-please) for automated releases:

1. Commit your changes using conventional commit format
2. Push to `main` branch
3. Release-please will automatically create a PR with:
   - Updated version in `pyproject.toml`
   - Updated CHANGELOG.md
   - Release notes
4. Review and merge the release PR
5. A GitHub release will be created automatically

## Version Bumping

- **Major** (1.0.0 → 2.0.0): Breaking changes (`feat!:` or `BREAKING CHANGE:`)
- **Minor** (1.0.0 → 1.1.0): New features (`feat:`)
- **Patch** (1.0.0 → 1.0.1): Bug fixes (`fix:`)
