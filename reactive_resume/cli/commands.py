"""CLI Command Handlers."""

import base64
import json
from pathlib import Path
from typing import Any

from reactive_resume.core.client import RxResumeClient
from reactive_resume.core.exceptions import ReactiveResumeError
from reactive_resume.models import ResumeImportData

from .config import load_config, save_config
from .formatters import format_json, print_table


# ---------------------------------------------------------------------------
# Config Commands
# ---------------------------------------------------------------------------
def handle_config(args: Any, _client: RxResumeClient) -> int:
    """Handle config management commands."""
    config = load_config()
    action = args.config_action

    if action == "show":
        print(format_json(config))
        return 0

    if action == "set-url":
        profile = args.profile or config.get("current_profile", "default")
        config.setdefault("profiles", {}).setdefault(profile, {})["url"] = args.url
        save_config(config)
        print(f"Profile '{profile}' URL set to: {args.url}")
        return 0

    if action == "set-key":
        profile = args.profile or config.get("current_profile", "default")
        config.setdefault("profiles", {}).setdefault(profile, {})["api_key"] = args.key
        save_config(config)
        print(f"Profile '{profile}' API key updated.")
        return 0

    if action == "use-profile":
        if args.name not in config.get("profiles", {}):
            config.setdefault("profiles", {})[args.name] = {}
        config["current_profile"] = args.name
        save_config(config)
        print(f"Switched active profile to: {args.name}")
        return 0

    return 0


# ---------------------------------------------------------------------------
# Resumes Commands
# ---------------------------------------------------------------------------
def handle_resumes(args: Any, client: RxResumeClient) -> int:
    """Handle resume operations."""
    action = args.resumes_action

    if action == "list":
        resumes = client.resumes.list()
        if args.format == "json":
            print(format_json(resumes))
        else:
            headers = ["ID", "Name", "Slug", "Locked", "Updated At"]
            rows = [
                [
                    r.id,
                    r.name,
                    r.slug,
                    str(r.locked),
                    r.updated_at.strftime("%Y-%m-%d %H:%M") if r.updated_at else "",
                ]
                for r in resumes
            ]
            print_table(headers, rows)
        return 0

    if action == "get":
        resume = client.resumes.get(args.id)
        if args.format == "json":
            print(format_json(resume))
        else:
            headers = ["Field", "Value"]
            rows = [
                ["ID", resume.id],
                ["Name", resume.name],
                ["Slug", resume.slug],
                ["Visibility", resume.visibility],
                ["Locked", str(resume.locked)],
                ["Created At", str(resume.created_at)],
                ["Updated At", str(resume.updated_at)],
            ]
            print_table(headers, rows)
        return 0

    if action == "download":
        fmt = getattr(args, "export_format", "pdf")
        content_bytes = client.resumes.export(args.id, format=fmt)
        out_path = Path(args.output or f"{args.id}.{fmt}")
        out_path.write_bytes(content_bytes)
        print(f"File saved to: {out_path}")
        return 0

    if action == "import":
        with open(args.file, encoding="utf-8") as f:
            data = json.load(f)
        payload = ResumeImportData.model_validate(data)
        created = client.resumes.import_resume(payload)
        print(f"Resume imported successfully: {created.name} (ID: {created.id})")
        return 0

    if action == "batch-import":
        return _handle_batch_import(args, client)

    if action == "duplicate":
        new_resume = client.resumes.duplicate(
            resume_id=args.id,
            name=args.name,
            slug=args.slug,
        )
        print(f"Resume duplicated successfully: {new_resume.name} (ID: {new_resume.id})")
        return 0

    if action == "delete":
        if not args.yes:
            confirm = input(f"Delete resume '{args.id}'? [y/N]: ").strip().lower()
            if confirm not in ("y", "yes"):
                print("Operation cancelled.")
                return 1
        client.resumes.delete(args.id)
        print(f"Resume '{args.id}' deleted.")
        return 0

    if action == "lock":
        client.resumes.lock(args.id, is_locked=True)
        print(f"Resume '{args.id}' locked.")
        return 0

    if action == "unlock":
        client.resumes.lock(args.id, is_locked=False)
        print(f"Resume '{args.id}' unlocked.")
        return 0

    if action == "password":
        if args.pwd_action == "set":
            client.resumes.set_password(args.id, args.password)
            print(f"Password set for resume '{args.id}'.")
        elif args.pwd_action == "remove":
            client.resumes.remove_password(args.id)
            print(f"Password removed from resume '{args.id}'.")
        elif args.pwd_action == "verify":
            valid = client.resumes.verify_password(args.id, args.password)
            print(f"Password valid: {valid}")
        return 0

    if action == "public":
        resume = client.resumes.get_public_resume(args.username, args.slug)
        if args.format == "json":
            print(format_json(resume))
        else:
            print(f"Public Resume: {resume.name} ({resume.slug})")
            print(f"User: {args.username}")
        return 0

    return 0


