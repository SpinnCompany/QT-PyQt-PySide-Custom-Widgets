# Final release checklist

## Release readiness

- [x] Confirm package metadata and version in pyproject.toml
- [x] Verify the test suite passes in a clean environment
- [ ] Build wheel and sdist artifacts
- [ ] Review README and install instructions for accuracy
- [ ] Verify changelog/release notes are ready
- [ ] Confirm optional dependency groups are documented
- [ ] Tag the release and publish artifacts

## Verification commands

```bash
.venv/bin/pytest -q
.venv/bin/python -m build
```

## Notes

- The current test baseline is green: 647 passed.
- The current packaging build should be validated once the build backend is available in the environment.
