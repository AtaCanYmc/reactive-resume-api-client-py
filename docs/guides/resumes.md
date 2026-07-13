# Managing Resumes (CRUD)

Detailed guide on creating, reading, updating, deleting, and exporting resumes.

---

## 📝 1. Creating and Importing Resumes

To create a new resume, build a `ResumeImportData` Pydantic model. You can specify top-level personal details under `basics` and structure list entries under `sections`:

```python
from reactive_resume import RxResumeClient
from reactive_resume.models import ResumeImportData, Basics, Section, WorkItem

# Prepare Pydantic Model
import_data = ResumeImportData(
    title="Ata Can Yaymacı - Lead Architect",
    basics=Basics(
        name="Ata Can Yaymacı",
        headline="Software Architect",
        email="ata@example.com",
        phone="+905555555555"
    ),
    sections={
        "work": Section(
            id="work",
            name="Work Experience",
            items=[
                WorkItem(
                    id="work-item-1",
                    company="Google DeepMind",
                    position="AI Resident",
                    date="2024 - Present",
                    summary="Developing autonomous agent frameworks."
                )
            ]
        )
    }
)

with RxResumeClient(base_url="https://rxresu.me", api_key="my_key") as client:
    new_resume = client.resumes.import_resume(import_data)
    print(f"Created Resume ID: {new_resume.id}")
```

---

## 🔍 2. Reading and Listing Resumes

You can retrieve either all resumes belonging to the authenticated user or fetch a specific resume:

```python
with RxResumeClient(base_url="https://rxresu.me", api_key="my_key") as client:
    # List all
    all_resumes = client.resumes.list()
    print(f"Total Resumes: {len(all_resumes)}")

    # Get by ID
    resume = client.resumes.get("test-resume-id")
    print(f"Resume Name: {resume.name}")
    print(f"Email: {resume.data.basics.email}")
```

---

## ✏️ 3. Updating Resumes

Updates are executed via the `update()` method, which performs a `PATCH` request to modify specific settings or structure:

```python
with RxResumeClient(base_url="https://rxresu.me", api_key="my_key") as client:
    # Update properties like name, slug, visibility, etc.
    updated = client.resumes.update(
        resume_id="test-resume-id",
        data={"name": "New Portfolio Name", "visibility": "private"}
    )
    print(f"Updated Name: {updated.name}")
```

---

## 🗑️ 4. Deleting Resumes

To delete a resume permanently:

```python
with RxResumeClient(base_url="https://rxresu.me", api_key="my_key") as client:
    client.resumes.delete("test-resume-id")
    print("Resume deleted successfully.")
```

---

## 📄 5. Exporting PDF

To get the download link to the compiled PDF document of a specific resume:

```python
with RxResumeClient(base_url="https://rxresu.me", api_key="my_key") as client:
    pdf_url = client.resumes.get_pdf_url("test-resume-id")
    print(f"Download PDF: {pdf_url}")
```