def _handle_batch_import(args: Any, client: RxResumeClient) -> int:
    """Handle batch importing multiple resumes from a directory."""
    target_dir = Path(args.path)
    if not target_dir.exists():
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    files: list[Path] = []
    if target_dir.is_file():
        files.append(target_dir)
    else:
        file_fmt = getattr(args, "import_format", "auto")
        if file_fmt in ("auto", "json", "json_resume"):
            files.extend(sorted(target_dir.glob("*.json")))
        if file_fmt in ("auto", "pdf"):
            files.extend(sorted(target_dir.glob("*.pdf")))

    if not files:
        print(f"No matching resume files found in '{args.path}'.")
        return 0

    dry_run = getattr(args, "dry_run", False)
    results: list[dict[str, Any]] = []

    for file_path in files:
        file_res: dict[str, Any] = {"file": file_path.name, "status": "PENDING"}
        try:
            if file_path.suffix.lower() == ".json":
                with open(file_path, encoding="utf-8") as f:
                    raw_data = json.load(f)

                is_json_resume = (
                    isinstance(raw_data, dict)
                    and (
                        "basics" in raw_data or raw_data.get("$schema", "").find("jsonresume") != -1
                    )
                    and "sections" not in raw_data
                )

                if is_json_resume:
                    from ..utils.json_resume import from_json_resume, validate_json_resume

                    is_valid, errors = validate_json_resume(raw_data)
                    if not is_valid:
                        file_res["status"] = "INVALID"
                        file_res["error"] = "; ".join(errors[:2])
                        results.append(file_res)
                        continue

                    resume_data = from_json_resume(raw_data)
                    import_payload = ResumeImportData(
                        title=file_path.stem.replace("-", " ").replace("_", " ").title(),
                        slug=file_path.stem.lower(),
                        data=resume_data,
                    )
                else:
                    import_payload = ResumeImportData.model_validate(raw_data)

                if dry_run:
                    file_res["status"] = "VALID"
                    file_res["title"] = import_payload.title
                else:
                    created = client.resumes.import_resume(import_payload)
                    file_res["status"] = "IMPORTED"
                    file_res["id"] = created.id
                    file_res["title"] = created.name

            elif file_path.suffix.lower() == ".pdf":
                if dry_run:
                    file_res["status"] = "VALID_PDF"
                else:
                    imported = client.resumes.file_import(
                        format="PDF",
                        file_bytes=file_path.read_bytes(),
                        filename=file_path.name,
                    )
                    file_res["status"] = "IMPORTED"
                    file_res["id"] = imported.id
            else:
                file_res["status"] = "SKIPPED"
                file_res["error"] = "Unsupported file format"

        except Exception as exc:  # noqa: BLE001
            file_res["status"] = "FAILED"
            file_res["error"] = str(exc)

        results.append(file_res)

    if getattr(args, "format", "table") == "json":
        print(format_json(results))
    else:
        success_count = sum(1 for r in results if r["status"] in ("IMPORTED", "VALID", "VALID_PDF"))
        print(f"\nBatch Import Summary ({'DRY RUN' if dry_run else 'EXECUTED'}):")
        print(f"Total Files Scanned: {len(results)}")
        print(f"Succeeded / Valid:   {success_count}")
        print(f"Failed / Invalid:    {len(results) - success_count}\n")
        headers = ["File", "Status", "ID", "Title", "Error"]
        rows = [
            [
                r.get("file", ""),
                r.get("status", ""),
                r.get("id", ""),
                r.get("title", ""),
                r.get("error", ""),
            ]
            for r in results
        ]
        print_table(headers, rows)

    return 0 if all(r["status"] in ("IMPORTED", "VALID", "VALID_PDF") for r in results) else 1


# ---------------------------------------------------------------------------
# AI Commands
# ---------------------------------------------------------------------------
def handle_ai(args: Any, client: RxResumeClient) -> int:
    """Handle AI and document parsing commands."""
    action = args.ai_action

    if action == "parse-pdf":
        file_path = Path(args.file)
        data_bytes = file_path.read_bytes()
        b64_data = base64.b64encode(data_bytes).decode("ascii")
        result = client.ai.parse_pdf(file_path.name, b64_data, args.provider)
        print(format_json(result))
        return 0

    if action == "parse-docx":
        file_path = Path(args.file)
        data_bytes = file_path.read_bytes()
        b64_data = base64.b64encode(data_bytes).decode("ascii")
        result = client.ai.parse_docx(file_path.name, b64_data, args.provider)
        print(format_json(result))
        return 0

    if action == "analyze":
        result = client.ai.analyze_resume(args.id, args.provider)
        print(format_json(result))
        return 0

    if action == "providers":
        if args.providers_action == "list":
            providers = client.ai_providers.list()
            if args.format == "json":
                print(format_json(providers))
            else:
                headers = ["ID", "Label", "Model"]
                rows = [
                    [p.get("id", ""), p.get("label", ""), p.get("model", "")] for p in providers
                ]
                print_table(headers, rows)
        elif args.providers_action == "test":
            success = client.ai_providers.test(args.id)
            print(f"Provider connection test: {'SUCCESS' if success else 'FAILED'}")
        return 0

    return 0


