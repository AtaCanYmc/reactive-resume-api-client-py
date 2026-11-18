"""Main CLI entrypoint for Reactive Resume."""

import argparse
import sys

from reactive_resume.core.exceptions import ReactiveResumeError

from .commands import (
    handle_agent,
    handle_ai,
    handle_applications,
    handle_auth,
    handle_config,
    handle_flags,
    handle_resumes,
    handle_stats,
)
from .config import get_client


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser hierarchy."""
    parser = argparse.ArgumentParser(
        prog="rxresume",
        description="Command-line interface for Reactive Resume v4 API",
    )
    parser.add_argument("--url", help="Base URL of the Reactive Resume instance")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--token", help="Bearer token for authentication")
    parser.add_argument("--profile", help="Configuration profile to use")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument("-v", "--version", action="version", version="rxresume 0.6.0")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Config
    p_config = subparsers.add_parser("config", help="Manage CLI configuration and profiles")
    config_sub = p_config.add_subparsers(dest="config_action", required=True)
    config_sub.add_parser("show", help="Show current configuration")
    p_url = config_sub.add_parser("set-url", help="Set Reactive Resume URL for profile")
    p_url.add_argument("url", help="Reactive Resume server URL")
    p_key = config_sub.add_parser("set-key", help="Set API key for profile")
    p_key.add_argument("key", help="API key")
    p_prof = config_sub.add_parser("use-profile", help="Switch active profile")
    p_prof.add_argument("name", help="Profile name")

    # 2. Resumes
    p_resumes = subparsers.add_parser("resumes", help="Resume management commands")
    resumes_sub = p_resumes.add_subparsers(dest="resumes_action", required=True)
    resumes_sub.add_parser("list", help="List all resumes")

    p_r_get = resumes_sub.add_parser("get", help="Get resume details by ID")
    p_r_get.add_argument("id", help="Resume ID")

    p_r_dl = resumes_sub.add_parser("download", help="Download resume PDF")
    p_r_dl.add_argument("id", help="Resume ID")
    p_r_dl.add_argument("-o", "--output", help="Output file path (default: <id>.pdf)")

    p_r_imp = resumes_sub.add_parser("import", help="Import a resume from JSON file")
    p_r_imp.add_argument("-f", "--file", required=True, help="Path to JSON file")

    p_r_dup = resumes_sub.add_parser("duplicate", help="Duplicate an existing resume")
    p_r_dup.add_argument("id", help="Source resume ID")
    p_r_dup.add_argument("--name", required=True, help="New resume name")
    p_r_dup.add_argument("--slug", required=True, help="New resume slug")

    p_r_del = resumes_sub.add_parser("delete", help="Delete a resume by ID")
    p_r_del.add_argument("id", help="Resume ID to delete")
    p_r_del.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt")

    p_r_lock = resumes_sub.add_parser("lock", help="Lock a resume against changes")
    p_r_lock.add_argument("id", help="Resume ID")

    p_r_unlock = resumes_sub.add_parser("unlock", help="Unlock a resume")
    p_r_unlock.add_argument("id", help="Resume ID")

    p_r_pwd = resumes_sub.add_parser("password", help="Manage resume password security")
    pwd_sub = p_r_pwd.add_subparsers(dest="pwd_action", required=True)
    p_pwd_set = pwd_sub.add_parser("set", help="Set a password for resume")
    p_pwd_set.add_argument("id", help="Resume ID")
    p_pwd_set.add_argument("-p", "--password", required=True, help="Password")
    p_pwd_rm = pwd_sub.add_parser("remove", help="Remove password protection")
    p_pwd_rm.add_argument("id", help="Resume ID")
    p_pwd_vf = pwd_sub.add_parser("verify", help="Verify resume password")
    p_pwd_vf.add_argument("id", help="Resume ID")
    p_pwd_vf.add_argument("-p", "--password", required=True, help="Password to check")

    p_r_pub = resumes_sub.add_parser("public", help="Fetch a public resume by username and slug")
    p_r_pub.add_argument("username", help="Author username")
    p_r_pub.add_argument("slug", help="Resume slug")

    # 3. AI
    p_ai = subparsers.add_parser("ai", help="AI and document parsing commands")
    ai_sub = p_ai.add_subparsers(dest="ai_action", required=True)

    p_ai_pdf = ai_sub.add_parser("parse-pdf", help="Parse PDF into resume data")
    p_ai_pdf.add_argument("file", help="Path to PDF file")
    p_ai_pdf.add_argument("--provider", required=True, help="AI Provider ID")

    p_ai_docx = ai_sub.add_parser("parse-docx", help="Parse DOCX into resume data")
    p_ai_docx.add_argument("file", help="Path to DOCX file")
    p_ai_docx.add_argument("--provider", required=True, help="AI Provider ID")

    p_ai_an = ai_sub.add_parser("analyze", help="Analyze resume and retrieve recommendations")
    p_ai_an.add_argument("id", help="Resume ID")
    p_ai_an.add_argument("--provider", required=True, help="AI Provider ID")

    p_ai_prov = ai_sub.add_parser("providers", help="List or test AI providers")
    prov_sub = p_ai_prov.add_subparsers(dest="providers_action", required=True)
    prov_sub.add_parser("list", help="List configured AI providers")
    p_pr_test = prov_sub.add_parser("test", help="Test AI provider connection")
    p_pr_test.add_argument("id", help="AI Provider ID")

    # 4. Agent
    p_agent = subparsers.add_parser("agent", help="AI agent interaction commands")
    agent_sub = p_agent.add_subparsers(dest="agent_action", required=True)
    agent_sub.add_parser("threads", help="List active agent threads")

    p_ag_send = agent_sub.add_parser("send", help="Send a message to an agent thread")
    p_ag_send.add_argument("thread_id", help="Agent thread ID")
    p_ag_send.add_argument("message", help="Message content to send")

    p_ag_arch = agent_sub.add_parser("archive", help="Archive an agent thread")
    p_ag_arch.add_argument("thread_id", help="Agent thread ID")

    p_ag_chat = agent_sub.add_parser("chat", help="Start interactive agent chat session")
    p_ag_chat.add_argument("--thread-id", help="Existing thread ID (creates new if omitted)")
    p_ag_chat.add_argument("--resume-id", help="Source resume ID")
    p_ag_chat.add_argument("--provider", help="AI Provider ID")

    # 5. Applications
    p_apps = subparsers.add_parser("applications", help="Job application tracking commands")
    apps_sub = p_apps.add_subparsers(dest="applications_action", required=True)
    apps_sub.add_parser("list", help="List all job applications")

    p_app_get = apps_sub.add_parser("get", help="Get application details by ID")
    p_app_get.add_argument("id", help="Application ID")

    p_app_del = apps_sub.add_parser("delete", help="Delete application by ID")
    p_app_del.add_argument("id", help="Application ID")

    apps_sub.add_parser("stats", help="Get application pipeline statistics")

    # 6. Auth
    p_auth = subparsers.add_parser("auth", help="Authentication and account commands")
    auth_sub = p_auth.add_subparsers(dest="auth_action", required=True)
    auth_sub.add_parser("providers", help="List configured authentication providers")

    p_auth_exp = auth_sub.add_parser("export", help="Export account data")
    p_auth_exp.add_argument("-o", "--output", help="Save account data to JSON file")

    # 7. Stats
    p_stats = subparsers.add_parser("stats", help="System statistics commands")
    stats_sub = p_stats.add_subparsers(dest="stats_metric", required=True)
    stats_sub.add_parser("users", help="Get total number of users")
    stats_sub.add_parser("resumes", help="Get total number of resumes")
    stats_sub.add_parser("stars", help="Get GitHub star count")

    # 8. Flags
    subparsers.add_parser("flags", help="List feature flags")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run CLI with given arguments."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # Config actions do not require an active API client
    if args.command == "config":
        return handle_config(args, None)  # type: ignore[arg-type]

    try:
        client = get_client(
            url=args.url,
            api_key=args.api_key,
            token=args.token,
            profile=args.profile,
        )

        handlers = {
            "resumes": handle_resumes,
            "ai": handle_ai,
            "agent": handle_agent,
            "applications": handle_applications,
            "auth": handle_auth,
            "stats": handle_stats,
            "flags": handle_flags,
        }

        handler = handlers.get(args.command)
        if handler:
            return handler(args, client)
        parser.print_help()
        return 1
    except ReactiveResumeError as err:
        sys.stderr.write(f"Error: {err}\n")
        return 1
    except Exception as err:  # noqa: BLE001
        sys.stderr.write(f"Unexpected error: {err}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
