# Changelog

All notable changes to this project will be documented in this file. See [commit-conventions](https://conventionalcommits.org) for commit guidelines.

## [0.2.0](https://github.com/AtaCanYmc/reactive-resume-api-client-py/compare/v0.1.0...v0.2.0) (2026-07-13)


### Features

* add documentation for asynchronous and synchronous clients, bulk import example, and resume management ([e9c40c4](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/e9c40c4168513d025336b1e5db1198747426b013))
* add mypy as a development dependency and configure type checking ([e852ada](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/e852adab4b44ed2e94bfa7c266054c8efa45c5f4))
* update release-please configuration to include publishing to PyPI ([55ab756](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/55ab756811225917fd498d1021fa58ffa1057ba9))

## 0.1.0 (2026-07-13)


### Features

* add .gitignore, CHANGELOG, and CONTRIBUTING files ([de634ae](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/de634ae6b83b53c06f87ee1c68738bb60ba88528))
* add bandit as a development dependency in various configuration files ([ce3d407](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/ce3d407f77c1b6e38c799e0e55696832bbe6fb9b))
* add CI pipeline and PR title validation workflows ([d2f8cf9](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/d2f8cf9eb7aebef1009f3425a0ed1cd66b7ff384))
* add Dependabot configuration and release workflows for PyPI publishing ([4d91c03](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/4d91c03ef0ccbfd34eb0152025b96220c7d7008d))
* add pre-commit configuration and update .gitignore, README, and various files for formatting ([b907653](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/b907653c439194d7035e683eaffc2a6cf6756b8f))
* add pytest-cov as a development dependency in configuration files ([a0ccdeb](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/a0ccdeb595cd5d4f190eb7cdd3316c6f2aaa13ef))

## 0.1.0 (2026-07-13)

### Features
- Initial release of `rxresume-python` SDK.
- Support for synchronous client (`RxResumeClient`) and asynchronous client (`AsyncRxResumeClient`).
- Custom exceptions for error status codes.
- Complete Pydantic v2 schemas for Resume and User details.
- CI/CD workflow automation (tests, linting, bandit, PyPI publishing, and release-please).