# ---------------------------------------------------------------------------
# Agent Commands
# ---------------------------------------------------------------------------
def handle_agent(args: Any, client: RxResumeClient) -> int:
    """Handle agent interaction commands."""
    action = args.agent_action

    if action == "threads":
        threads = client.agent.list_threads()
        if args.format == "json":
            print(format_json(threads))
        else:
            headers = ["Thread ID", "Resume ID", "AI Provider ID"]
            rows = [
                [t.get("id", ""), t.get("sourceResumeId", ""), t.get("aiProviderId", "")]
                for t in threads
            ]
            print_table(headers, rows)
        return 0

    if action == "send":
        resp = client.agent.send_message(args.thread_id, args.message)
        print(format_json(resp))
        return 0

    if action == "archive":
        client.agent.archive_thread(args.thread_id)
        print(f"Thread '{args.thread_id}' archived.")
        return 0

    if action == "chat":
        thread_id = args.thread_id
        if not thread_id:
            created = client.agent.create_thread(
                ai_provider_id=args.provider,
                source_resume_id=args.resume_id,
            )
            thread_id = created.get("id")
            print(f"Created new agent thread: {thread_id}")

        print(f"Starting chat session on thread {thread_id}. Type 'exit' to quit.\n")
        while True:
            try:
                user_input = input("You > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nEnding session.")
                break
            if not user_input or user_input.lower() in ("exit", "quit"):
                break
            try:
                reply = client.agent.send_message(thread_id, user_input)
                print(f"Agent > {reply.get('content') or reply}\n")
            except ReactiveResumeError as e:
                print(f"Error: {e}\n")
        return 0

    return 0


# ---------------------------------------------------------------------------
# Applications Commands
# ---------------------------------------------------------------------------
def handle_applications(args: Any, client: RxResumeClient) -> int:
    """Handle job application tracking commands."""
    action = args.applications_action

    if action == "list":
        apps = client.applications.list()
        if args.format == "json":
            print(format_json(apps))
        else:
            headers = ["ID", "Company", "Position", "Stage", "Date"]
            rows = [
                [
                    a.id,
                    a.company,
                    a.position,
                    a.stage,
                    a.date.strftime("%Y-%m-%d") if a.date else "",
                ]
                for a in apps
            ]
            print_table(headers, rows)
        return 0

    if action == "get":
        app_obj = client.applications.get(args.id)
        print(format_json(app_obj))
        return 0

    if action == "delete":
        client.applications.delete(args.id)
        print(f"Application '{args.id}' deleted.")
        return 0

    if action == "stats":
        stats = client.applications.get_pipeline_stats()
        print(format_json(stats))
        return 0

    return 0


# ---------------------------------------------------------------------------
# Auth Commands
# ---------------------------------------------------------------------------
def handle_auth(args: Any, client: RxResumeClient) -> int:
    """Handle authentication endpoints."""
    action = args.auth_action

    if action == "providers":
        providers = client.auth.list_providers()
        print(format_json(providers) if args.format == "json" else "\n".join(providers))
        return 0

    if action == "export":
        data = client.auth.export_account()
        out_file = args.output
        if out_file:
            Path(out_file).write_text(format_json(data), encoding="utf-8")
            print(f"Account data exported to: {out_file}")
        else:
            print(format_json(data))
        return 0

    return 0


# ---------------------------------------------------------------------------
# Stats Commands
# ---------------------------------------------------------------------------
def handle_stats(args: Any, client: RxResumeClient) -> int:
    """Handle statistics commands."""
    metric = args.stats_metric

    if metric == "users":
        count = client.statistics.get_users_count()
        print(f"Users: {count}")
    elif metric == "resumes":
        count = client.statistics.get_resumes_count()
        print(f"Resumes: {count}")
    elif metric == "stars":
        stars = client.statistics.get_github_stars()
        print(f"GitHub Stars: {stars}")
    return 0


# ---------------------------------------------------------------------------
# Flags Commands
# ---------------------------------------------------------------------------
def handle_flags(args: Any, client: RxResumeClient) -> int:
    """Handle feature flags commands."""
    flags = client.flags.list()
    print(format_json(flags))
    return 0


