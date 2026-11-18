"""Native JSON Resume export and validation utilities.

Compliant with the official JSON Resume specification (https://jsonresume.org/schema/).
Provides conversion between Reactive Resume internal schema and standard JSON Resume format.
"""

from __future__ import annotations

import re
from typing import Any

from ..models.resume import (
    AwardItem,
    Basics,
    CertificationItem,
    EducationItem,
    InterestItem,
    LanguageItem,
    Profile,
    ProjectItem,
    PublicationItem,
    ReferenceItem,
    Resume,
    ResumeData,
    ResumeItemDates,
    Section,
    SkillItem,
    URLModel,
    VolunteerItem,
    WorkItem,
)

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def validate_json_resume(data: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate a dictionary against the standard JSON Resume schema.

    Args:
        data: The dictionary to validate.

    Returns:
        A tuple of (is_valid: bool, errors: list[str]).
    """
    errors: list[str] = []

    if not isinstance(data, dict):
        return False, ["Root object must be a dictionary"]

    # Validate basics
    basics = data.get("basics")
    if basics is not None:
        if not isinstance(basics, dict):
            errors.append("Field 'basics' must be a dictionary")
        else:
            email = basics.get("email")
            if email and (not isinstance(email, str) or not EMAIL_REGEX.match(email)):
                errors.append(f"Invalid email format in basics: '{email}'")

            profiles = basics.get("profiles")
            if profiles is not None:
                if not isinstance(profiles, list):
                    errors.append("'basics.profiles' must be a list")
                else:
                    for i, p in enumerate(profiles):
                        if not isinstance(p, dict):
                            errors.append(f"'basics.profiles[{i}]' must be a dictionary")

    # Validate list sections
    list_fields = [
        "work",
        "volunteer",
        "education",
        "awards",
        "certificates",
        "publications",
        "skills",
        "languages",
        "interests",
        "references",
        "projects",
    ]
    for field in list_fields:
        val = data.get(field)
        if val is not None and not isinstance(val, list):
            errors.append(f"Field '{field}' must be a list")
        elif isinstance(val, list):
            for i, item in enumerate(val):
                if not isinstance(item, dict):
                    errors.append(f"'{field}[{i}]' must be a dictionary")

    return len(errors) == 0, errors


def to_json_resume(resume_or_data: Resume | ResumeData | dict[str, Any]) -> dict[str, Any]:
    """Convert a Reactive Resume model or dictionary into JSON Resume standard format.

    Args:
        resume_or_data: Reactive Resume instance or data dictionary.

    Returns:
        Dictionary adhering to the JSON Resume v1.0.0 schema.
    """
    if isinstance(resume_or_data, Resume):
        rd: dict[str, Any] = resume_or_data.data.model_dump() if resume_or_data.data else {}
    elif isinstance(resume_or_data, ResumeData):
        rd = resume_or_data.model_dump()
    elif isinstance(resume_or_data, dict):
        rd = resume_or_data.get("data", resume_or_data)
    else:
        rd = {}

    basics_in = rd.get("basics", {})
    sections = rd.get("sections", {})

    # Extract website URL
    website_raw = basics_in.get("website", "")
    if isinstance(website_raw, dict):
        website_url = website_raw.get("href", "")
    else:
        website_url = str(website_raw)

    # Format profiles
    profiles_out: list[dict[str, str]] = []
    for p in basics_in.get("profiles", []):
        if isinstance(p, dict):
            url_raw = p.get("url", "")
            url_str = url_raw.get("href", "") if isinstance(url_raw, dict) else str(url_raw)
            profiles_out.append(
                {
                    "network": p.get("network", ""),
                    "username": p.get("username", ""),
                    "url": url_str,
                }
            )

    # Build basics
    out: dict[str, Any] = {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": {
            "name": basics_in.get("name", ""),
            "label": basics_in.get("headline", ""),
            "image": basics_in.get("picture", ""),
            "email": basics_in.get("email", ""),
            "phone": basics_in.get("phone", ""),
            "url": website_url,
            "summary": basics_in.get("about", "") or basics_in.get("summary", ""),
            "location": {
                "address": basics_in.get("location", ""),
                "city": "",
                "region": "",
                "postalCode": "",
                "countryCode": "",
            },
            "profiles": profiles_out,
        },
        "work": [],
        "volunteer": [],
        "education": [],
        "awards": [],
        "certificates": [],
        "publications": [],
        "skills": [],
        "languages": [],
        "interests": [],
        "references": [],
        "projects": [],
    }

    def _extract_items(sec_key: str) -> list[dict[str, Any]]:
        sec = sections.get(sec_key, {})
        if isinstance(sec, dict):
            return [it for it in sec.get("items", []) if isinstance(it, dict)]
        return []

    def _extract_dates(item: dict[str, Any]) -> tuple[str, str]:
        dates = item.get("dates", {})
        if isinstance(dates, dict):
            start = dates.get("start", "")
            end = "Present" if dates.get("present") else dates.get("end", "")
            return start, end
        date_str = str(item.get("date", ""))
        return date_str, ""

    # Work
    for w in _extract_items("work"):
        start, end = _extract_dates(w)
        url_raw = w.get("url", "")
        url_str = url_raw.get("href", "") if isinstance(url_raw, dict) else str(url_raw)
        out["work"].append(
            {
                "name": w.get("company", ""),
                "position": w.get("position", ""),
                "url": url_str,
                "startDate": start,
                "endDate": end,
                "summary": w.get("summary", ""),
                "highlights": [],
            }
        )

    # Volunteer
    for v in _extract_items("volunteer"):
        start, end = _extract_dates(v)
        url_raw = v.get("url", "")
        url_str = url_raw.get("href", "") if isinstance(url_raw, dict) else str(url_raw)
        out["volunteer"].append(
            {
                "organization": v.get("organization", ""),
                "position": v.get("position", ""),
                "url": url_str,
                "startDate": start,
                "endDate": end,
                "summary": v.get("summary", ""),
                "highlights": [],
            }
        )

    # Education
    for e in _extract_items("education"):
        start, end = _extract_dates(e)
        url_raw = e.get("url", "")
        url_str = url_raw.get("href", "") if isinstance(url_raw, dict) else str(url_raw)
        out["education"].append(
            {
                "institution": e.get("institution", ""),
                "url": url_str,
                "area": e.get("area", ""),
                "studyType": e.get("studyType", "") or e.get("degree", ""),
                "startDate": start,
                "endDate": end,
                "score": str(e.get("score", "")),
                "courses": [],
            }
        )

    # Awards
    for a in _extract_items("awards"):
        date_val, _ = _extract_dates(a)
        out["awards"].append(
            {
                "title": a.get("title", ""),
                "date": date_val or a.get("date", ""),
                "awarder": a.get("awarder", ""),
                "summary": a.get("summary", ""),
            }
        )

    # Certificates
    for c in _extract_items("certifications"):
        date_val, _ = _extract_dates(c)
        url_raw = c.get("url", "")
        url_str = url_raw.get("href", "") if isinstance(url_raw, dict) else str(url_raw)
        out["certificates"].append(
            {
                "name": c.get("name", ""),
                "date": date_val or c.get("date", ""),
                "issuer": c.get("issuer", ""),
                "url": url_str,
            }
        )

    # Publications
    for p in _extract_items("publications"):
        date_val, _ = _extract_dates(p)
        url_raw = p.get("url", "")
        url_str = url_raw.get("href", "") if isinstance(url_raw, dict) else str(url_raw)
        out["publications"].append(
            {
                "name": p.get("name", ""),
                "publisher": p.get("publisher", ""),
                "releaseDate": date_val or p.get("date", ""),
                "url": url_str,
                "summary": p.get("summary", ""),
            }
        )

    # Skills
    for s in _extract_items("skills"):
        keywords = s.get("keywords", [])
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(",") if k.strip()]
        out["skills"].append(
            {
                "name": s.get("name", ""),
                "level": s.get("description", "") or str(s.get("level", "")),
                "keywords": keywords,
            }
        )

    # Languages
    for lang in _extract_items("languages"):
        out["languages"].append(
            {
                "language": lang.get("name", ""),
                "fluency": lang.get("description", ""),
            }
        )

    # Interests
    for item in _extract_items("interests"):
        keywords = item.get("keywords", [])
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(",") if k.strip()]
        out["interests"].append(
            {
                "name": item.get("name", ""),
                "keywords": keywords,
            }
        )

    # References
    for ref in _extract_items("references"):
        out["references"].append(
            {
                "name": ref.get("name", ""),
                "reference": ref.get("description", ""),
            }
        )

    # Projects
    for prj in _extract_items("projects"):
        start, end = _extract_dates(prj)
        url_raw = prj.get("url", "")
        url_str = url_raw.get("href", "") if isinstance(url_raw, dict) else str(url_raw)
        keywords = prj.get("keywords", [])
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(",") if k.strip()]
        out["projects"].append(
            {
                "name": prj.get("name", ""),
                "description": prj.get("description", "") or prj.get("summary", ""),
                "highlights": [],
                "keywords": keywords,
                "startDate": start,
                "endDate": end,
                "url": url_str,
                "roles": [],
            }
        )

    return out


def from_json_resume(data: dict[str, Any]) -> ResumeData:
    """Convert standard JSON Resume dictionary into a Reactive Resume ResumeData model.

    Args:
        data: Dictionary conforming to JSON Resume format.

    Returns:
        ResumeData instance ready for import or save.
    """
    basics_in = data.get("basics", {})
    location_raw = basics_in.get("location", {})
    if isinstance(location_raw, dict):
        loc_parts = [
            location_raw.get("city", ""),
            location_raw.get("region", ""),
            location_raw.get("countryCode", ""),
        ]
        loc_str = ", ".join(p for p in loc_parts if p) or location_raw.get("address", "")
    else:
        loc_str = str(location_raw)

    profiles_out: list[Profile] = []
    for i, p in enumerate(basics_in.get("profiles", [])):
        if isinstance(p, dict):
            profiles_out.append(
                Profile(
                    id=f"prof-{i}",
                    network=p.get("network", ""),
                    username=p.get("username", ""),
                    url=URLModel(label=p.get("network", "Profile"), href=p.get("url", "")),
                )
            )

    basics = Basics(
        name=basics_in.get("name", ""),
        headline=basics_in.get("label", ""),
        email=basics_in.get("email", ""),
        phone=basics_in.get("phone", ""),
        location=loc_str,
        website=URLModel(label="Website", href=basics_in.get("url", "")),
        picture=basics_in.get("image", ""),
        profiles=profiles_out,
    )

    # Sections mapping
    work_items: list[WorkItem] = []
    for i, w in enumerate(data.get("work", [])):
        if isinstance(w, dict):
            work_items.append(
                WorkItem(
                    id=f"work-{i}",
                    company=w.get("name", ""),
                    position=w.get("position", ""),
                    summary=w.get("summary", ""),
                    date=w.get("startDate", ""),
                    dates=ResumeItemDates(
                        start=w.get("startDate", ""),
                        end=w.get("endDate", ""),
                        present=(w.get("endDate", "").lower() == "present"),
                    ),
                    url=URLModel(label=w.get("name", "Company"), href=w.get("url", "")),
                )
            )

    edu_items: list[EducationItem] = []
    for i, e in enumerate(data.get("education", [])):
        if isinstance(e, dict):
            edu_items.append(
                EducationItem(
                    id=f"edu-{i}",
                    institution=e.get("institution", ""),
                    studyType=e.get("studyType", ""),
                    area=e.get("area", ""),
                    score=str(e.get("score", "")),
                    date=e.get("startDate", ""),
                    dates=ResumeItemDates(
                        start=e.get("startDate", ""),
                        end=e.get("endDate", ""),
                    ),
                    url=URLModel(label=e.get("institution", "School"), href=e.get("url", "")),
                )
            )

    skill_items: list[SkillItem] = []
    for i, s in enumerate(data.get("skills", [])):
        if isinstance(s, dict):
            skill_items.append(
                SkillItem(
                    id=f"skill-{i}",
                    name=s.get("name", ""),
                    description=s.get("level", ""),
                    keywords=s.get("keywords", []),
                )
            )

    project_items: list[ProjectItem] = []
    for i, prj in enumerate(data.get("projects", [])):
        if isinstance(prj, dict):
            project_items.append(
                ProjectItem(
                    id=f"proj-{i}",
                    name=prj.get("name", ""),
                    description=prj.get("description", ""),
                    date=prj.get("startDate", ""),
                    dates=ResumeItemDates(
                        start=prj.get("startDate", ""),
                        end=prj.get("endDate", ""),
                    ),
                    url=URLModel(label=prj.get("name", "Project"), href=prj.get("url", "")),
                    keywords=prj.get("keywords", []),
                )
            )

    volunteer_items: list[VolunteerItem] = []
    for i, v in enumerate(data.get("volunteer", [])):
        if isinstance(v, dict):
            volunteer_items.append(
                VolunteerItem(
                    id=f"vol-{i}",
                    organization=v.get("organization", ""),
                    position=v.get("position", ""),
                    summary=v.get("summary", ""),
                    date=v.get("startDate", ""),
                    dates=ResumeItemDates(
                        start=v.get("startDate", ""),
                        end=v.get("endDate", ""),
                    ),
                    url=URLModel(label=v.get("organization", "Org"), href=v.get("url", "")),
                )
            )

    award_items: list[AwardItem] = []
    for i, a in enumerate(data.get("awards", [])):
        if isinstance(a, dict):
            award_items.append(
                AwardItem(
                    id=f"award-{i}",
                    title=a.get("title", ""),
                    awarder=a.get("awarder", ""),
                    date=a.get("date", ""),
                    summary=a.get("summary", ""),
                )
            )

    cert_items: list[CertificationItem] = []
    for i, c in enumerate(data.get("certificates", [])):
        if isinstance(c, dict):
            cert_items.append(
                CertificationItem(
                    id=f"cert-{i}",
                    name=c.get("name", ""),
                    issuer=c.get("issuer", ""),
                    date=c.get("date", ""),
                    url=URLModel(label=c.get("name", "Certificate"), href=c.get("url", "")),
                )
            )

    pub_items: list[PublicationItem] = []
    for i, p in enumerate(data.get("publications", [])):
        if isinstance(p, dict):
            pub_items.append(
                PublicationItem(
                    id=f"pub-{i}",
                    name=p.get("name", ""),
                    publisher=p.get("publisher", ""),
                    date=p.get("releaseDate", "") or p.get("date", ""),
                    summary=p.get("summary", ""),
                    url=URLModel(label=p.get("name", "Publication"), href=p.get("url", "")),
                )
            )

    lang_items: list[LanguageItem] = []
    for i, l_item in enumerate(data.get("languages", [])):
        if isinstance(l_item, dict):
            lang_items.append(
                LanguageItem(
                    id=f"lang-{i}",
                    name=l_item.get("language", ""),
                    description=l_item.get("fluency", ""),
                )
            )

    interest_items: list[InterestItem] = []
    for i, item in enumerate(data.get("interests", [])):
        if isinstance(item, dict):
            interest_items.append(
                InterestItem(
                    id=f"int-{i}",
                    name=item.get("name", ""),
                    keywords=item.get("keywords", []),
                )
            )

    ref_items: list[ReferenceItem] = []
    for i, ref in enumerate(data.get("references", [])):
        if isinstance(ref, dict):
            ref_items.append(
                ReferenceItem(
                    id=f"ref-{i}",
                    name=ref.get("name", ""),
                    description=ref.get("reference", ""),
                )
            )

    sections = {
        "work": Section(id="work", name="Work Experience", items=work_items),
        "education": Section(id="education", name="Education", items=edu_items),
        "skills": Section(id="skills", name="Skills", items=skill_items),
        "projects": Section(id="projects", name="Projects", items=project_items),
        "volunteer": Section(id="volunteer", name="Volunteering", items=volunteer_items),
        "awards": Section(id="awards", name="Awards", items=award_items),
        "certifications": Section(id="certifications", name="Certifications", items=cert_items),
        "publications": Section(id="publications", name="Publications", items=pub_items),
        "languages": Section(id="languages", name="Languages", items=lang_items),
        "interests": Section(id="interests", name="Interests", items=interest_items),
        "references": Section(id="references", name="References", items=ref_items),
    }

    return ResumeData(basics=basics, sections=sections)
