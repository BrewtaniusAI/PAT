# Signed Provenance

PAT currently includes:
- `provenance.json` as an unsigned publication stub
- receipts for SHA256-based artifact integrity
- proof bundles for archival packaging

Optional future path:
1. generate artifact
2. generate receipt
3. generate proof bundle
4. sign provenance metadata with your preferred key
5. archive artifact + proof materials

Example structure:
- `provenance.signed.example.json`

This release does not require signed provenance to remain useful as executable prior art.
