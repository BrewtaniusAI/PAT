# PAT v0.8.0 Public Alpha

PAT is a patent-free Pan-African language infrastructure project released as executable public knowledge.

This public alpha includes:
- governed execution pipeline
- validation and policy enforcement
- language profiles for Yorùbá, Kiswahili, and isiZulu
- dataset builder and batch dataset processing
- receipts and proof bundle export
- schema validation and release integrity checks
- contribution and community language guidance

## Core commands
```bash
pat run "Ẹ káàárọ̀ Africa" --profile yo
pat build-dataset input.json output.json
pat receipt output.json
pat proof output.json
pat validate-output output.json
pat release-check --repo-root .
```
