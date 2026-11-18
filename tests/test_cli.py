"""Tests for the rxresume CLI interface."""

import json

import pytest
import respx
from httpx import Response

from reactive_resume.cli.main import build_parser, main

BASE_URL = "https://rxresu.me"

MOCK_RESUME = {
    "id": "res-1",
    "name": "Dev CV",
    "slug": "dev-cv",
    "userId": "user-1",
    "visibility": "public",
    "locked": False,
    "data": {"basics": {"name": "Dev", "headline": "Dev", "email": "dev@test.com"}},
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-01-01T00:00:00Z",
}


def test_parser_version():
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--version"])
    assert exc.value.code == 0


def test_cli_config(tmp_path, monkeypatch, capsys):
    mock_config_file = tmp_path / "config.json"
    monkeypatch.setattr("reactive_resume.cli.config.CONFIG_FILE", mock_config_file)
    monkeypatch.setattr("reactive_resume.cli.config.CONFIG_DIR", tmp_path)

    # 1. set-url
    assert main(["config", "set-url", "https://custom.rxresu.me"]) == 0
    captured = capsys.readouterr()
    assert "https://custom.rxresu.me" in captured.out

    # 2. set-key
    assert main(["config", "set-key", "secret-key-123"]) == 0
    captured = capsys.readouterr()
    assert "API key updated" in captured.out

    # 3. use-profile
    assert main(["config", "use-profile", "prod"]) == 0
    captured = capsys.readouterr()
    assert "prod" in captured.out

    # 4. show
    assert main(["config", "show"]) == 0
    captured = capsys.readouterr()
    assert "prod" in captured.out


@respx.mock
def test_cli_resumes_list_and_get(capsys):
    respx.get(f"{BASE_URL}/api/openapi/resumes").mock(
        return_value=Response(200, json=[MOCK_RESUME])
    )
    respx.get(f"{BASE_URL}/api/openapi/resumes/res-1").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )

    # list (table)
    ret = main(["--url", BASE_URL, "--api-key", "test", "resumes", "list"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "res-1" in captured.out
    assert "Dev CV" in captured.out

    # list (json)
    ret = main(["--url", BASE_URL, "--api-key", "test", "--format", "json", "resumes", "list"])
    assert ret == 0
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert len(parsed) == 1
    assert parsed[0]["id"] == "res-1"

    # get (table)
    ret = main(["--url", BASE_URL, "--api-key", "test", "resumes", "get", "res-1"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "res-1" in captured.out


@respx.mock
def test_cli_resumes_actions(capsys):
    respx.post(f"{BASE_URL}/api/openapi/resumes/res-1/lock").mock(
        return_value=Response(200, json=MOCK_RESUME)
    )
    respx.delete(f"{BASE_URL}/api/openapi/resumes/res-1").mock(
        return_value=Response(200, json={"success": True})
    )
    respx.put(f"{BASE_URL}/api/openapi/resumes/res-1/password").mock(
        return_value=Response(200, json={"success": True})
    )
    respx.delete(f"{BASE_URL}/api/openapi/resumes/res-1/password").mock(
        return_value=Response(200, json={"success": True})
    )
    respx.post(f"{BASE_URL}/api/openapi/resumes/res-1/password").mock(
        return_value=Response(200, json={"success": True})
    )

    # lock / unlock
    assert main(["--url", BASE_URL, "--api-key", "test", "resumes", "lock", "res-1"]) == 0
    assert main(["--url", BASE_URL, "--api-key", "test", "resumes", "unlock", "res-1"]) == 0

    # password set/remove/verify
    assert (
        main(
            [
                "--url",
                BASE_URL,
                "--api-key",
                "test",
                "resumes",
                "password",
                "set",
                "res-1",
                "-p",
                "secret",
            ]
        )
        == 0
    )
    assert (
        main(["--url", BASE_URL, "--api-key", "test", "resumes", "password", "remove", "res-1"])
        == 0
    )
    assert (
        main(
            [
                "--url",
                BASE_URL,
                "--api-key",
                "test",
                "resumes",
                "password",
                "verify",
                "res-1",
                "-p",
                "secret",
            ]
        )
        == 0
    )

    # delete with -y
    assert main(["--url", BASE_URL, "--api-key", "test", "resumes", "delete", "res-1", "-y"]) == 0
    captured = capsys.readouterr()
    assert "deleted" in captured.out


@respx.mock
def test_cli_stats_flags_auth(capsys):
    respx.get(f"{BASE_URL}/api/openapi/statistics/users").mock(return_value=Response(200, json=100))
    respx.get(f"{BASE_URL}/api/openapi/statistics/resumes").mock(
        return_value=Response(200, json=50)
    )
    respx.get(f"{BASE_URL}/api/openapi/statistics/github/stars").mock(
        return_value=Response(200, json=999)
    )
    respx.get(f"{BASE_URL}/api/openapi/flags").mock(
        return_value=Response(200, json={"isSignupsDisabled": False})
    )
    respx.get(f"{BASE_URL}/api/openapi/auth/providers").mock(
        return_value=Response(200, json=["github", "google"])
    )

    assert main(["--url", BASE_URL, "--api-key", "test", "stats", "users"]) == 0
    assert main(["--url", BASE_URL, "--api-key", "test", "stats", "resumes"]) == 0
    assert main(["--url", BASE_URL, "--api-key", "test", "stats", "stars"]) == 0
    assert main(["--url", BASE_URL, "--api-key", "test", "flags"]) == 0
    assert main(["--url", BASE_URL, "--api-key", "test", "auth", "providers"]) == 0


@respx.mock
def test_cli_error_handling(capsys):
    respx.get(f"{BASE_URL}/api/openapi/resumes/unknown").mock(
        return_value=Response(404, json={"message": "Resume not found"})
    )
    ret = main(["--url", BASE_URL, "--api-key", "test", "resumes", "get", "unknown"])
    assert ret == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


@respx.mock
def test_cli_v6_commands(capsys):
    # Health
    respx.get(f"{BASE_URL}/api/health").mock(
        return_value=Response(
            200,
            json={
                "service": "reactive-resume",
                "version": "6.1.1",
                "status": "healthy",
                "timestamp": "2026-11-18T18:00:00Z",
                "uptime": "10d",
                "database": {"status": "healthy", "latencyMs": 1.0},
                "storage": {"status": "healthy", "latencyMs": 1.2},
            },
        )
    )
    assert main(["--url", BASE_URL, "health"]) == 0
    captured = capsys.readouterr()
    assert "reactive-resume v6.1.1" in captured.out

    # Cover letters
    respx.get(f"{BASE_URL}/api/openapi/cover-letters").mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "cl-1",
                    "name": "CL 1",
                    "slug": "cl-1",
                    "isLocked": False,
                    "createdAt": "2026-01-01T00:00:00Z",
                    "updatedAt": "2026-01-01T00:00:00Z",
                }
            ],
        )
    )
    assert main(["--url", BASE_URL, "--api-key", "test", "cover-letters", "list"]) == 0

    # Documents counts
    respx.get(f"{BASE_URL}/api/openapi/documents/counts").mock(
        return_value=Response(200, json={"resumes": 2, "coverLetters": 1, "trash": 0})
    )
    assert main(["--url", BASE_URL, "--api-key", "test", "documents", "counts"]) == 0

    # Custom domain
    respx.get(f"{BASE_URL}/api/openapi/custom-domain").mock(
        return_value=Response(200, json={"hostname": "cv.test.com"})
    )
    assert main(["--url", BASE_URL, "--api-key", "test", "custom-domain", "get"]) == 0


