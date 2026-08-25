"""Flask web application demonstrating the usage of rxresume-python SDK."""

import os
from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for

from reactive_resume import ReactiveResumeError, RxResumeClient
from reactive_resume.models import Basics, ResumeImportData

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "reactive-resume-demo-secret-key")

# Configuration from Environment
RX_RESUME_URL = os.environ.get("RX_RESUME_URL", "https://rxresu.me")
RX_RESUME_API_KEY = os.environ.get("RX_RESUME_API_KEY", "")


def get_client() -> RxResumeClient:
    """Return an initialized RxResumeClient instance."""
    api_key = os.environ.get("RX_RESUME_API_KEY", RX_RESUME_API_KEY)
    base_url = os.environ.get("RX_RESUME_URL", RX_RESUME_URL)
    return RxResumeClient(base_url=base_url, api_key=base_url_to_key(api_key))


def base_url_to_key(key: str) -> str:
    """Helper to return key."""
    return key


@app.route("/")  # type: ignore[misc]
def index() -> str:
    """Render home page with SDK configuration status."""
    has_api_key = bool(os.environ.get("RX_RESUME_API_KEY", RX_RESUME_API_KEY))
    return render_template(
        "index.html",
        server_url=RX_RESUME_URL,
        has_api_key=has_api_key,
    )


@app.route("/resumes")  # type: ignore[misc]
def list_resumes() -> str:
    """Fetch and list all resumes for the configured user."""
    client = get_client()
    resumes: list[Any] = []
    error_message = None

    try:
        resumes = client.resumes.list()
    except ReactiveResumeError as e:
        error_message = str(e)

    return render_template(
        "resumes.html",
        resumes=resumes,
        error_message=error_message,
    )


@app.route("/resumes/<resume_id>")  # type: ignore[misc]
def view_resume(resume_id: str) -> str:
    """View detailed information and download link for a specific resume."""
    client = get_client()
    resume = None
    pdf_url = None
    error_message = None

    try:
        resume = client.resumes.get(resume_id)
        pdf_url = client.resumes.get_pdf_url(resume_id)
    except ReactiveResumeError as e:
        error_message = str(e)

    return render_template(
        "resume_detail.html",
        resume=resume,
        pdf_url=pdf_url,
        error_message=error_message,
    )


@app.route("/import", methods=["GET", "POST"])  # type: ignore[misc]
def import_resume() -> Any:
    """Form and action to import a new candidate resume."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        headline = request.form.get("headline", "").strip()
        email = request.form.get("email", "").strip()
        title = request.form.get("title", f"{name} - Resume").strip()

        if not name or not email:
            flash("Name and Email are required fields.", "error")
            return render_template("import.html")

        client = get_client()
        import_payload = ResumeImportData(
            title=title,
            basics=Basics(
                name=name,
                headline=headline,
                email=email,
            ),
        )

        try:
            created_resume = client.resumes.import_resume(import_payload)
            flash(f"Resume '{created_resume.name}' imported successfully!", "success")
            return redirect(url_for("view_resume", resume_id=created_resume.id))
        except ReactiveResumeError as e:
            flash(f"Failed to import resume: {e}", "error")

    return render_template("import.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
