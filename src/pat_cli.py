from __future__ import annotations
import argparse
import json
from pathlib import Path
from pat_audit.jsonl_export import append_jsonl
from pat_audit.proof_export import export_proof_bundle
from pat_audit.receipts import write_receipt
from pat_builder.batch import build_dataset_batch
from pat_builder.builder import build_dataset
from pat_pipeline.pipeline import run_pipeline
from pat_release import check_release_readiness
from pat_release_pack import generate_release_summary
from pat_validation.schema_check import validate_pipeline_output_file
from pat_version import get_version

def main() -> None:
    parser = argparse.ArgumentParser(prog="pat")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("text")
    run_parser.add_argument("--profile", dest="profile_code", default=None)
    run_parser.add_argument("--log", dest="log_path", default=None)

    build_parser = subparsers.add_parser("build-dataset")
    build_parser.add_argument("input_path")
    build_parser.add_argument("output_path")

    batch_parser = subparsers.add_parser("build-dataset-batch")
    batch_parser.add_argument("input_dir")
    batch_parser.add_argument("output_dir")

    receipt_parser = subparsers.add_parser("receipt")
    receipt_parser.add_argument("path")

    proof_parser = subparsers.add_parser("proof")
    proof_parser.add_argument("path")

    release_parser = subparsers.add_parser("release-check")
    release_parser.add_argument("--repo-root", default=".")

    summary_parser = subparsers.add_parser("release-summary")
    summary_parser.add_argument("--repo-root", default=".")

    validate_parser = subparsers.add_parser("validate-output")
    validate_parser.add_argument("output_path")
    validate_parser.add_argument("--schema", default="schemas/pipeline_output.schema.json")

    version_parser = subparsers.add_parser("version")

    chat_parser = subparsers.add_parser("chat", help="Interactive AI chat in African languages")
    chat_parser.add_argument("--profile", dest="profile_code", default=None, help="Language profile code (e.g. yo, sw, ha)")
    chat_parser.add_argument("--backend", default=None, help="LLM backend: ollama, openai, anthropic, echo")
    chat_parser.add_argument("--model", default=None, help="Model name override")

    web_parser = subparsers.add_parser("chat-web", help="Launch web-based chat UI")
    web_parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    web_parser.add_argument("--port", type=int, default=8080, help="Port to bind (default: 8080)")
    web_parser.add_argument("--profile", dest="profile_code", default=None, help="Language profile code")
    web_parser.add_argument("--backend", default=None, help="LLM backend: ollama, openai, anthropic, echo")
    web_parser.add_argument("--model", default=None, help="Model name override")

    args = parser.parse_args()

    if args.command == "run":
        result = run_pipeline(args.text, profile_code=args.profile_code)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.log_path:
            append_jsonl(args.log_path, result)
    elif args.command == "build-dataset":
        out = build_dataset(args.input_path, args.output_path)
        print(str(out))
    elif args.command == "build-dataset-batch":
        result = build_dataset_batch(args.input_dir, args.output_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.command == "receipt":
        out = write_receipt(args.path)
        print(str(out))
    elif args.command == "proof":
        out = export_proof_bundle(args.path)
        print(str(out))
    elif args.command == "release-check":
        print(json.dumps(check_release_readiness(Path(args.repo_root)), indent=2, ensure_ascii=False))
    elif args.command == "release-summary":
        print(json.dumps(generate_release_summary(Path(args.repo_root)), indent=2, ensure_ascii=False))
    elif args.command == "validate-output":
        print(json.dumps(validate_pipeline_output_file(args.output_path, args.schema), indent=2, ensure_ascii=False))
    elif args.command == "version":
        print(get_version())
    elif args.command == "chat":
        from pat_chat.cli import run_chat_cli
        run_chat_cli(
            backend_name=args.backend,
            profile_code=args.profile_code,
            model=args.model,
        )
    elif args.command == "chat-web":
        from pat_chat.web import run_web_server
        run_web_server(
            host=args.host,
            port=args.port,
            backend_name=args.backend,
            profile_code=args.profile_code,
            model=args.model,
        )

if __name__ == "__main__":
    main()