@respx.mock
def test_cli_batch_import(tmp_path, capsys):
    # 1. Create a json resume file
    cv1 = tmp_path / "resume1.json"
    cv1.write_text(
        json.dumps(
            {
                "basics": {"name": "Alice", "email": "alice@test.com"},
                "work": [{"name": "Company A", "position": "Dev"}],
            }
        )
    )

    # 2. Create a reactive resume file
    cv2 = tmp_path / "resume2.json"
    cv2.write_text(
        json.dumps(
            {
                "title": "Bob CV",
                "slug": "bob-cv",
                "data": {"basics": {"name": "Bob", "headline": "Engineer"}},
            }
        )
    )

    # 3. Create a dummy pdf file
    cv3 = tmp_path / "resume3.pdf"
    cv3.write_bytes(b"%PDF-1.4 mock pdf content")

    # Dry-run
    res = main(
        [
            "--url",
            BASE_URL,
            "--api-key",
            "test",
            "resumes",
            "batch-import",
            str(tmp_path),
            "--dry-run",
        ]
    )
    assert res == 0
    captured = capsys.readouterr()
    assert "DRY RUN" in captured.out
    assert "Total Files Scanned: 3" in captured.out
    assert "Succeeded / Valid:   3" in captured.out

    # Execute
    respx.post(f"{BASE_URL}/api/openapi/resumes/import").mock(
        return_value=Response(
            201,
            json={
                "id": "res-imp-1",
                "title": "Imported CV",
                "name": "Imported CV",
                "slug": "imp-cv",
                "data": {},
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z",
            },
        )
    )
    respx.post(f"{BASE_URL}/api/openapi/resumes/file-imports").mock(
        return_value=Response(
            201,
            json={
                "id": "res-imp-pdf",
                "name": "Imported PDF CV",
                "slug": "imp-pdf-cv",
                "data": {},
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z",
            },
        )
    )
    res_exec = main(
        ["--url", BASE_URL, "--api-key", "test", "resumes", "batch-import", str(tmp_path)]
    )
    assert res_exec == 0
    captured_exec = capsys.readouterr()
    assert "EXECUTED" in captured_exec.out
    assert "res-imp-1" in captured_exec.out
    assert "res-imp-pdf" in captured_exec.out
