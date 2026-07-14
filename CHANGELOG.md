# Changelog

All notable changes to this project will be documented in this file. See [commit-conventions](https://conventionalcommits.org) for commit guidelines.

## [0.4.0](https://github.com/AtaCanYmc/reactive-resume-api-client-py/compare/v0.3.0...v0.4.0) (2026-07-14)


### Features

* add AI functions and feature flags documentation to API and README ([0d7ebaa](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/0d7ebaa6fa0e1cc70017c6da111ce80c651abb60))
* add Applications API and enhance Agent API with new thread management features ([1456992](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/1456992129b1f1c158be6d7febebd298b05dd0b8))
* add Job Application models to documentation and remove unused AgentRequest and AgentResponse sections ([def99fd](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/def99fdd48eacfe9c0af3ae0d9c957ce5b94277e))
* add new postman collection ([b4571ae](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/b4571ae138b84e7179eaee4e3327714d95a8e0a7))
* enhance API documentation with new Resumes and Job Applications sections, update authentication instructions, and improve README clarity ([6cb9e67](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/6cb9e67ba4ae3f74aceefc70b807170b697ec294))
* enhance README with architecture diagram and capability matrix for service modules ([c78dfdc](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/c78dfdc23099a623c74e418d73299d99e1894527))
* implement Flags and AI APIs, enhance resumes API with additional features and tests ([1766288](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/1766288a0da1c65c5025e7c548a5af0942e113bc))
* remove Applications and Storage APIs from public interface and documentation ([a41f9ae](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/a41f9ae182e42721c0967932061f325f51fe8164))
* update README to improve clarity of service modules diagram ([003871b](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/003871ba12645c79b3b2cd196da36f657ea17536))
* update README to improve clarity of service modules diagram ([db25f74](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/db25f74b8fdca6ca4a6b6697d360df0c5c0bb57a))

## [0.3.0](https://github.com/AtaCanYmc/reactive-resume-api-client-py/compare/v0.2.0...v0.3.0) (2026-07-13)


### Features

* add API and Pydantic models documentation, enhance quickstart guide, and implement comprehensive tests ([0276c83](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/0276c8371fd70e80a44e67ac0bb858b9062629f5))
* implement Applications and Statistics APIs, add Agent communication models ([5008ba6](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/5008ba622cf02db16de543039b1dcbeb3c7dffb1))
* update README with advanced features examples and enhance API coverage description ([46bca04](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/46bca04a52d1f83d96ba8e154aeaccd61c0e9988))

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
