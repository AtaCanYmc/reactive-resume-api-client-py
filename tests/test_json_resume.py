"""Tests for JSON Resume validation, export, and import utilities."""

from reactive_resume.models.resume import (
    Basics,
    Resume,
    ResumeData,
    ResumeItemDates,
    Section,
    WorkItem,
)
from reactive_resume.utils.json_resume import from_json_resume, to_json_resume, validate_json_resume


def test_validate_json_resume_valid():
    sample = {
        "basics": {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "profiles": [
                {"network": "GitHub", "username": "janedoe", "url": "https://github.com/janedoe"}
            ],
        },
        "work": [
            {
                "name": "Tech Corp",
                "position": "Lead Developer",
                "startDate": "2022-01-01",
                "endDate": "Present",
            }
        ],
        "skills": [{"name": "Python", "level": "Expert", "keywords": ["Django", "FastAPI"]}],
    }

    is_valid, errors = validate_json_resume(sample)
    assert is_valid is True
    assert len(errors) == 0


def test_validate_json_resume_invalid():
    sample = {
        "basics": {
            "email": "invalid-email-string",
            "profiles": "not-a-list",
        },
        "work": "not-a-list",
    }

    is_valid, errors = validate_json_resume(sample)
    assert is_valid is False
    assert len(errors) >= 2
    assert any("Invalid email" in e for e in errors)
    assert any("must be a list" in e for e in errors)


def test_to_json_resume_conversion():
    resume_data = ResumeData(
        basics=Basics(
            name="Alice Smith",
            headline="Software Architect",
            email="alice@example.com",
            location="Berlin, Germany",
        ),
        sections={
            "work": Section(
                id="work",
                name="Experience",
                items=[
                    WorkItem(
                        id="work-1",
                        company="Acme Corp",
                        position="Staff Engineer",
                        summary="Building scalable systems",
                        dates=ResumeItemDates(start="2020-03", end="Present", present=True),
                    )
                ],
            )
        },
    )

    from datetime import datetime

    resume = Resume(
        id="res-123",
        name="Alice's CV",
        slug="alice-cv",
        data=resume_data,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    converted = to_json_resume(resume)

    assert converted["basics"]["name"] == "Alice Smith"
    assert converted["basics"]["label"] == "Software Architect"
    assert converted["basics"]["email"] == "alice@example.com"
    assert len(converted["work"]) == 1
    assert converted["work"][0]["name"] == "Acme Corp"
    assert converted["work"][0]["position"] == "Staff Engineer"
    assert converted["work"][0]["endDate"] == "Present"

    # Validation should pass
    is_valid, errors = validate_json_resume(converted)
    assert is_valid is True, f"Validation errors: {errors}"


def test_from_json_resume_conversion():
    json_resume_input = {
        "basics": {
            "name": "Bob Marley",
            "label": "DevOps Engineer",
            "email": "bob@example.com",
            "location": {"city": "Amsterdam", "countryCode": "NL"},
        },
        "work": [
            {
                "name": "Cloud Infra Inc",
                "position": "DevOps Architect",
                "startDate": "2021-06",
                "endDate": "2024-01",
                "summary": "Kubernetes automation",
            }
        ],
        "skills": [{"name": "Kubernetes", "level": "Senior", "keywords": ["Helm", "ArgoCD"]}],
    }

    rd = from_json_resume(json_resume_input)

    assert rd.basics.name == "Bob Marley"
    assert rd.basics.headline == "DevOps Engineer"
    assert rd.basics.email == "bob@example.com"
    assert "Amsterdam" in rd.basics.location

    work_items = rd.sections["work"].items
    assert len(work_items) == 1
    assert work_items[0].company == "Cloud Infra Inc"
    assert work_items[0].position == "DevOps Architect"

    skill_items = rd.sections["skills"].items
    assert len(skill_items) == 1
    assert skill_items[0].name == "Kubernetes"
