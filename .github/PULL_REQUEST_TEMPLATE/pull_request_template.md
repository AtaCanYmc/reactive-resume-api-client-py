## Description

Provide a clear and concise summary of the changes proposed in this pull request.

## Type of Change

- [ ] `feat`: A new feature or endpoint mapping
- [ ] `fix`: A bug fix or error handling improvement
- [ ] `docs`: Documentation updates
- [ ] `refactor`: Code change that neither fixes a bug nor adds a feature
- [ ] `test`: Adding missing tests or updating existing tests
- [ ] `ci` / `chore`: Maintenance, dependencies, or workflow changes

## Verification Steps

List the exact commands used to verify the changes:

```bash
make check
```

## Checklist

- [ ] PR title follows Conventional Commits format (`type(scope): description`)
- [ ] Code formatting passes (`make format-check`)
- [ ] Type checking passes (`make typecheck`)
- [ ] Linter & security scan pass (`make lint`)
- [ ] All tests pass (`make test`)