# ---------------------------------------------------------------------------
# Health Commands
# ---------------------------------------------------------------------------
def handle_health(args: Any, client: RxResumeClient) -> int:
    """Handle system health and version inspection."""
    health = client.health()
    if args.format == "json":
        print(format_json(health))
    else:
        print(f"Service:  {health.service} v{health.version} (Status: {health.status})")
        print(f"Uptime:   {health.uptime}")
        print(f"Database: {health.database.status} ({health.database.latency_ms} ms)")
        print(f"Storage:  {health.storage.status} ({health.storage.latency_ms} ms)")
        if health.redis:
            print(f"Redis:    {health.redis.status} ({health.redis.latency_ms} ms)")
    return 0 if health.status == "healthy" else 1


# ---------------------------------------------------------------------------
# Cover Letters Commands
# ---------------------------------------------------------------------------
def handle_cover_letters(args: Any, client: RxResumeClient) -> int:
    """Handle standalone cover letter operations."""
    action = args.cover_letters_action

    if action == "list":
        letters = client.cover_letters.list()
        if args.format == "json":
            print(format_json(letters))
        else:
            headers = ["ID", "Name", "Slug", "Locked", "Updated At"]
            rows = [
                [
                    c.id,
                    c.name,
                    c.slug,
                    str(c.is_locked),
                    c.updated_at.strftime("%Y-%m-%d %H:%M") if c.updated_at else "",
                ]
                for c in letters
            ]
            print_table(headers, rows)
        return 0

    if action == "get":
        letter = client.cover_letters.get(args.id)
        if args.format == "json":
            print(format_json(letter))
        else:
            print(f"Cover Letter: {letter.name} (ID: {letter.id})")
            print(f"Slug: {letter.slug}")
            print(f"Content:\n{letter.content}")
        return 0

    if action == "export":
        fmt = getattr(args, "export_format", "pdf")
        content_bytes = client.cover_letters.export(args.id, format=fmt)
        out_path = Path(args.output or f"{args.id}.{fmt}")
        out_path.write_bytes(content_bytes)
        print(f"File saved to: {out_path}")
        return 0

    if action == "delete":
        client.cover_letters.delete(args.id)
        print(f"Cover letter '{args.id}' deleted (moved to Trash).")
        return 0

    return 0


# ---------------------------------------------------------------------------
# Documents & Trash Commands
# ---------------------------------------------------------------------------
def handle_documents(args: Any, client: RxResumeClient) -> int:
    """Handle document lifecycle and trash commands."""
    action = args.documents_action

    if action == "counts":
        counts = client.documents.get_counts()
        print(format_json(counts))
        return 0

    if action == "trash":
        client.documents.trash(args.type, args.id)
        print(f"Moved {args.type} '{args.id}' to Trash.")
        return 0

    if action == "restore":
        client.documents.restore(args.id, doc_type=args.type)
        print(f"Restored {args.type} '{args.id}' from Trash.")
        return 0

    if action == "purge":
        client.documents.purge(args.id, doc_type=args.type)
        print(f"Permanently purged {args.type} '{args.id}'.")
        return 0

    return 0


# ---------------------------------------------------------------------------
# Custom Domain Commands
# ---------------------------------------------------------------------------
def handle_custom_domain(args: Any, client: RxResumeClient) -> int:
    """Handle custom domain commands."""
    action = args.custom_domain_action

    if action == "get":
        info = client.custom_domain.get()
        print(format_json(info))
        return 0

    if action == "set":
        res = client.custom_domain.set(args.hostname)
        print(format_json(res))
        return 0

    if action == "verify":
        res = client.custom_domain.verify()
        print(format_json(res))
        return 0

    if action == "delete":
        client.custom_domain.delete()
        print("Custom domain removed.")
        return 0

    return 0


# ---------------------------------------------------------------------------
# MCP Commands
# ---------------------------------------------------------------------------
def handle_mcp(args: Any, _client: RxResumeClient) -> int:
    """Handle running the FastMCP Model Context Protocol server."""
    try:
        import sys

        from reactive_resume.mcp.server import create_mcp_server

        mcp = create_mcp_server(
            url=getattr(args, "url", None),
            api_key=getattr(args, "api_key", None),
            token=getattr(args, "token", None),
            profile=getattr(args, "profile", None),
        )
        if getattr(args, "transport", "stdio") == "sse":
            port = getattr(args, "port", 8000)
            print(f"Starting Reactive Resume FastMCP server on SSE port {port}...", file=sys.stderr)
            mcp.run(transport="sse", port=port)
        else:
            mcp.run(transport="stdio")
        return 0
    except ImportError:
        print("Error: FastMCP is not installed. Install with: pip install 'rxresume-python[mcp]'")
        return 1
