# Changelog

All notable changes to this project will be documented in this file. See [commit-conventions](https://conventionalcommits.org) for commit guidelines.

## [0.8.0](https://github.com/AtaCanYmc/reactive-resume-api-client-py/compare/v0.7.0...v0.8.0) (2026-11-18)


### Features

* complete v0.7.0 roadmap features and establish v0.8.0 / v1.0.0 milestones ([e008a93](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/e008a935c9fef291f98896fba0ee07c8d872c6bf))

## [0.7.0](https://github.com/AtaCanYmc/reactive-resume-api-client-py/compare/v0.6.0...v0.7.0) (2026-11-18)


### Features

* add Files and Career APIs, structured dates, resume checks, and kanban lanes ([80166a5](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/80166a584c76b338d7a98668b216dc057738e04a))
* add Makefile with development, testing, and linting targets ([be5b93b](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/be5b93bac8841f65beae74a1b82fa0250e2896a4))
* align SDK with Reactive Resume v6.1.1 API, health endpoint, and standalone cover letters ([38240ed](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/38240ed8bc20f92517e0d4b04fac50d4d03ff776))
* **brew:** add Homebrew formula for rxresume CLI and FastMCP server ([d92b9ad](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/d92b9adf4e90bb389c42817d55524f3623b0ac53))
* **cli:** implement full-featured rxresume command-line interface ([51a3d76](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/51a3d76af0e80bba1701a64fe87b491784ee17d4))
* **docs:** replace mkdocs with custom modern web documentation UI ([2f754ff](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/2f754ff62eccb882e2aa329cf5e3345920ff4e63))
* **mcp:** add FastMCP server with tools, resources, and prompt templates ([0da90b4](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/0da90b4bdbbfd1bbd99c8baecee397281f84bf15))


### Bug Fixes

* **ci:** bump python matrix to 3.11/3.12 and pin secure dnspython/filelock to resolve pip-audit failure ([2fee396](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/2fee396f8136b12ec7c67af3fb3335c315379c89))
* **ci:** install mcp extra in CI and use importorskip for fastmcp tests ([7267303](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/7267303ffc98d9f40eae682beb57c1e181caf9c9))
* **ci:** upgrade setuptools before dependency audit to prevent runner image vulnerability failure ([9721f84](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/9721f8497e61124701b97160db431f08ba09f4a0))
* **docs:** deploy custom web docs directory to gh-pages branch via peaceiris action ([3f846ac](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/3f846ac2007fec3e8d92bd490cce7b26e6fb7b45))
* **security:** resolve dependency vulnerabilities and harden demo configuration ([3622bd5](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/3622bd5d6a8b938b13d3ab2e2c5966c32d561b32))


### Documentation

* establish anti-slop documentation and repository governance ([2a06b1a](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/2a06b1a26f7e8bc7e89f231a466b88f08e5658dd))

## [0.6.0](https://github.com/AtaCanYmc/reactive-resume-api-client-py/compare/v0.5.0...v0.6.0) (2026-08-25)


### Features

* add Flask demo application with Docker support and resume management features ([a37de3b](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/a37de3b11e4363a93c9a0075213f280832e7f6aa))


### Bug Fixes

* correct condition for publishing to PyPI in release workflow ([a584974](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/a58497454e7f887ece8159b15734202b763359a4))
* update site URL in mkdocs configuration ([6d69992](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/6d699926806252bdec31210ca05f98765afdadfc))

## [0.5.0](https://github.com/AtaCanYmc/reactive-resume-api-client-py/compare/v0.4.0...v0.5.0) (2026-07-14)


### Features

* enhance documentation with architecture and capability matrix, and improve error handling examples ([cf99a46](https://github.com/AtaCanYmc/reactive-resume-api-client-py/commit/cf99a465a00b84eb3622198771ea5d8813261d60))

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
