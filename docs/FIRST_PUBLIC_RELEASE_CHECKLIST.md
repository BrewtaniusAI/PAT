# First Public Release Checklist

## Final sanity checks
- [ ] pytest passes
- [ ] pat release-check returns ready=true
- [ ] pat version matches release tag
- [ ] README is polished
- [ ] LICENSE present

## Generate proof artifacts
- [ ] run pipeline
- [ ] generate receipt
- [ ] generate proof bundle

## Publish
- [ ] git tag v1.0.0
- [ ] push tag
- [ ] verify GitHub release created
- [ ] upload to Zenodo
- [ ] attach DOI to README

## Announce
- [ ] share repo link
- [ ] include purpose and context
